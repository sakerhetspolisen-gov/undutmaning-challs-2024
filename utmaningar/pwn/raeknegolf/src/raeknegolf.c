#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/mman.h>
#include <time.h>

#define DIE(str) perror(str); exit(1);

#define NAME_MAX_LEN 0x10
#define CODE_MAX_LEN 0x1000 - NAME_MAX_LEN - 1

uint64_t v_rax, v_rbx, v_imm;

struct program {
    char name[NAME_MAX_LEN];
    char code[CODE_MAX_LEN];
};

struct prog_arg {
    char name[256];
    uint64_t val;
};

void alarmHandler(int pass) {
    puts("Tiden rann ut!");
    exit(1);
}

void setup() {
    struct sigaction act;
    act.sa_handler = alarmHandler;
    sigaction(SIGALRM, &act, NULL);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void print_banner(){
    printf(R"EOF(
           █ █
 ██████╗░░█████╗░██╗░░██╗███╗░░██╗███████╗░██████╗░░█████╗░██╗░░░░░███████╗
 ██╔══██╗██╔══██╗██║░██╔╝████╗░██║██╔════╝██╔════╝░██╔══██╗██║░░░░░██╔════╝
 ██████╔╝███████║█████═╝░██╔██╗██║█████╗░░██║░░██╗░██║░░██║██║░░░░░█████╗░░
 ██╔══██╗██╔══██║██╔═██╗░██║╚████║██╔══╝░░██║░░╚██╗██║░░██║██║░░░░░██╔══╝░░
 ██║░░██║██║░░██║██║░╚██╗██║░╚███║███████╗╚██████╔╝╚█████╔╝███████╗██║░░░░░
 ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝░╚═════╝░░╚════╝░╚══════╝╚═╝░░░░░

)EOF");
}

uint64_t run_program(struct program * p, struct prog_arg ** prog_args) {
    long a, b;
    for (int i = 0; i < 3; i++) {
        if (!strcmp(prog_args[i]->name, "rax")) {
            a = prog_args[i]->val; 
        } else if (!strcmp(prog_args[i]->name, "rax")) {
            b = prog_args[i]->val; 
        } 
    }
    uint64_t res;
    int (*func)() = (int (*)())p->code;

    asm ("mov %1, %%rbx\n"
         "mov %2, %%rax\n"
         "mov %3, %%rcx\n"
         "call %%rcx\n"
         "mov %%rax, %0\n"
     : "=r" (res)
     : "r" (b),
       "r" (a),
       "r" (func)
     : "%rax", "%rbx", "%rcx"
    );

    return res;
}

uint64_t get_correct_answer(uint64_t a, uint64_t b, uint64_t c) {
    return a + b -c;
}

struct prog_arg ** randomize_things() {
    struct prog_arg * rax_arg = malloc(sizeof(struct prog_arg));
    struct prog_arg * rbx_arg = malloc(sizeof(struct prog_arg));
    struct prog_arg * imm_arg = malloc(sizeof(struct prog_arg));
    struct prog_arg * v_args[3] = {rax_arg, rbx_arg, imm_arg};
    struct prog_arg ** prog_args = malloc(sizeof(struct prog_arg *) * 3);
    int idx;
    int r = 0;
    int i;

    for (i = 0; i < 3; i++) {
        prog_args[i] = NULL;
    }

    rax_arg->val = rand() % 1000000;
    strcpy(rax_arg->name, "rax");
    rbx_arg->val = rand() % 1000000;
    strcpy(rbx_arg->name, "rbx");
    imm_arg->val = rand() % 1000000;
    strcpy(imm_arg->name, "imm");

    idx = rand() % 3;
    for (int i = 0; i < 3; i++) {
        while(prog_args[idx]) {
            idx = rand() % 3;
        }
        prog_args[idx] = v_args[i];
    }

    return prog_args;
}

void print_rules(){
printf(R"EOF(
    Tillåtna register:         
                  rax, rbx
    Tillåtna instruktioner:
                  mov reg, reg
                  mov reg, immediate
                  add reg, reg
                  sub reg, reg
                  ret
)EOF");
}

void print_mission(struct prog_arg ** prog_args){
    char s_imm[256] = "\0";
    char * strings[3] = { NULL };

    char mission_statement[256] = {0};

    for (int i = 0; i < 3; i++) {
        if (!strcmp(prog_args[i]->name,"imm")){
            sprintf(s_imm, "0x%lx", prog_args[i]->val);
            strings[i] = s_imm;
        } else {
            strings[i] = prog_args[i]->name;
        }
    }
    printf("Skriv en funktion som returnerar %s + %s - %s\n", strings[0], strings[1], strings[2]);
}

void validate_program(uint8_t * code, size_t len) {
#define MOV_RAX_IMM 0x48c7c0
#define MOV_RBX_IMM 0x48c7c3
#define MOV_RAX_RAX 0x4889c0
#define MOV_RBX_RBX 0x4889db
#define MOV_RBX_RAX 0x4889d8
#define MOV_RAX_RBX 0x4889c3
#define ADD_RAX_RAX 0x4801c0
#define ADD_RBX_RBX 0x4801db
#define ADD_RBX_RAX 0x4801d8
#define ADD_RAX_RBX 0x4801c3
#define SUB_RAX_RAX 0x4829c0
#define SUB_RBX_RBX 0x4829db
#define SUB_RBX_RAX 0x4829d8
#define SUB_RAX_RBX 0x4829c3
#define RET         0xc3

    uint32_t opcode;

    size_t i = 0;
    while(i < len) {
        if (code[i] == 0xc3) {
            opcode = 0xc3;
        } else {
            opcode = (code[i] << 16) + (code[i+1] << 8) + code[i+2];
        }

        switch (opcode) {
            case MOV_RAX_IMM:
            case MOV_RBX_IMM:
                i += 7;
                break;
            case MOV_RAX_RAX:
            case MOV_RBX_RBX:
            case MOV_RBX_RAX:
            case MOV_RAX_RBX:
            case ADD_RAX_RAX:
            case ADD_RBX_RBX:
            case ADD_RBX_RAX:
            case ADD_RAX_RBX:
            case SUB_RAX_RAX:
            case SUB_RBX_RBX:
            case SUB_RBX_RAX:
            case SUB_RAX_RBX:
                i += 3;
                break;
            case RET:
                i += 1;
                break;
            default:
                puts("Ajabaja! Fusk är inte tillåtet!");
                exit(1);
        }
    }
}

int main() {
    ssize_t bytes_read;
    struct program * p;
    void * mem;
    struct prog_arg ** prog_args;
    long correct_ans, user_ans;

    srand(time(NULL));

    setup();
    alarm(60);
    print_banner();

    mem = mmap(NULL, 0x1000,
            PROT_READ | PROT_WRITE | PROT_EXEC,
            MAP_ANONYMOUS | MAP_PRIVATE,
            0,
            0);

    if (mem < 0) {
        DIE("mmap");
    }

    p = mem;

    prog_args = randomize_things();
    print_mission(prog_args);
    print_rules();
    printf("Kod: ");

    if ( (bytes_read = read(STDIN_FILENO, p->code, CODE_MAX_LEN)) == -1) {
        DIE("read");
    }

    if (bytes_read > 0 && p->code[bytes_read-1] == '\n') {
        bytes_read--;
    }
    p->code[bytes_read] = '\xc3';

    validate_program(p->code, bytes_read);

    printf("\nNamnge ditt program: ");
    if ( (bytes_read = read(STDIN_FILENO, p->name, NAME_MAX_LEN)) == -1){
        DIE("read");
    }

    p->name[bytes_read] = 0;

    correct_ans = get_correct_answer(prog_args[0]->val, prog_args[1]->val, prog_args[2]->val);

    printf("\nExekverar: %s\n", p->name);
    user_ans = run_program(p, prog_args);
      
    if (correct_ans == user_ans) {
        puts("Tack!");
    } else {
        printf("Fel! Det sökta svaret var 0x%lx\n", correct_ans);
        printf("    Fick felaktiga svaret 0x%lx\n", user_ans);

    }

    return 0;
}

