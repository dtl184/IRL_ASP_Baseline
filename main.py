import numpy as np
import subprocess
import os
import irl_maxent as irl
import itertools
import pandas as pd
import re

# =========================================================================
# 1. Towers of Hanoi Constants (Shared with mdp_helpers)
# These constants MUST match those used to generate T_prob.npy
# =========================================================================
PEGS = [1, 2, 3] 
DISKS = [1, 2, 3] # 1 (smallest), 2, 3 (largest)

# State is (Disc1_peg, Disc2_peg, Disc3_peg)
STATE_SPACE = list(itertools.product(PEGS, PEGS, PEGS)) 
STATE_TO_INDEX = {state: i for i, state in enumerate(STATE_SPACE)}

# Action is 'move(P1, P2)'
ACTION_SPACE = [f'move({p1}, {p2})' for p1 in PEGS for p2 in PEGS if p1 != p2]
ACTION_TO_INDEX = {action: i for i, action in enumerate(ACTION_SPACE)}
# =========================================================================


# Import dependent functions from mdp_helpers
# Note: Ensure mdp_helpers.py is in the same directory and contains the
# definitions provided previously (MDP class, get_sparse_reward, etc.)
from mdp_helpers import (
    MDP,
    get_sparse_reward, # Requires only state 's'
    trajectory_to_logic_examples,
    hypothesis_to_constraints
)

# --- Configuration ---
HORIZON = 50 
MAX_ITERATIONS = 50

# --- Core MaxEnt IRL Functions (Using irl-maxent) ---

# --- Core MaxEnt IRL Functions (Using irl-maxent) ---
def calculate_constrained_policy_and_frequencies(mdp, C, expert_sa_count):
    """
    Calculates the constrained policy π^C and state-action visitation D_sa.
    """
    
    # 1. IMPORT FIX and T-matrix Transposition
    from irl_maxent import maxent 
    from __main__ import STATE_SPACE, STATE_TO_INDEX, ACTION_SPACE
    
    # CRITICAL FIX: The irl-maxent library expects T to be (S, S', A), but ours is (S, A, S').
    # Transpose mdp.T from (S, A, S') to (S, S', A) before calling library functions.
    T_transposed = mdp.T.transpose(0, 2, 1) # Permute axes 1 (A) and 2 (S')
    
    # 2. Define Reward Vector and Terminal States
    reward_vector = np.array([get_sparse_reward(s) for s in mdp.S])
    GOAL_STATE = (3, 3, 3)
    try:
        terminal_index = STATE_TO_INDEX[GOAL_STATE]
        TERMINAL_STATES = [terminal_index]
    except KeyError:
        TERMINAL_STATES = []
    
    # 3. Compute the nominal MaxEnt Policy π_nom
    # Pass the correctly shaped T_transposed matrix
    pi_nom = maxent.local_action_probabilities(
        p_transition=T_transposed, 
        terminal=TERMINAL_STATES, 
        reward=reward_vector
    )
    
    # 4. Enforce Constraints C on the nominal policy (creates π^C)
    pi_constrained = pi_nom.copy()
    
    for s_idx, s in enumerate(STATE_SPACE):
        for a_idx, a in enumerate(ACTION_SPACE):
            if (s, a) in C:
                pi_constrained[s_idx, a_idx] = 0.0
    
    # Re-normalize the constrained policy probabilities for each state
    for s_idx in range(mdp.n_states):
        sum_prob = np.sum(pi_constrained[s_idx, :])
        if sum_prob > 1e-6:
            pi_constrained[s_idx, :] /= sum_prob

    # 5. Compute State Visitation Frequency (D_s) for π^C
    D0 = np.array(expert_sa_count)
    D0_norm = D0 / D0.sum() if D0.sum() > 0 else np.zeros_like(D0)
    
    # Compute SVF (D_s). Must also pass the T_transposed matrix.
    D_s = maxent.expected_svf_from_policy(
        p_transition=T_transposed, 
        p_initial=D0_norm, 
        terminal=TERMINAL_STATES, 
        p_action=pi_constrained
    )

    # 6. Compute State-Action Visitation Frequency (D_sa)
    D_sa = np.zeros((mdp.n_states, mdp.n_actions))
    for s_idx in range(mdp.n_states):
        for a_idx in range(mdp.n_actions):
            D_sa[s_idx, a_idx] = D_s[s_idx] * pi_constrained[s_idx, a_idx]
            
    D_sa_vector = D_sa.flatten()
    
    return pi_constrained, D_s, D_sa_vector

# --- Main Logic ---

def maxent_irl_ilp(mdp, expert_trajectories, B_path, M_path):
    """
    The main iterative algorithm.
    """
    # 1. Initialization
    C = set()
    H = "None"
    
    # Helper for fast lookups and initialization of D0
    Expert_SA = set((s, a) for traj in expert_trajectories for s, a, _ in traj)
    
    # Expert state count for D0 approximation (initial state distribution)
    expert_state_count = np.zeros(mdp.n_states)
    for trajectory in expert_trajectories:
        if trajectory:
            initial_state = trajectory[0][0]
            try:
                s_idx = mdp.S.index(initial_state)
                expert_state_count[s_idx] += 1
            except ValueError:
                # Handle case where initial state is not in STATE_SPACE (shouldn't happen for Hanoi)
                pass
            
    expert_sa_count = expert_state_count # Used as the initial state distribution D0

    for i in range(MAX_ITERATIONS):
        print(f"\n--- Iteration {i+1}/{MAX_ITERATIONS} ---")
        
        # A. MaxEnt Constraint Inference (Algorithm 1, Steps 3-5)
        pi_c, D_s, D_sa_vector = calculate_constrained_policy_and_frequencies(
            mdp, C, expert_sa_count
        )
        
        D_sa_matrix = D_sa_vector.reshape(mdp.n_states, mdp.n_actions)
        
        # Find the state-action pair with the highest D_sa that is NOT in the expert data
        c_star = None
        max_D_sa = -np.inf
        
        for s_idx, s in enumerate(STATE_SPACE):
            for a_idx, a in enumerate(ACTION_SPACE):
                s_a = (s, a)
                if s_a not in Expert_SA and s_a not in C:
                    if D_sa_matrix[s_idx, a_idx] > max_D_sa:
                        max_D_sa = D_sa_matrix[s_idx, a_idx]
                        c_star = s_a
        
        if c_star is None or max_D_sa < 1e-6:
            print("Convergence: No new highly visited unobserved constraint found.")
            break
            
        # Update constraints C with the most probable constraint c*
        C.add(c_star)
        print(f"Inferred new constraint c*: {c_star} (D_sa={max_D_sa:.4f})")
        print(f"Total constraints C before induction: {len(C)}")

        # B. Program Induction (Algorithm 1, Steps 6-8)
        
        # 1. Map to Logic Examples (ψ)
        E_plus, E_minus = trajectory_to_logic_examples(expert_trajectories, C)
        
        # Write E+ and E- to temporary files for ILASP input
        with open("E_plus.txt", "w") as f:
            f.write("\n".join(E_plus))
        with open("E_minus.txt", "w") as f:
            f.write("\n".join(E_minus))
        
        # 2. Induce Hypothesis H (ILASP)
        ilasp_command = [
            'ilasp',
            '-B', B_path,  # Background Knowledge (B)
            '-M', M_path,  # Language Bias (M)
            '-P', 'E_plus.txt', # Positive Examples (E+)
            '-N', 'E_minus.txt' # Negative Examples (E-)
        ]
        
        try:
            print("Running ILASP...")
            result = subprocess.run(ilasp_command, capture_output=True, text=True, check=True)
            
            # Simple parsing: H is often the last answer set. Adjust as necessary.
            H_raw = result.stdout.strip().split('\n')[-1] 
            H = H_raw 
            print(f"Induced Hypothesis H: {H}")

        except subprocess.CalledProcessError as e:
            print(f"ILASP failed: {e.stderr}")
            break
        except FileNotFoundError:
            print("Error: 'ilasp' executable not found. Ensure ILASP is installed and in your PATH.")
            break
        
        # 3. Generalize and Update Constraints (ψ⁻¹)
        # This function runs Clingo over all (s,a) pairs using H
        C_generalized = hypothesis_to_constraints(H, mdp)
        C.update(C_generalized)
        print(f"Total constraints C after generalization: {len(C)}")
        
        # Clean up temporary files
        if os.path.exists("E_plus.txt"): os.remove("E_plus.txt")
        if os.path.exists("E_minus.txt"): os.remove("E_minus.txt")
        
    print(f"\n--- Final Result ---")
    print(f"Final Constraint Set C has {len(C)} elements.")
    print(f"Final Logic Program H: {H}")
    return H, C

if __name__ == '__main__':
    # --- TODO: Domain-Specific Data Setup ---
    # 1. Define expert trajectories
    # Provide a list of expert demonstrations. For the first iteration, even a single,
    # complete, valid trajectory is enough, but more data is better.
    EXPERT_TRAJECTORIES = [
        # Example valid path for Hanoi: move D1 (1->2), move D2 (1->3), move D1 (2->3)
        [
            ((1, 1, 1), 'move(1, 2)', (2, 1, 1)), # Move D1 from P1 to P2
            ((2, 1, 1), 'move(1, 3)', (2, 3, 1)), # Move D2 from P1 to P3 (D1 is on P2)
            ((2, 3, 1), 'move(2, 3)', (3, 3, 1))  # Move D1 from P2 to P3
        ]
        # ADD MORE TRAJECTORIES HERE
    ]
    
    # 2. Load Transition Probability matrix
    try:
        TRANSITION_PROBABILITY = np.load('T_prob.npy')
        print(f"Successfully loaded T_prob.npy with shape: {TRANSITION_PROBABILITY.shape}")
    except FileNotFoundError:
        print("ERROR: T_prob.npy not found. Please run 'generate_mdp.py' first.")
        # Exit or use dummy data to allow execution to proceed (but results will be invalid)
        TRANSITION_PROBABILITY = np.zeros((len(STATE_SPACE), len(ACTION_SPACE), len(STATE_SPACE)))
        
    
    # 3. Instantiate the MDP object
    mdp_instance = MDP(
        T=TRANSITION_PROBABILITY,
        S=STATE_SPACE,
        A=ACTION_SPACE,
        gamma=0.99, # Discount factor
        horizon=HORIZON
    )
    
    # 4. Paths to your ILASP configuration files
    BACKGROUND_PATH = 'ilasp_config.lp'
    LANGUAGE_BIAS_PATH = 'ilasp_config.lp' # Often the same file
    
    # Run the algorithm
    final_hypothesis, final_constraints = maxent_irl_ilp(
        mdp=mdp_instance,
        expert_trajectories=EXPERT_TRAJECTORIES,
        B_path=BACKGROUND_PATH,
        M_path=LANGUAGE_BIAS_PATH
    )