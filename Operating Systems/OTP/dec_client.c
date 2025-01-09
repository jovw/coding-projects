#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>  // ssize_t
#include <sys/socket.h> // send(),recv()
#include <netdb.h>      // gethostbyname()
#include <netinet/in.h>

/**
* Client code
* 1. Create a socket and connect to the server specified in the command arugments.
* 2. Prompt the user for input and send that input as a message to the server.
* 3. Print the message received from the server and exit the program.
*/

// Error function used for reporting issues
void error(const char *msg) { 
  perror(msg); 
  exit(0); 
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

// Set up the address struct
void setupAddressStruct(struct sockaddr_in* address, 
                        int portNumber){
 
  // Clear out the address struct
  memset((char*) address, '\0', sizeof(*address)); 

  // The address should be network capable
  address->sin_family = AF_INET;
  // Store the port number
  address->sin_port = htons(portNumber);

  // Get the DNS entry for this host name
  struct hostent* hostInfo = gethostbyname("localhost"); 
  if (hostInfo == NULL) { 
    fprintf(stderr, "CLIENT: ERROR, no such host\n"); 
    exit(0); 
  }
  // Copy the first IP address from the DNS entry to sin_addr.s_addr
  memcpy((char*) &address->sin_addr.s_addr, 
        hostInfo->h_addr_list[0],
        hostInfo->h_length);
}

// TODO: Your code does not currently validate the characters in the plaintext
int isValidCharacter(char c) {
  return (c >= 'A' && c <= 'Z') || c == ' ';
}

// and key files before attempting encryption
char* 
readFile(const char* filename, long* length) {
  FILE* file = fopen(filename, "r");
  if (!file) {
    fprintf(stderr, "Could not open file %s for reading\n", filename);
    exit(1);
  }

  fseek(file, 0, SEEK_END);
  *length = ftell(file);
  fseek(file, 0, SEEK_SET);

  char* buffer = malloc(*length);
  if (!buffer) {
    fprintf(stderr, "Failed to allocate memory for file\n");
    fclose(file);
    exit(1);
  }

  fread(buffer, 1, *length, file);
  
  // check for valid character
  for (long i = 0; i < *length; i++) {
    if (!isValidCharacter(buffer[i]) && buffer[i] != '\n') {
      fprintf(stderr, "Error: file '%s' contains invalid characters\n", filename);
      free(buffer);
      fclose(file);
      exit(1);
    }
  }

  if (buffer[*length - 1] == '\n') {
    buffer[*length - 1] = '\0';
    (*length)--;
  } else {
    buffer[*length] = '\0'; // If no newline, still ensure null-termination for safety
  }
  fclose(file);
  return buffer;
}


int main(int argc, char *argv[]) {
  // int socketFD, portNumber, charsWritten;

  // char buffer[256];
  // Check usage & args
  if (argc < 4) { 
    fprintf(stderr,"USAGE: %s ciphertext key port\n", argv[0]); 
    exit(1); 
  } 

  // Set up the server address struct
  int portNumber = atoi(argv[3]);
  struct sockaddr_in serverAddress;
  setupAddressStruct(&serverAddress, portNumber);

  // Create a socket
  int socketFD = socket(AF_INET, SOCK_STREAM, 0); 
  if (socketFD < 0){
    error("CLIENT: ERROR opening socket");
  }


  // Connect to server
  if (connect(socketFD, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0){
    error("CLIENT: ERROR connecting");
  }

  long ciphertextLength, keyLength;
  char* ciphertext = readFile(argv[1], &ciphertextLength); // Changed variable names for clarity
  char* key = readFile(argv[2], &keyLength);

//   if (keyLength < plaintextLength) {
//     fprintf(stderr, "Error: key '%s' is too short\n", argv[2]);
//     // free allocated memory
//     free(plaintext);
//     free(key);
//     exit(1);
//   }
  
  // Send lengths and data
  sendall(socketFD, &ciphertextLength, sizeof(ciphertextLength));
  sendall(socketFD, ciphertext, ciphertextLength);
  sendall(socketFD, &keyLength, sizeof(keyLength));
  sendall(socketFD, key, keyLength);

  // charsWritten = send(socketFD, plaintext, strlen(plaintext), 0);
  // send(socketFD, key, strlen(key), 0);
  // if (charsWritten < 0) error ("CLIENT: ERROR writing to socket");
  // if (charsWritten < strlen(plaintext)) printf("CLIENT: WARNING: Not all data written to socket!\n");

  // Wait for and print received plaintext
  char plaintextBuffer[ciphertextLength + 1]; 
  memset(plaintextBuffer, '\0', sizeof(plaintextBuffer));
  recv(socketFD, plaintextBuffer, sizeof(plaintextBuffer) - 1, 0);
  printf("%s\n", plaintextBuffer);

  // Close the socket
  free(ciphertext);
  free(key);
  close(socketFD); 
  return 0;
}
