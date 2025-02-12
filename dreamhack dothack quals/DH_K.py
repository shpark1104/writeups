from pwn import *
r = remote("host1.dreamhack.games", 23138)
outputs = []
mask = (1<<64) - 1
for _ in range(130):
    S = r.recvline().strip()
    x = eval(S.split()[1].decode())
    if x < 0:
        x = -x
        x = (x^mask) + 1
    outputs.append(x)

Z = []
mask = (1<<64)-1
for x in outputs:
    x = (x^(x>>32))*pow(0xdaba0b6eb09322e3, -1, 2**64)%(2**64)
    x = (x^(x>>32))*pow(0xdaba0b6eb09322e3, -1, 2**64)%(2**64)
    x = (x^(x>>32))
    Z.append(x)

for start_s in [0, 1]:
    X0 = []
    s = start_s
    for i in range(len(Z)):
        X0.append((Z[i]&1)^s)
        s ^= 1
    
    # bits[i] & (1<<j)
    def rotl(bitvec, n):
        return bitvec[-n:] + bitvec[:-n]
    def shiftl(bitvec, n):
        return [0]*n + bitvec[:-n]
    def xor(bitvec1, bitvec2):
        return [a^b for a, b in zip(bitvec1, bitvec2)]
    
    x0, x1 = [1<<i for i in range(64)], [1<<i for i in range(64, 128)]
    eq = []
    for i in range(len(outputs)):
        eq.append([x0[0], X0[i]])
        x1 = xor(x0, x1)
        x0 = rotl(x0, 24)
        x0 = xor(x0, xor(x1, shiftl(x1, 16)))
        x1 = rotl(x1, 37)
    
    for i in range(128):
        for j in range(i, len(eq)):
            if eq[j][0]&(1<<i):
                eq[j], eq[i] = eq[i], eq[j]
                break
        else:
            print("error!")
            exit(0)
        for j in range(i+1, len(eq)):
            if eq[j][0]&(1<<i):
                eq[j][0] ^= eq[i][0]
                eq[j][1] ^= eq[i][1]
        
    for i in range(127, -1, -1):
        for j in range(i):
            if eq[j][0] & (1<<i):
                eq[j][0] ^= eq[i][0]
                eq[j][1] ^= eq[i][1]
    
    for i in range(128, len(eq)):
        assert eq[i][0] == 0
        if eq[i][1] != 0:
            print("wrong")
            break
    else:
        x0, x1 = 0, 0
        for i in range(64):
            x0 += eq[i][1]<<i
                    
        for i in range(64):
            x1 += eq[i+64][1]<<i
        print(x0, x1)
        ans_x0, ans_x1 = x0, x1

def rotl(x, n):
    return (x<<n | x>>(64-n))&mask

x0, x1 = ans_x0, ans_x1
S = []
for i in range(len(outputs)):
    S.append((Z[i]-x0)%(2**64))
    x1 ^= x0
    x0 = rotl(x0, 24)
    x0 = (x0 ^ x1 ^ (x1<<16))&mask
    x1 = rotl(x1, 37)

M = 0xd1342543de82ef95
a = (S[1] - M*S[0])%(2**64)
for i in range(len(outputs)-1):
    assert (S[i+1] - M*S[i])%(2**64) == a

context.log_level = "debug"
for _ in range(50):
    S.append((S[-1]*M+a)%(2**64))
    ans = (S[-1]+x0)%(2**64)
    ans = (ans^(ans>>32))*0xdaba0b6eb09322e3%(2**64)
    ans = (ans^(ans>>32))*0xdaba0b6eb09322e3%(2**64)
    ans = (ans^(ans>>32))
    if ans & (1<<63):
        ans = ans & ((1<<63) - 1)
        ans ^= ((1<<63) - 1)
        ans += 1
        ans = -ans

    r.sendline(str(ans).encode())
    x1 ^= x0
    x0 = rotl(x0, 24)
    x0 = (x0 ^ x1 ^ (x1<<16))&mask
    x1 = rotl(x1, 37)

r.interactive()