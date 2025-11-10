# main.py
from __future__ import annotations
from typing import Iterable, List, Tuple, Dict
from dataclasses import dataclass, field

from core import (
    MDP, State, Action, Transition, FeatureExtractor, Rule,
    Constraints, ListTrajectory
)
from learn import (
    LearnConfig, learn_constraints_from_trajectories
)

# -------------------------------------------------------------------
# 1) Define YOUR domain MDP and feature extractor here (single file).
#    This is a minimal example (stub) — replace with your domain logic.
# -------------------------------------------------------------------

@dataclass
class MyDomain(MDP):
    # Start with empty constraints; learning will fill these in.
    constraints: Constraints = field(default_factory=lambda: Constraints(rules=[], phi=lambda s,a: {}))

    def initial_state(self) -> State:
        # TODO: return your initial state (must be hashable)
        return ("init",)

    def is_terminal(self, s: State) -> bool:
        # TODO: implement your goal condition
        return s == ("goal",)

    def legal_actions(self, s: State):
        # TODO: return iterable of legal actions at state s
        if s == ("init",):
            return [("go", "mid")]
        if s == ("mid",):
            return [("go", "goal")]
        return []

    def apply(self, s: State, a: Action) -> State:
        # TODO: implement transition logic
        if s == ("init",) and a == ("go", "mid"):
            return ("mid",)
        if s == ("mid",) and a == ("go", "goal"):
            return ("goal",)
        return s

class MyPhi(FeatureExtractor):
    def __call__(self, s: State, a: Action) -> Dict[str, float]:
        # TODO: extract features for your domain
        # Example: treat "going to goal" as a boolean feature
        return {
            "action_go_goal": 1.0 if a == ("go", "goal") else 0.0,
            "is_from_init": 1.0 if s == ("init",) else 0.0,
        }

# -------------------------------------------------------------------
# 2) Load / build trajectories (as (s, a, s') triplets)
# -------------------------------------------------------------------

def load_trajectories() -> List[ListTrajectory]:
    """
    Provide your demonstration trajectories here.
    In general you'll parse logs → produce triplets [(s,a,s'), ...]
    """
    # Tiny toy demo (replace with your own data)
    t1: List[Transition] = [
        (("init",), ("go","mid"), ("mid",)),
        (("mid",),  ("go","goal"), ("goal",)),
    ]
    return [ListTrajectory(t1)]

# -------------------------------------------------------------------
# 3) Run learner to produce logic constraints and attach to MDP
# -------------------------------------------------------------------

def main():
    mdp = MyDomain()
    phi = MyPhi()
    trajectories = load_trajectories()

    cfg = LearnConfig(
        bool_feature_keys=["action_go_goal", "is_from_init"],
        # Optionally add numeric thresholds:
        # le_thresholds={"risk": 0.0},
        # ge_thresholds={"risk": 0.8},
    )

    result = learn_constraints_from_trajectories(mdp, trajectories, phi, cfg)

    # Attach constraints to the MDP instance (so downstream planners can use mdp.constraints.violates)
    mdp.constraints = result.constraints

    # --- Output ---
    print("[IRL] feature profile:")
    for k, v in sorted(result.profile.items()):
        print(f"  {k:20s} {v:.4f}")

    print("\n[ILP] learned constraint(s):")
    print(result.constraints.pretty())

    TP, FP, FN = result.best_rule_stats
    print(f"\n[ILP] rule stats: TP={TP} FP={FP} FN={FN}")

    # Example: check a violation call
    s = ("mid",)
    a = ("go", "goal")
    print(f"\n[CHECK] violates({s}, {a}) -> {mdp.constraints.violates(s,a)}")

if __name__ == "__main__":
    main()
