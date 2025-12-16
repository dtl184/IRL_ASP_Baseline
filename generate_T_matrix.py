import numpy as np
import itertools
import re
import pandas as pd

# --- Constants for 3-Disk Towers of Hanoi ---
PEGS = [1, 2, 3] 
DISKS = [1, 2, 3] # 1 (smallest), 2, 3 (largest)
DISK_INDEX_MAP = {1: 0, 2: 1, 3: 2}

# Generate State Space (27 states)
# State is (Disc1_peg, Disc2_peg, Disc3_peg)
STATE_SPACE = list(itertools.product(PEGS, PEGS, PEGS)) 
STATE_TO_INDEX = {state: i for i, state in enumerate(STATE_SPACE)}

# Generate Action Space (6 actions)
ACTION_SPACE = [f'move({p1}, {p2})' for p1 in PEGS for p2 in PEGS if p1 != p2]
ACTION_TO_INDEX = {action: i for i, action in enumerate(ACTION_SPACE)}

def get_disks_on_peg(state, peg):
    """Returns a list of disks (1, 2, 3) on a given peg, sorted smallest to largest."""
    # Map from disk index (0, 1, 2) to disk number (1, 2, 3)
    disks = [d for d in DISKS if state[DISK_INDEX_MAP[d]] == peg]
    return sorted(disks)

def get_disk_on_top(state, peg):
    """Returns the smallest disk on a given peg (the one that can be moved), or 0 if empty."""
    disks_on_peg = get_disks_on_peg(state, peg)
    return disks_on_peg[0] if disks_on_peg else 0

def is_move_physically_legal(state, from_peg, to_peg):
    """Checks if a move from_peg to to_peg is physically legal based on Hanoi rules."""
    
    # 1. Determine disk to move (must be the top disk on the source peg)
    disk_to_move = get_disk_on_top(state, from_peg)
    
    # If source peg is empty, the move is illegal
    if disk_to_move == 0:
        return False, 0
    
    # 2. Check placement rule on the target peg
    top_disk_on_target = get_disk_on_top(state, to_peg)
    
    # If target peg is not empty, the disk being moved must be smaller than the top disk on the target.
    if top_disk_on_target != 0 and disk_to_move > top_disk_on_target:
        return False, 0
        
    return True, disk_to_move

def get_next_state(state, disk_to_move, to_peg):
    """Returns the new state tuple after moving the disk."""
    new_state_list = list(state)
    disk_idx = DISK_INDEX_MAP[disk_to_move]
    new_state_list[disk_idx] = to_peg
    
    return tuple(new_state_list)

# --- Transition Matrix Generation ---

# T_prob[s_idx, a_idx, s_prime_idx]
T_prob = np.zeros((len(STATE_SPACE), len(ACTION_SPACE), len(STATE_SPACE)), dtype=np.float32)

# Regular expression to parse move(p1, p2)
move_pattern = re.compile(r'move\((\d+),\s*(\d+)\)')

for s_idx, state in enumerate(STATE_SPACE):
    for a_idx, action in enumerate(ACTION_SPACE):
        
        # Parse action string
        match = move_pattern.match(action)
        if not match:
            continue
            
        from_peg = int(match.group(1))
        to_peg = int(match.group(2))
        
        # Check physical legality of the move
        is_legal, disk_to_move = is_move_physically_legal(state, from_peg, to_peg)
        
        if is_legal:
            # Determine the next state
            s_prime = get_next_state(state, disk_to_move, to_peg)
            s_prime_idx = STATE_TO_INDEX.get(s_prime)
            
            if s_prime_idx is not None:
                # Since the environment is deterministic, set P(s'|s, a) = 1
                T_prob[s_idx, a_idx, s_prime_idx] = 1.0

# Save the matrix
np.save('T_prob.npy', T_prob)

# --- Create CSV sample for verification ---
def matrix_to_csv(T, states, actions):
    data = []
    for s_idx, s in enumerate(states):
        for a_idx, a in enumerate(actions):
            s_prime_indices = np.where(T[s_idx, a_idx, :] > 0)[0]
            for sp_idx in s_prime_indices:
                sp = states[sp_idx]
                prob = T[s_idx, a_idx, sp_idx]
                data.append({'state': s, 'action': a, 'next_state': sp, 'prob': prob})
    
    return data[:20] # Limit to 20 entries for a quick look

csv_data = matrix_to_csv(T_prob, STATE_SPACE, ACTION_SPACE)
df = pd.DataFrame(csv_data)
df.to_csv('T_prob_check.csv', index=False)

print(f"Transition Matrix (T_prob.npy) generated with shape: {T_prob.shape}")
print("A sample of non-zero transitions saved to T_prob_check.csv for verification.")