# learn.py
from __future__ import annotations
from typing import Iterable, Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import Counter
from core import (
    MDP, State, Action, Transition, FeatureVector, FeatureExtractor,
    Rule, Constraints
)

# ---------------- IRL (lightweight placeholder you can swap out) ----------------

def feature_count_profile(traj: Iterable[Transition], phi: FeatureExtractor) -> Dict[str, float]:
    """
    Very light 'IRL' signal: normalized counts of feature activations over demos.
    Replace with MaxEnt IRL, Bayesian IRL, or any library later.
    """
    c = Counter()
    total = 0.0
    for (s, a, s2) in traj:
        feats = phi(s, a)
        for k, v in feats.items():
            c[k] += float(v)
            total += abs(float(v))
    if total == 0:
        total = 1.0
    return {k: v / total for k, v in c.items()}

# ---------------- Positives / Negatives from trajectories ----------------

def positives_from_traj(traj: Iterable[Transition], phi: FeatureExtractor) -> List[FeatureVector]:
    return [phi(s, a) for (s, a, _) in traj]

def negatives_from_traj(
    mdp: MDP,
    traj: Iterable[Transition],
    phi: FeatureExtractor,
    deduplicate: bool = True,
    limit: int = 10_000
) -> Tuple[List[FeatureVector], List[FeatureVector]]:
    """
    Negatives = (s,a) pairs that were feasible in visited states but never taken in demos,
    identified by feature signature.
    """
    pos = positives_from_traj(traj, phi)
    pos_keys: Set[Tuple[Tuple[str, float], ...]] = {tuple(sorted(f.items())) for f in pos}

    negs: List[FeatureVector] = []
    seen = set()
    count = 0
    for (s, _, _) in traj:
        for alt in mdp.legal_actions(s):
            f = phi(s, alt)
            k = tuple(sorted(f.items()))
            if k not in pos_keys and (not deduplicate or k not in seen):
                negs.append(f)
                seen.add(k)
                count += 1
                if count >= limit:
                    return pos, negs
    return pos, negs

# ---------------- ILP-style rule learning over features ----------------

def make_threshold_rules(
    *,
    bool_keys: List[str] | None = None,
    le_thresholds: Dict[str, float] | None = None,
    ge_thresholds: Dict[str, float] | None = None,
) -> List[Rule]:
    """
    Generic rule space:
      - boolean literal:     not_allowed :- key.
      - numeric threshold:   not_allowed :- key <= t.
      - numeric threshold:   not_allowed :- key >= t.
    You provide which keys are boolean and (optionally) numeric thresholds to consider.
    """
    bool_keys = bool_keys or []
    le_thresholds = le_thresholds or {}
    ge_thresholds = ge_thresholds or {}

    rules: List[Rule] = []

    for k in bool_keys:
        rules.append(Rule(
            name=f"{k}_is_true",
            pretty=f"not_allowed(S,A) :- {k}.",
            predicate=lambda f, kk=k: f.get(kk, 0.0) >= 0.5
        ))

    for k, t in le_thresholds.items():
        rules.append(Rule(
            name=f"{k}_le_{t}",
            pretty=f"not_allowed(S,A) :- {k} <= {t}.",
            predicate=lambda f, kk=k, tt=t: f.get(kk, 0.0) <= tt
        ))

    for k, t in ge_thresholds.items():
        rules.append(Rule(
            name=f"{k}_ge_{t}",
            pretty=f"not_allowed(S,A) :- {k} >= {t}.",
            predicate=lambda f, kk=k, tt=t: f.get(kk, 0.0) >= tt
        ))

    return rules

def score_rule(rule: Rule, positives: List[FeatureVector], negatives: List[FeatureVector]) -> Tuple[int,int,int]:
    """
    TP = negatives correctly flagged as not-allowed
    FP = positives wrongly flagged (over-forbids)
    FN = negatives missed
    """
    TP = sum(1 for x in negatives if rule.covers(x))
    FP = sum(1 for x in positives if rule.covers(x))
    FN = len(negatives) - TP
    return TP, FP, FN

def select_best_rule(rules: List[Rule], positives: List[FeatureVector], negatives: List[FeatureVector]) -> Tuple[Rule, Tuple[int,int,int]]:
    """
    Pick one rule that best separates negatives from positives.
    (Extend to greedy multi-rule set cover if you want multiple constraints.)
    """
    best: Rule | None = None
    best_stats = (0,0,0)
    best_score = None
    for r in rules:
        TP, FP, FN = score_rule(r, positives, negatives)
        score = TP - 10*FP  # heavily penalize forbidding positive examples
        if best is None or score > best_score:
            best = r
            best_score = score
            best_stats = (TP, FP, FN)
    assert best is not None, "Rule space was empty."
    return best, best_stats

# ---------------- Learn constraints end-to-end ----------------

@dataclass
class LearnConfig:
    bool_feature_keys: List[str]
    le_thresholds: Dict[str, float] | None = None
    ge_thresholds: Dict[str, float] | None = None

@dataclass
class LearnResult:
    constraints: Constraints
    profile: Dict[str, float]
    best_rule_stats: Tuple[int,int,int]

def learn_constraints_from_trajectories(
    mdp: MDP,
    trajectories: Iterable[Iterable[Transition]],
    phi: FeatureExtractor,
    cfg: LearnConfig
) -> LearnResult:
    # Merge trajectories into one sequence
    merged: List[Transition] = [t for traj in trajectories for t in traj]

    # IRL-lite profile
    prof = feature_count_profile(merged, phi)

    # Positives / negatives
    pos, neg = negatives_from_traj(mdp, merged, phi)

    # Rule space + selection
    rulespace = make_threshold_rules(
        bool_keys=cfg.bool_feature_keys,
        le_thresholds=cfg.le_thresholds,
        ge_thresholds=cfg.ge_thresholds,
    )
    best_rule, stats = select_best_rule(rulespace, pos, neg)

    # Package constraints
    constraints = Constraints([best_rule], phi)
    return LearnResult(constraints=constraints, profile=prof, best_rule_stats=stats)
