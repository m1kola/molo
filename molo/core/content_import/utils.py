def conj(a, b):
    res = {}
    res.update(a)
    res.update(b)
    return res


def omit_nones(d):
    return dict((k, v) for k, v in d.iteritems() if v is not None)