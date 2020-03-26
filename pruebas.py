
dic1 = {1:2,2:3,33:4}
dic2 = {1:1, 2:3 , 3:5}
dic3 = {1:1, 2:3 , 3:5}

def dict_zip(*dicts):
    all_keys = {k for d in dicts for k in d.keys()}
    return {k: [d[k] for d in dicts if k in d] for k in all_keys}

a = dict_zip(dic1,dic2,dic3)
print(a)
print(a[1][0])
