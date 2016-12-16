pr = [pr[i][1] for i in xrange(0, precip.data)]

    consecutive_dry = [1 if pr.data < 1 else 0 for data in pr]

    for i in xrange(1,len(consecutive_dry)):

    if consecutive_dry[i] == 1:

    consecutive_dry[i] += consecutive_dry[i - 1]


    # set your day range here.

    day_range = 10


    for i in xrange (0,precip):

    if consecutive_wet[i] >= day_range:

    month_id = data[i,0]

    wet[month_id - 1] += 1


    print '10 Days Wet Spell\n', wet