import collections
import itertools

# --- Configuration ---
PEGS = [1, 2, 3]
DISKS = [1, 2, 3]
GOAL_STATE = (3, 3, 3)

def get_top_disk(state, peg):
    disks_on_peg = [d for d in DISKS if state[d-1] == peg]
    return min(disks_on_peg) if disks_on_peg else 99

def get_legal_neighbors(state):
    neighbors = []
    for from_peg in PEGS:
        disk_to_move = get_top_disk(state, from_peg)
        if disk_to_move == 99: continue
        
        for to_peg in PEGS:
            if from_peg == to_peg: continue
            
            dest_top_disk = get_top_disk(state, to_peg)
            if disk_to_move < dest_top_disk:
                new_state = list(state)
                new_state[disk_to_move-1] = to_peg
                action = f"move({from_peg}, {to_peg})"
                neighbors.append((tuple(new_state), action))
    return neighbors

def find_optimal_path(start_state, goal_state):
    queue = collections.deque([(start_state, [])])
    visited = {start_state}
    
    while queue:
        current_state, path = queue.popleft()
        if current_state == goal_state:
            return path
        
        for next_state, action in get_legal_neighbors(current_state):
            if next_state not in visited:
                visited.add(next_state)
                new_path = path + [(current_state, action, next_state)]
                queue.append((next_state, new_path))
    return []

# Generate trajectories from all 27 states
all_states = list(itertools.product(PEGS, PEGS, PEGS))
all_trajectories = []

for start in all_states:
    if start == GOAL_STATE: continue
    path = find_optimal_path(start, GOAL_STATE)
    if path:
        all_trajectories.append(path)

# Save to file
with open('expert_trajectories.txt', 'w') as f:
    f.write("EXPERT_TRAJECTORIES = [\n")
    for traj in all_trajectories:
        f.write("    [\n")
        for step in traj:
            f.write(f"        {step},\n")
        f.write("    ],\n")
    f.write("]\n")

print(f"Generated {len(all_trajectories)} trajectories and saved to expert_trajectories.txt")