#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <signal.h>

ssize_t 
recvall(int socket, void *buffer, size_t length) {
    size_t totalReceived = 0; // how many bytes we've received
    ssize_t bytesReceived;
    while (totalReceived < length) {
        bytesReceived = recv(socket, (char*)buffer + totalReceived, length - totalReceived, 0);
        if (bytesReceived == -1) { break; } // handle errors as you see fit
        if (bytesReceived == 0) { return totalReceived; } // Connection closed
        totalReceived += bytesReceived;
    }
    return bytesReceived == -1 ? -1 : totalReceived; // return -1 on failure, total on success
}

ssize_t 
sendall(int socket, const void *buffer, size_t length) {
    size_t totalSent = 0; // how many bytes we've sent
    ssize_t bytesSent;
    while (totalSent < length) {
        bytesSent = send(socket, (char*)buffer + totalSent, length - totalSent, 0);
        if (bytesSent == -1) { break; } // handle errors as you see fit
        totalSent += bytesSent;
    }
    return bytesSent == -1 ? -1 : totalSent; // return -1 on failure, total on success
}

// Error function used for reporting issues
void error(const char *msg) {
  perror(msg);
  exit(1);
} 

// Function to map characters to their numerical equivalents
int charToNum(char c) {
    if (c == ' ') return 26;
    else return c - 'A';
}

// Function to map numerical values back to characters
char numToChar(int num) {
    if (num == 26) return ' ';
    else return 'A' + num;
}

// The encryption function
char* encrypt(const char* plaintext, const char* key, size_t textLen) {
    char* ciphertext = malloc(textLen + 1);
    if (!ciphertext) exit(1);

    for (size_t i = 0; i < textLen; ++i) {
        int plainNum = charToNum(plaintext[i]);
        int keyNum = charToNum(key[i]);
        int cipherNum = (plainNum + keyNum) % 27;
        ciphertext[i] = numToChar(cipherNum);
    }

    ciphertext[textLen] = '\0';
    return ciphertext;
}

// The encryption function
char* 
decrypt(const char* ciphertext, const char* key, size_t textLen) {
    char* plaintext = malloc(textLen + 1);
    if (!plaintext) exit(1);

    for (size_t i = 0; i < textLen; ++i) {
        int cipherNum = charToNum(ciphertext[i]);
        int keyNum = charToNum(key[i]);
        int plainNum = (cipherNum - keyNum + 27) % 27; // +27 ensures a non-negative result
        plaintext[i] = numToChar(plainNum);
    }

    plaintext[textLen] = '\0';
    return plaintext;
}

// Set up the address struct for the server socket
void 
setupAddressStruct(struct sockaddr_in* address, 
                        int portNumber){
 
  // Clear out the address struct
  memset((char*) address, '\0', sizeof(*address)); 

  // The address should be network capable
  address->sin_family = AF_INET;
  // Store the port number
  address->sin_port = htons(portNumber);
  // Allow a client at any address to connect to this server
  address->sin_addr.s_addr = INADDR_ANY;
}

int main(int argc, char *argv[]){
  // Check usage & args
  if (argc < 2) { 
    fprintf(stderr,"USAGE: %s port\n", argv[0]); 
    exit(1);
  } 
  
  // Create the socket that will listen for connections
  int listenSocket = socket(AF_INET, SOCK_STREAM, 0);
  if (listenSocket < 0) {
    error("ERROR opening socket");
  }

  // Set up the address struct for the server socket
  struct sockaddr_in serverAddress;
  setupAddressStruct(&serverAddress, atoi(argv[1]));

  // Associate the socket to the port
  if (bind(listenSocket, 
          (struct sockaddr *)&serverAddress, 
          sizeof(serverAddress)) < 0){
    error("ERROR on binding");
  }

  // Start listening for connetions. Allow up to 5 connections to queue up
  listen(listenSocket, 5); 

  // Accept a connection, blocking if one is not available until one connects
  while(1){
    struct sockaddr_in clientAddress;
    socklen_t sizeOfClientInfo = sizeof(clientAddress);
    // Accept the connection request which creates a connection socket
    int connectionSocket = accept(listenSocket, 
                (struct sockaddr *)&clientAddress, 
                &sizeOfClientInfo); 
    if (connectionSocket < 0){
      error("ERROR on accept");
    }

    // Fork a new process to handle the connection
    pid_t spawnedPid = fork();
    if(spawnedPid == -1){
      error("ERROR on fork");
    }

    if(spawnedPid == 0){ // This is the child process
      // Close the listening socket in child process to clean up file descriptors
      close(listenSocket); 

      // Child process handling connection
      long inputTextLength, keyLength;
      recvall(connectionSocket, &inputTextLength, sizeof(inputTextLength));
      char* inputTextBuffer = malloc(inputTextLength + 1);
      recvall(connectionSocket, inputTextBuffer, inputTextLength);
      inputTextBuffer[inputTextLength] = '\0'; // Ensure null termination

      recvall(connectionSocket, &keyLength, sizeof(keyLength));
      char* keyBuffer = malloc(keyLength + 1);
      recvall(connectionSocket, keyBuffer, keyLength);
      keyBuffer[keyLength] = '\0';

      #ifdef DEC
        char* plaintext = decrypt(inputTextBuffer, keyBuffer, inputTextLength); 
        sendall(connectionSocket, plaintext, inputTextLength + 1);
      #else
        char* ciphertext = encrypt(inputTextBuffer, keyBuffer, inputTextLength);
        sendall(connectionSocket, ciphertext, inputTextLength + 1);
      #endif
      close(connectionSocket);
      free(inputTextBuffer);
      free(keyBuffer);
      exit(0); // Child process exits after handling connection
    } else {
      // Parent process closing the connection socket. It does not need it.
      close(connectionSocket); 
    }
  }

  // Close the listening socket
  close(listenSocket); 
  return 0;
}