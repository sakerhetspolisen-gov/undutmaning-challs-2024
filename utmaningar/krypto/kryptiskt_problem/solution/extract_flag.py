req  = "716b4535dd8d3a9defb6c2740bd3199a74453a" 
resp = "04052140a9f677c8bce28e4560e06ac31b1047"

req = bytes.fromhex(req)
resp = bytes.fromhex(resp)

print(''.join([chr(a[0] ^ a[1]) for a in zip(req, resp)]))
