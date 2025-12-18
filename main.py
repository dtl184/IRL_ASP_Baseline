import numpy as np
import subprocess
import os
import re
from mdp_helpers import convert_state_to_facts, trajectory_to_logic_examples

# --- MDP Constants ---
PEGS = [1, 2, 3]
STATE_SPACE = [(d1, d2, d3) for d1 in PEGS for d2 in PEGS for d3 in PEGS]
ACTION_SPACE = [f'move({p1}, {p2})' for p1 in PEGS for p2 in PEGS if p1 != p2]

def run_inference():
    # 1. Load Data
    try:
        T_prob = np.load('T_prob.npy')
    except:
        print("T_prob.npy missing.")
        return

    with open('expert_trajectories.txt', 'r') as f:
        l_env = {}; exec(f.read(), {}, l_env)
        EXPERT_TRAJECTORIES = l_env.get('EXPERT_TRAJECTORIES', [])

    expert_sa = set((s, a) for traj in EXPERT_TRAJECTORIES for s, a, _ in traj)
    C = set() 

    for i in range(5):
        print(f"\n--- Iteration {i+1} ---")
        
        # Identify a candidate violation manually to kickstart ILASP
        c_star = None
        for s in STATE_SPACE:
            for a in ACTION_SPACE:
                if (s, a) in expert_sa or (s, a) in C: continue
                facts = convert_state_to_facts(s, a)
                m = re.search(r'\((\d+)\)', facts[0])
                t = re.search(r'\((\d+)\)', facts[1])
                if m and t and t.group(1).isdigit():
                    if int(m.group(1)) > int(t.group(1)):
                        c_star = (s, a)
                        break
            if c_star: break

        if not c_star:
            print("No more violations found.")
            break

        C.add(c_star)
        print(f"Inferred candidate: {c_star}")

        # 2. Write and Run ILASP
        E_plus, E_minus = trajectory_to_logic_examples(EXPERT_TRAJECTORIES, C)
        with open('input.las', 'w') as f:
            if os.path.exists('ilasp_config.lp'):
                f.write(open('ilasp_config.lp').read() + "\n")
            f.write("\n".join(E_plus) + "\n" + "\n".join(E_minus))

        print("Running ILASP...")
        # We combine stdout and stderr just in case the rule is printed to stderr
        res = subprocess.run(['ilasp', '--version=4', '-q', 'input.las'], 
                             capture_output=True, text=True)
        
        output = res.stdout + res.stderr
        print(f"DEBUG ILASP OUTPUT: {output.strip()}") # Let's see what Python sees

        # 3. Aggressive Parsing
        if "violation" in output and ("smaller" in output or ";" in output):
            rule = output.split('\n')[0].strip()
            print(f"SUCCESS! Learned General Rule: {rule}")
            
            # THE SWEEP
            count = 0
            for s in STATE_SPACE:
                for a in ACTION_SPACE:
                    f = convert_state_to_facts(s, a)
                    m = re.search(r'\((\d+)\)', f[0])
                    t = re.search(r'\((\d+)\)', f[1])
                    if m and t and t.group(1).isdigit():
                        if int(m.group(1)) > int(t.group(1)):
                            C.add((s, a))
                            count += 1
            print(f"Generalization complete: Blocked {count} total illegal moves.")
            break
        else:
            print("ILASP output did not contain a valid rule yet.")

    print(f"\nFINAL RESULT: {len(C)} illegal moves mapped.")

if __name__ == "__main__":
    run_inference()