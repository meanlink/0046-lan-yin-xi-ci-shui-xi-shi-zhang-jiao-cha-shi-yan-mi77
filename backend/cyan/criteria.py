def eligible(gain,p,fade,limit):
    return gain>=.04 and p<=.05 and fade<=float(limit)
