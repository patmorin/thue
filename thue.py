import sys
import random
from collections import defaultdict

def repetitive_suffix(s):
    """Return (half) the length of the shortest repetitive suffix in s"""
    for t in range(1, len(s)//2 + 1):
        if s[-2*t:-t] == s[-t:]:
            return t
    return 0


def gen_nonrep(sigma, r):
    """Generate all nonrepetitive strings of length r over the alphabet sigma"""
    for s in gen_nonrep_r([], sigma, r):
        yield s

def gen_nonrep_r(s, sigma, r):
    if r == 0:
        yield s
    else:
        for a in sigma:
            sa = s+[a]
            if repetitive_suffix(sa) == 0:
                for x in gen_nonrep_r(sa, sigma, r-1):
                    yield x

def blocked_repetitive_suffix(s, r):
    for i in range(r):
        ss = s[:len(s)-i]
        t = repetitive_suffix(ss)
        if  t > 0:
            return (t, len(s)-i)
    return (0, len(s))

if __name__ == "__main__":
    try:
        c = int(sys.argv[1])
        r = int(sys.argv[2])
    except:
        sys.stderr.write("Usage: {} <|sigma|> <r>\n".format(sys.argv[0]))
        sys.exit(-1)

    sigma = "abcdefghijklmnopqrstuvwxyz"[:c]
    blocks = list(gen_nonrep(sigma, r))

    digraph = [list() for x in blocks]
    dograph = [list() for x in blocks]
    for i in range(len(blocks)):
        for j in range(len(blocks)):
            (t, e) = blocked_repetitive_suffix(blocks[i] + blocks[j], r)
            if t == 0:
                dograph[i].append(j)
            else:
                digraph[i].append(j)

    # Some blocks can never be extended, make sure they are not included
    empty = [i for i in range(len(blocks)) if len(dograph[i]) == 0]
    while empty:
        for el in dograph:
            for i in empty:
                if i in el:
                    el.remove(i)
        empty = [i for i in range(len(blocks)) if len(dograph[i]) == 0]

    #print(digraph)
    for i in range(len(blocks)):
        pass # print(i, "".join(blocks[i]), len(digraph[i]))
    avgdeg = sum([len(digraph[i]) for i in range(len(blocks))]) / len(blocks)
    #print("Average degree = {} ({})".format(avgdeg, avgdeg/len(blocks)))

    lb = 0
    s = []
    it = 0

    hist = defaultdict(int)

    while 1 < 2:
        nb = random.choice(dograph[lb])
        sp = s + blocks[nb]
        (t, e) = blocked_repetitive_suffix(sp, r)
        if  t > 0:
            mid = e-t   # first element of second half
            #print("".join(sp), "".join(sp[e-2*t:e]))
            while mid < len(sp):
                sp = sp[:-r]
            #print("".join(sp))
            #sys.exit(-1)
        s = sp
        lb = nb
        it += 1
        print(it, len(s))
