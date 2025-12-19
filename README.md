# Towers of Hanoi Constraint Learning

This project implements the constraint learning algorithm from "Inverse reinforcement learning through logic constraint inference" by Baert et. al. The goal is to uncover the constraint that larger disks may not be placed on top of smaller disks while completing the Towers of Hanoi task. 

## 1. Methodology

The environment is defined as a Markov Decision Process (MDP) without a reward function: $\mathcal{M} = (S, A, T, \gamma)$.

### 2. Maximum Entropy IRL
We use Maximum Entropy IRL to estimate the **State-Action Visitation Frequency** $D_{sa}$. This value represents how often an unconstrained agent would take a specific action to reach a goal efficiently.

$$D_{sa} = \sum_{t=0}^{H} P(s_t = s, a_t = a \mid \pi)$$

Where $\pi$ is the maximum-entropy policy. $\pi$ initially sets all actions as equally likely, and removes actions whenever they are identified as candidate constraints.

The algorithm then identifies a candidate violation state-action pair, where the unconstrained agent's visitation frequency is high, but the expert's is zero. A candidate violation $c^*$ is selected as:

$$c^* = \arg\max_{(s,a) \notin T} D_{sa}(s, a)$$

where $T$ is the set of expert trajectories. 

### 3. Symbolic Induction
Once a candidate $c^*$ is identified, we use **ILASP** to find a hypothesis $H$ that explains why the candidate is a violation while the expert's moves are not. ILASP uses the language bias which sets the structure of the generated constraints. The head of a generated constraint is `violation` and the body predicates `moving_disk(X)`, `disk_below(X)`, and `smaller(X, Y)`. ILASP generates constraints $H$ that, with background knowledge $B$, satisfy the following:

$$B \cup H \models E^+ \quad \text{and} \quad B \cup H \not\models E^-$$

In other words, the constraints must be true for all positive violation examples and false for all negative violation examples. ILASP may generate multiple rules, it selects the simplest rule out all candidates (the rule with the fewest number of literals in the body). 

### 4. Results
We generated 26 trajectories of solving Towers of Hanoi with three disks and three pegs. The three disks are labeled 1, 2, and 3. Disk 1 is smaller than disk 2 which is smaller than disk 3. After a single iteration of IRL and ILASP, the following constraint was discovered:

`violation :- moving_disk(V1), disk_below(V2), smaller(V2, V1).`

which is precisely the underlying constraint of Towers of Hanoi: it is a violation to move $V1$ on top of $V2$ if $V2$ is smaller than $V1$. 

## 2. Instructions for Running

Requirements: numpy, re, clingo. Additionally you will need an ILASP implementation. There is no pip package for this but you can find an implementation here: https://github.com/ilaspltd/ILASP-releases. 

To run, clone this repo and navigate to the new directory. Enter command `python main.py` to run the IRL-ILASP solver on the Towers of Hanoi trajectories and generate the smaller-disk constraint.  
## 3. Future Work

Future work on this project will entail discovering constraints in more complex environments. For example, the Proper Shopper environment https://github.com/dtl184/propershopper where agents must follow social norms in addition to completing tasks. 

