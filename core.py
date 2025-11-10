from __future__ import annotations
from typing import Protocol, Iterable, Tuple, Hashable, Dict, List, Callable, Optional
from dataclasses import dataclass

# ---------- Generic types ----------
State  = Hashable     # Your state must be hashable (tuple/str/frozenset/...).
Action = Hashable     # Your action must be hashable (tuple/str/int/...).
Transition = Tuple[State, Action, State]
FeatureVector = Dict[str, float]

# ---------- Feature extraction ----------
class FeatureExtractor(Protocol):
    """Map (state, action) -> named feature vector (strings → numbers)."""
    def __call__(self, s: State, a: Action) -> FeatureVector: ...

# ---------- Constraints (logic-like rules over features) ----------
@dataclass(frozen=True)
class Rule:
    """
    A rule decides NOT-ALLOWED based on a feature vector.
    - `name`/`pretty` are for human readability.
    - `predicate` returns True iff the action violates this rule.

    For example, in Hanoi maybe a rule is that an action is prohibited if
    the destination is location B. This rule would be declared as follows:
    Rule(
        name="dst_is_B",
        pretty="not_allowed(S,A) :- dst_is_B.",
        predicate=lambda f: f.get("dst_is_B", 0) >= 0.5 <---- tests if rule is violated based on current state
    )
    """
    name: str
    pretty: str
    predicate: Callable[[FeatureVector], bool]

    def covers(self, f: FeatureVector) -> bool:
        return bool(self.predicate(f))

@dataclass
class Constraints:
    """A set of rules evaluated via a FeatureExtractor."""
    rules: List[Rule]
    phi: FeatureExtractor

    def violates(self, s: State, a: Action) -> bool:
        f = self.phi(s, a)
        return any(r.covers(f) for r in self.rules)

    def pretty(self) -> str:
        return "\n".join(r.pretty for r in self.rules)

# ---------- Generic MDP interface (domain pluggable) ----------
class MDP(Protocol):
    """
    Minimal API the rest of the system uses. Implement these 4 methods in your domain:
        - initial_state()
        - is_terminal(s)
        - legal_actions(s)
        - apply(s, a) -> s'
    And provide a `constraints` field for learned rules (filled during/after learning).
    """
    constraints: Constraints

    def initial_state(self) -> State: ...
    def is_terminal(self, s: State) -> bool: ...
    def legal_actions(self, s: State) -> Iterable[Action]: ...
    def apply(self, s: State, a: Action) -> State: ...

# ---------- Convenience container for in-memory trajectories ----------
@dataclass
class ListTrajectory:
    triples: List[Transition]
    def __iter__(self) -> Iterable[Transition]:
        return iter(self.triples)
