with open("image.png.enc", "rb") as f:
    F = f.read()

header = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,
        0, 0, 0, 0x0D, ord("I"), ord("H"), ord("D"), ord("R")]
for i in range(len(header)):
    header[i] ^= F[i]

arr = [-1]*16
idx = list(range(16))
ans = [0]*16
i, j = 0, 0
def f(p):
    global i, j
    if p == len(header):
        print("found!")
        for k in range(16):
            ans[idx[k]] = arr[k]
        return
    _i, _j = i, j
    i = (_i + 1) % 16
    if arr[i] != -1:
        j = (_j + arr[i]) % 16
        x = arr[j]
        if arr[j] != -1:
            if arr[j] != header[p] ^ arr[i]:
                i, j = _i, _j
                return
        else:
            arr[j] = header[p] ^ arr[i]
        arr[i], arr[j] = arr[j], arr[i]
        idx[i], idx[j] = idx[j], idx[i]
        f(p+1)
        arr[i], arr[j] = arr[j], arr[i]
        idx[i], idx[j] = idx[j], idx[i]
        arr[j] = x
        i, j = _i, _j
        return


    for k in range(16):
        if k in arr:
            continue
        arr[i] = k
        j = (_j + k) % 16
        if i == j:
            if header[p] == 0:
                f(p+1)
            continue
        
        x = arr[j]
        if arr[j] != -1:
            if arr[j] != header[p] ^ k:
                continue
        else:
            arr[j] = header[p] ^ k
        arr[i], arr[j] = arr[j], arr[i]
        idx[i], idx[j] = idx[j], idx[i]
        f(p+1)
        arr[i], arr[j] = arr[j], arr[i]
        idx[i], idx[j] = idx[j], idx[i]
        arr[j] = x
    
    arr[i] = -1
    i, j = _i, _j
    return
f(0)
print(ans)
def stream():
    i, j = 0, 0
    #S = list(range(16))
    #random.shuffle(S)

    while True:
        i = (i + 1) % 16
        j = (j + S[i]) % 16
        S[i], S[j] = S[j], S[i]

        yield S[i] ^ S[j]

S = ans
with open("image.png", "wb") as f:
    for a, b in zip(F, stream()):
        f.write(bytes([a ^ b]))
