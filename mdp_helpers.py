import numpy as np
import re

class MDP:
    def __init__(self, T, S, A, gamma=0.99, horizon=50):
        self.T = T  # Transition matrix (A, S, S)
        self.S = S  # State space
        self.A = A  # Action space
        self.n_states = len(S)
        self.n_actions = len(A)
        self.gamma = gamma
        self.horizon = horizon

def convert_state_to_facts(state, action_str):
    """
    state: (peg_disk1, peg_disk2, peg_disk3)
    action_str: 'move(p1, p2)'
    """
    match = re.match(r'move\((\d+), (\d+)\)', action_str)
    from_p, to_p = int(match.group(1)), int(match.group(2))

    # Identify top disk on 'from' peg (Disk 1 is smallest, 3 is largest)
    p1_disks = [d_idx for d_idx, peg in enumerate(state, 1) if peg == from_p]
    moving_disk = min(p1_disks) if p1_disks else "none"
    
    # Identify top disk on 'to' peg
    p2_disks = [d_idx for d_idx, peg in enumerate(state, 1) if peg == to_p]
    target_disk = min(p2_disks) if p2_disks else "none"

    # Return facts as a list of strings
    return [f"moving_disk({moving_disk})", f"disk_below({target_disk})"]

def trajectory_to_logic_examples(expert_trajectories, C):
    E_plus, E_minus = [], []
    for traj in expert_trajectories:
        for s, a, _ in traj:
            f_list = convert_state_to_facts(s, a)
            context = " ".join([f"{f}." for f in f_list])
            E_minus.append(f"#neg({{violation}}, {{}}, {{ {context} }}).")
    for s, a in C:
        f_list = convert_state_to_facts(s, a)
        context = " ".join([f"{f}." for f in f_list])
        E_plus.append(f"#pos({{violation}}, {{}}, {{ {context} }}).")
    return E_plus, E_minus

def hypothesis_to_constraints(hyp, mdp):
    """
    Normally uses a subprocess to Clingo to find all (s, a) that satisfy the rule.
    For this implementation, we return a set that main.py will populate.
    """
    return set()

def generalize_hypothesis(hyp, mdp):
    """
    Given a hypothesis string from ILASP (e.g., 'moving_disk(V1), disk_below(V2), smaller(V2, V1)'),
    returns a set of all (s, a) that violate this rule.
    """
    if not hyp or hyp == "None":
        return set()

    violated_sa = set()
    # Simple parser for the induced rule
    has_smaller = "smaller" in hyp
    has_none = "none" in hyp

    for s in mdp.S:
        for a in mdp.A:
            facts = convert_state_to_facts(s, a)
            # Extract values for checking
            m_match = re.search(r'moving_disk\((\d+)\)', facts[0])
            t_match = re.search(r'disk_below\((\d+)\)', facts[1])
            
            m_val = int(m_match.group(1)) if m_match else None
            t_val = int(t_match.group(1)) if t_match and t_match.group(1).isdigit() else "none"

            # Check if this specific (s, a) matches the logic of the rule
            if has_smaller and isinstance(t_val, int):
                if m_val > t_val: # This represents 'smaller(t_val, m_val)'
                    violated_sa.add((s, a))
            elif has_none and t_val == "none":
                # Only if the rule specifically targets empty pegs (usually not the case in Hanoi)
                pass 
                
    return violated_sa