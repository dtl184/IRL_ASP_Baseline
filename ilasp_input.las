% --- Background Knowledge ---
disk(0..2).
bigger_than(2, 1). 
bigger_than(1, 0). 
bigger_than(2, 0).

% --- Language Bias ---
#modeh(1, violation).

% We use the 'disk' type to ensure variables can be shared across all three predicates
#modeb(1, moving(var(disk)), (positive)).
#modeb(1, on_top_of(var(disk)), (positive)).
#modeb(1, bigger_than(var(disk), var(disk)), (positive)).

% Bias for 'nothing' case
#modeb(1, on_top_of(const(nothing))).

#constant(nothing, nothing).
#pos(c_0, {violation}, {}, { moving(1). on_top_of(0). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#pos(c_1, {violation}, {}, { moving(1). on_top_of(0). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#pos(c_2, {violation}, {}, { moving(1). on_top_of(0). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#pos(c_3, {violation}, {}, { moving(2). on_top_of(0). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#pos(c_4, {violation}, {}, { moving(2). on_top_of(0). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(2). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(nothing). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(1). on_top_of(2). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).
#neg(exp, {violation}, {}, { moving(0). on_top_of(1). disk(0). disk(1). disk(2). bigger_than(2,1). bigger_than(1,0). bigger_than(2,0). }).