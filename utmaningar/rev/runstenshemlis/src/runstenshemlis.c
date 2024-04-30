#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <debugapi.h>

char* readFile(const char*);
void modifyContent(const char*, char*, size_t);
unsigned int generateRandomHex();

int main() {
    const char* secretFile = "secret.txt";
    char* fileContent = readFile(secretFile);

    if (IsDebuggerPresent()){
        return 1;
    }

    if (fileContent == NULL){
        printf("Unable to read file '%s'. Press any key to exit...\n", secretFile);
        getchar();
        return 1;
    }

    size_t fileSize = strlen(fileContent);
    modifyContent(secretFile, fileContent, fileSize);
    free(fileContent);

    return 0;
}

char* readFile(const char* filename){
    FILE *filePointer;
    char *fileContent = NULL;
    long fileSize;
    size_t bytesRead;

    filePointer = fopen(filename, "rb");
    if (filePointer == NULL){
        perror("Error opening file");
        return NULL;
    }

    //Find the filesize.
    fseek(filePointer, 0, SEEK_END);
    fileSize = ftell(filePointer);
    rewind(filePointer);

    //Allocate memory for file content.
    fileContent = (char*)malloc((fileSize+1)*sizeof(char));
    if(fileContent == NULL){
        fclose(filePointer);
        perror("Memory allocation failed");
        return NULL;
    }

    //Read bytes into fileContent.
    bytesRead = fread(fileContent, sizeof(char), fileSize, filePointer);
    if(bytesRead != fileSize){
        free(fileContent);
        fclose(filePointer);
        perror("");
        return NULL;
    }

    //Adds a final EOF to the content.
    fileContent[fileSize] = '\0';
    fclose(filePointer);
    return fileContent;
}

void modifyContent(const char* filename, char* oldContent, size_t fileSize){
    FILE *filePointer;

    filePointer = fopen(filename, "wb");
    if (filePointer == NULL){
        perror("Error opening file");
        return;
    }

    unsigned int hexKeyOffset = generateRandomHex();
    fwrite(&hexKeyOffset, sizeof(char), 1, filePointer);

    for(int i = 0; oldContent[i] != '\0'; i++){
        oldContent[i] ^= ((hexKeyOffset + i) % 256);
    }

    fwrite(oldContent, sizeof(char), fileSize, filePointer);

    fclose(filePointer);
}

unsigned int generateRandomHex(){
    srand(time(NULL));
    return rand() % 0xFF;
}