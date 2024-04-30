#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <stdint.h>
#include <unistd.h>

#include <string.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <limits.h>

#include <sys/mman.h>

#define DIE(str) perror(str); exit(1);

#define FILENAME_MAX_LEN 0x40

void alarmHandler(int pass) {
    puts("\nTime is up!");
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

#define FILEPATH_MAX_LEN 0x40
#define BUF_SIZE 0x90
int validate_file_path(char* filepath) {
    char actual_path[PATH_MAX];
    char actual_path_flag[PATH_MAX];
    realpath(filepath, actual_path);
    realpath("./flag", actual_path_flag);
    return strcmp(actual_path, actual_path_flag);
}

void read_file() {
    // use a struct in order to control stack layout for CTF purposes
    struct {
        int32_t n_bytes;
        uint32_t bytes_read;
        int fd;
        char filepath[FILEPATH_MAX_LEN];
        char buf[BUF_SIZE];
    } locals;
    printf("Filename: ");   
    if ( (locals.bytes_read = read(STDIN_FILENO, locals.filepath, sizeof(locals.filepath) - 1)) == -1) {
        DIE("read");
    }

    if (locals.filepath[locals.bytes_read-1] == '\n')
        locals.filepath[locals.bytes_read-1] = 0;

    printf("nr of bytes: ");
    scanf("%u", &locals.n_bytes);

    if ( !validate_file_path(locals.filepath) )  {
        puts("not allowed");
        exit(1);
    }

    if (locals.n_bytes > BUF_SIZE) {
        puts("Too many");
        exit(1);
    }

    if ( (locals.fd = open(locals.filepath, O_RDONLY)) == -1) {
        DIE("open");
    }

    if ( (locals.bytes_read = read(locals.fd, locals.buf, locals.n_bytes)) == -1) {
        DIE("read");
    }

    write(STDOUT_FILENO, locals.buf, locals.bytes_read);
    printf("\nEOF %s\n", locals.filepath);
    
    close(locals.fd);

    return;
}

void read_mem() {
    char buf[0x200];
    long long addrl;
    char* addr;
    size_t n_bytes;
    printf("Addr: ");
    if ( (n_bytes = read(STDIN_FILENO, buf, sizeof(buf)-1)) == -1) {
        DIE("read");
    }
    if (buf[n_bytes-1] == '\n') {
        buf[n_bytes-1] = 0;
    }
    addrl = strtoll(buf, NULL, 16);
    addr = (char*)addrl;
    memset(buf, 0, sizeof(buf));
    memcpy(buf, addrl, sizeof(buf)-1);
    if (write(STDOUT_FILENO, buf, sizeof(buf)-1) == -1) {
        DIE("write");
    }
    puts("EOM");
    return;
}

void bloat_mem() {
    for (int i = 0 ; i < 50; i+=2) {
        if (mmap((0x10000000 + (0x1000*i)), 0x1000, 0, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0) == -1) {
            DIE("mmap");
        }
    }
    return;
}

int main() {
    char cmd[0x40000];
    memset(cmd, 0x0, 0x40000);
    ssize_t bytes_read;
    int choice;
    int debug_used = 0;
    setup();
    bloat_mem();
    alarm(60);

    while(1) {
        if (!debug_used) {
            printf("(1) Read file\n(2) [DEBUG] Read mem\nChoice: ");
        } else {
            printf("(1) Read file\nChoice: ");
        }
        if ( read(STDIN_FILENO, cmd, 2) == -1) {
            DIE("read");
        }
        choice = atoi(cmd);
        switch(choice) {
            case 1:
                read_file();
                break;
            case 2:
                if (!debug_used) {
                    debug_used = 1;
                    read_mem();
                    break;
                }
            default:
                puts("Invalid choice");
        }
    }

    return 0;
}
