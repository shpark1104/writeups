import pickle
with open("ans_dump", "rb") as f:
    ans = pickle.load(f)
from pwn import *
r = remote("host1.dreamhack.games", 16319)
words = b""
for _ in range(10):
    r.recvuntil(b"Type this word as soon as possible: ")
    word = r.recvline().strip()
    words += word
    r.sendlineafter(b"> ", word)

print(words)
ans_words = ans[words]
for i in range(10):
    r.recvuntil(b"Type this word as soon as possible: ")
    r.sendlineafter(b"> ", ans_words[i])
r.interactive()