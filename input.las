% --- Background Knowledge ---
disk(1..3).
smaller(1, 2). smaller(1, 3). smaller(2, 3).

% --- Language Bias ---
#modeh(violation).

% The agent 'sees' which disk is moving and which is below
#modeb(1, moving_disk(var(disk)), (positive)).
#modeb(1, disk_below(var(disk)), (positive)).

% The agent 'reasons' about their relative size
#modeb(1, smaller(var(disk), var(disk)), (positive)).

% Handle the empty peg case as a constant
#modeb(1, disk_below(const(none))).
#constant(none, none).
#pos({violation}, {}, { moving_disk(3). disk_below(1). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(3). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(3). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(3). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(1). disk_below(3). }).
#neg({violation}, {}, { moving_disk(2). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).
#neg({violation}, {}, { moving_disk(3). disk_below(none). }).
#neg({violation}, {}, { moving_disk(1). disk_below(none). }).
#neg({violation}, {}, { moving_disk(2). disk_below(3). }).
#neg({violation}, {}, { moving_disk(1). disk_below(2). }).