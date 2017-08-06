def recur(x, s):
    if x == 1:
        return x

    if True:
        val = recur(x-1, s)
    else:
        val = recur(x-2, s)

    s += x + val

    recur(x-1, s)

    return s

print recur(10, 0)
