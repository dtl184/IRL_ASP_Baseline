% --- Background Knowledge (B) ---
% Facts and rules defining the environment that ILASP can use.

disk(d1). disk(d2). disk(d3).
peg(p1). peg(p2). peg(p3).

% Disks 1 (smallest) < 2 < 3 (largest)
smaller_than(d1, d2).
smaller_than(d2, d3).
smaller_than(d1, d3).

% Helper definition for the inverse mapping (if needed, otherwise rely on direct facts)
% You can add rules here, e.g., 'larger_than(D1, D2) :- smaller_than(D2, D1).'

% --- Language Bias (M) (Search Space Definition) ---
% This defines the structure of the learned rule (H).

#modeh(1, constraint_violation(disk, peg, peg)). % The head predicate
#modeb(1, at(disk, peg)).                     % State fact: disk is on peg
#modeb(1, on_top(disk, peg)).                 % State fact: disk is on top of peg
#modeb(1, smaller_than(disk, disk)).           % Background relation: size comparison
#modeb(1, move(peg, peg)).                    % Action predicate

% The expected rule H to be induced is the Tower of Hanoi constraint:
% constraint_violation(D_move, P_from, P_to) :-
%   at(D_larger, P_to), 
%   smaller_than(D_move, D_larger). 
% (i.e., you are trying to move D_move onto P_to, but D_larger is already there and is smaller than D_move).

% --- Predicate Definitions for Examples ---
#max_body(3). % Max number of predicates in the rule body

% Define the structure of the hypothesis H
#external(pos(id, state_facts, action)).
#external(neg(id, state_facts, action)).