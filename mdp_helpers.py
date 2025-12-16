import numpy as np
import subprocess
import itertools
import os

# --- Constants for 3-Disk Towers of Hanoi ---

# Pegs are 1, 2, 3
PEGS = [1, 2, 3] 
# Disks are 1 (smallest), 2, 3 (largest)
DISKS = [1, 2, 3]

# 1. State Space, Action Space, and Goals

# STATE_SPACE: All 3^3 = 27 possible state tuples (D1_peg, D2_peg, D3_peg)
STATE_SPACE = list(itertools.product(PEGS, PEGS, PEGS)) 

# ACTION_SPACE: All 3 * 2 = 6 possible move actions: move(from_peg, to_peg)
ACTION_SPACE = [f'move({p1}, {p2})' for p1 in PEGS for p2 in PEGS if p1 != p2]

# GOALS: Target state (all disks on peg 3)
GOALS = [(3, 3, 3)]

# Map disk size index to the state tuple index: D1 -> 0, D2 -> 1, D3 -> 2
DISK_INDEX_MAP = {1: 0, 2: 1, 3: 2}

# 2. MDP Class for irl-maxent compatibility

class MDP:
    """A minimal MDP class compatible with irl-maxent library structure."""
    def __init__(self, T, S, A, gamma, horizon):
        # T: Transition matrix (n_states, n_actions, n_states)
        self.T = T
        self.S = S
        self.A = A
        self.gamma = gamma
        self.horizon = horizon
        self.n_states = len(S)
        self.n_actions = len(A)

# 3. Core MDP Functions

def get_sparse_reward(s):
    """
    Returns the sparse reward for state s (1 for goal state, 0 otherwise).
    """
    return 1.0 if s in GOALS else 0.0

# 4. Logic Mapping Functions (ψ and ψ⁻¹)

def get_disk_on_top(state, peg):
    """
    Helper function to find the smallest disk on a given peg.
    Returns the disk number (1, 2, or 3) or 0 if the peg is empty.
    """
    disks_on_peg = [d for d in DISKS if state[DISK_INDEX_MAP[d]] == peg]
    return min(disks_on_peg) if disks_on_peg else 0

def convert_state_to_facts(s):
    """Converts a state tuple (s) into a list of first-order logic facts."""
    facts = []
    
    # 1. at(Disk, Peg) facts
    for disk in DISKS:
        peg = s[DISK_INDEX_MAP[disk]]
        facts.append(f'at(d{disk}, p{peg})')
        
    # 2. clear(Peg) facts: A peg is clear if the top disk is D1
    for peg in PEGS:
        top_disk = get_disk_on_top(s, peg)
        if top_disk == 1: # The smallest disk is on top, or peg is empty
            facts.append(f'clear(p{peg})')
            
    # 3. on_top(Disk, Peg) facts
    for peg in PEGS:
        top_disk = get_disk_on_top(s, peg)
        if top_disk > 0:
            facts.append(f'on_top(d{top_disk}, p{peg})')
            
    return facts

def convert_action_to_predicate(a):
    """
    Converts an action string 'move(P1, P2)' into a logic predicate 'move(P1, P2)'.
    """
    # Assuming action 'move(1, 2)' is already in a logical format
    return a.replace('move(', 'move(p').replace(',', ',p').replace(')', ')')
    
def trajectory_to_logic_examples(expert_trajectories, C):
    """
    Maps (s, a) pairs to positive (E+) and negative (E-) logic examples (ψ mapping).
    
    E+ are successful (s, a) pairs from expert data.
    E- are illegal (s, a) pairs from the current constraint set C.
    """
    E_plus = set()
    E_minus = set()
    
    # Positive Examples (E+): All observed (s, a) from expert trajectories
    for traj_id, trajectory in enumerate(expert_trajectories):
        for step_idx, (s, a, s_prime) in enumerate(trajectory):
            state_facts = convert_state_to_facts(s) 
            action_predicate = convert_action_to_predicate(a)
            
            # ILASP format: pos(ID, [FACTS], [ACTION]).
            E_plus.add(f"pos(t{traj_id}_{step_idx}, [{', '.join(state_facts)}], [{action_predicate}]).")

    # Negative Examples (E-): All inferred constrained (s, a) from set C
    for s, a in C:
        state_facts = convert_state_to_facts(s)
        action_predicate = convert_action_to_predicate(a)
        
        # ILASP format: neg(ID, [FACTS], [ACTION]).
        E_minus.add(f"neg(c{len(E_minus)}, [{', '.join(state_facts)}], [{action_predicate}]).")
        
    return list(E_plus), list(E_minus)


def hypothesis_to_constraints(H_asp, mdp):
    """
    Maps the induced logic program H back to a generalized set of constrained (s, a) pairs (ψ⁻¹ mapping).
    
    Requires the 'clingo' executable to be in your PATH.
    """
    C_generalized = set()
    
    TEMP_ASP_FILE = 'current_hypothesis.lp'
    TEMP_FACTS_FILE = 'current_facts.lp'
    # This must match the head predicate defined in ilasp_config.lp
    CONSTRAINT_PREDICATE = 'constraint_violation' 

    # 1. Write H into a temporary file
    with open(TEMP_ASP_FILE, 'w') as f:
        f.write(H_asp)

    # 2. Loop through all possible (s, a) pairs and check for violation
    for s in mdp.S:
        for a in mdp.A:
            # a. Convert (s, a) to facts
            state_facts = convert_state_to_facts(s)
            action_predicate = convert_action_to_predicate(a)
            
            # Create a file with the facts for the current (s, a) pair
            with open(TEMP_FACTS_FILE, 'w') as f:
                # Add domain definitions (disk/peg definitions)
                for d in DISKS: f.write(f'disk(d{d}).\n')
                for p in PEGS: f.write(f'peg(p{p}).\n')
                f.write('smaller_than(d1, d2). smaller_than(d2, d3). smaller_than(d1, d3).\n')
                
                # Add state and action facts
                f.write('\n'.join([f"{fact}." for fact in state_facts]))
                f.write(f"\n{action_predicate}.")

            # b. Run Clingo with the facts and H
            clingo_command = [
                'clingo',
                TEMP_ASP_FILE,
                TEMP_FACTS_FILE,
                '-c', 'mode=check'
            ]
            
            try:
                result = subprocess.run(clingo_command, capture_output=True, text=True, timeout=5, check=False)
                
                # c. Check if the constraint predicate is in the output model
                if f'{CONSTRAINT_PREDICATE}' in result.stdout:
                    C_generalized.add((s, a))
                
            except subprocess.TimeoutExpired:
                pass
            except FileNotFoundError:
                print("Error: 'clingo' executable not found. Cannot generalize constraints.")
                # Clean up only if clingo is not found to prevent further errors
                if os.path.exists(TEMP_ASP_FILE): os.remove(TEMP_ASP_FILE)
                if os.path.exists(TEMP_FACTS_FILE): os.remove(TEMP_FACTS_FILE)
                return set()

    # Clean up temporary files
    if os.path.exists(TEMP_ASP_FILE): os.remove(TEMP_ASP_FILE)
    if os.path.exists(TEMP_FACTS_FILE): os.remove(TEMP_FACTS_FILE)
    
    return C_generalized