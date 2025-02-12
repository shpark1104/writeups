from pwn import *
from tqdm import tqdm
import pickle
ans = {}
context.log_level = "error"
for i in tqdm(range(256*256)):
    with open("/ctf/buf", "wb") as f:
        f.write(bytes([i//256, i%256,]))
        f.write(b"aa")

    r = process("./chall")#remote("host1.dreamhack.games", 16319)
    words = b""
    for _ in range(10):
        r.recvuntil(b"Type this word as soon as possible: ")
        word = r.recvline().strip()
        words += word
        r.sendlineafter(b"> ", word)
    ans_words = []
    for _ in range(10):
        r.recvuntil(b"Type this word as soon as possible: ")
        word = r.recvline().strip()
        ans_words.append(word)
        r.sendlineafter(b"> ", word)

    ans[words] = ans_words
    r.close()

with open("ans_dump", "wb") as f:
    pickle.dump(ans, f)