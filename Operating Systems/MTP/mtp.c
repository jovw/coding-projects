#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <err.h>
#include <errno.h>
#include <sys/types.h>
#include <pthread.h>
#include <unistd.h>
#include <stdbool.h>
#include <ctype.h>

// Macros
#define STOP_COMMAND "STOP\n"
#define STOP_CHAR '\3'
#define STOP_STR "\3"
#define NUM_LINES 50
#define SIZE 1000
#define NUM_THREADS 4

// Buffer Structure
struct buffer 
{
    char buffer[NUM_LINES][SIZE];
    pthread_mutex_t mutex;
    pthread_cond_t is_full;
};

// Global variables to hold the pipeline buffers
struct buffer *buffer1, *buffer2, *buffer3, *buffer4; // Mutex for synchronizing access to the buffer
struct buffer* buffers[NUM_THREADS];

// Initialize the global pipeline buffers
void 
init_buffers(void) {
    // Allocate memory for each buffer and initialize mutex and condition variables
    buffer1 = calloc(1, sizeof(struct buffer));
    buffer2 = calloc(1, sizeof(struct buffer));
    buffer3 = calloc(1, sizeof(struct buffer));
    buffer4 = calloc(1, sizeof(struct buffer));
    buffers[0] = buffer1;
    buffers[1] = buffer2;
    buffers[2] = buffer3;
    buffers[3] = buffer4;

    for (int i = 0; i < NUM_THREADS; i++) {
        memset(buffers[i]->buffer, 0, sizeof(char) * NUM_LINES * SIZE);
        buffers[i]->mutex = (pthread_mutex_t)PTHREAD_MUTEX_INITIALIZER;
        buffers[i]->is_full = (pthread_cond_t)PTHREAD_COND_INITIALIZER;
    }
}

// Write a line to a specified buffer
void
write_buffer(struct buffer* buffer, int line, char input[]) {
    pthread_mutex_lock(&buffer->mutex); // Lock
    strcpy(buffer->buffer[line], input); // Copy input to buffer
    pthread_cond_signal(&buffer->is_full); // signal waiting thread
    pthread_mutex_unlock(&buffer->mutex); // unlock
};

// read a line from a specific buffer
void
read_buffer(struct buffer* buffer, int line, char output[])
{
    ssize_t line_length = strlen(buffer->buffer[line]);
    pthread_mutex_lock(&buffer->mutex); // lock
    while (line_length == 0)
    {
        pthread_cond_wait(&buffer->is_full, &buffer->mutex); // wait to be non-empty
        line_length = strlen(buffer->buffer[line]);
    }
    strcpy(output, buffer->buffer[line]); //copy to output
    pthread_mutex_unlock(&buffer->mutex); // unlock
}

// cleanup to free allocated memory
void
cleanup_buffers(void) {
    for (int i = 0; i < NUM_THREADS; i++) {
        free(buffers[i]); // free each
    }
}

// input thread
// read form stdin
void* 
input_thread(void* args) {    
    bool running = true;
    char input[SIZE] = {0}; 
    int buffer_line = 0;

    while(running && buffer_line < NUM_LINES) { 
        if (fgets(input, SIZE, stdin) == NULL) {
            if (feof(stdin)) { // Check for EOF
                running = false;
                input[0] = STOP_CHAR; // termination
                input[1] = '\0'; 
            } else {
                perror("Error reading from stdin");
                exit(EXIT_FAILURE);
            }
        }

        // Check for STOP command
        if (strncmp(input, STOP_COMMAND, strlen(STOP_COMMAND)) == 0) {
            running = false;
            input[0] = STOP_CHAR; // Use STOP_CHAR to indicate termination
            input[1] = '\0'; 
        }
        // Write the processed line to buffer1
        write_buffer(buffer1, buffer_line, input);

        buffer_line++; 
    }

    return NULL;
}

// line_separator function
void* 
line_separator_thread(void* args) {
    int buffer_line = 0;
    char input[SIZE] = {0};

    while (true) {
        // Read the line from buffer1
        pthread_mutex_lock(&buffer1->mutex);
        while (strlen(buffer1->buffer[buffer_line % NUM_LINES]) == 0) {
            pthread_cond_wait(&buffer1->is_full, &buffer1->mutex);
        }
        strcpy(input, buffer1->buffer[buffer_line % NUM_LINES]);
        buffer1->buffer[buffer_line % NUM_LINES][0] = '\0'; // clear line buffer
        pthread_mutex_unlock(&buffer1->mutex);

        // Check for the STOP signal
        if (strstr(input, STOP_STR) != NULL) {
            break; 
        }

        // Replace '\n' with ' ' directly
        for (int i = 0; input[i] != '\0'; i++) {
            if (input[i] == '\n') {
                input[i] = ' ';
            }
        }

        // Write the processed line to buffer2
        write_buffer(buffer2, buffer_line, input);

        buffer_line++; 
    }

    // Signal to the next thread that processing is complete, in case it's waiting for input
    write_buffer(buffer2, buffer_line, input);

    return NULL;
}

//replace plus sign function with caret
void* 
plus_sign_thread(void* args) {
    int buffer_line = 0;
    char input[SIZE];

    while (true) {
        // Read the line from buffer2
        pthread_mutex_lock(&buffer2->mutex);
        while (strlen(buffer2->buffer[buffer_line % NUM_LINES]) == 0) {
            pthread_cond_wait(&buffer2->is_full, &buffer2->mutex);
        }
        strcpy(input, buffer2->buffer[buffer_line % NUM_LINES]);
        buffer2->buffer[buffer_line % NUM_LINES][0] = '\0';
        pthread_mutex_unlock(&buffer2->mutex);

        // Check for STOP signal
        if (strstr(input, STOP_STR) != NULL) {
            break; 
        }

        // Replace "++" with "^" in place
        char *p = input;
        while (*p && *(p+1)) { 
            if (*p == '+' && *(p+1) == '+') {
                *p = '^';
                memmove(p + 1, p + 2, strlen(p + 2) + 1);
            } else {
                ++p; 
            }
        }
        // Write the processed line to buffer3
        write_buffer(buffer3, buffer_line, input);

        buffer_line++; 
    }

    // Signal termination to the next thread
    write_buffer(buffer3, buffer_line, input);

    return NULL;
}

// process output and print to stdout
void* 
output_thread(void* args) {
    char input[SIZE] = {0}; 
    char output[81] = {0}; // buffer output for 80 + terminate
    int outputIndex = 0; 

    int buffer_line = 0;
    bool running = true;

    while (running) {
        read_buffer(buffer3, buffer_line, input);

        if (strstr(input, STOP_STR) != NULL) {
            break; 
        }

        for (int inputIndex = 0; input[inputIndex] != '\0'; ++inputIndex) {
            output[outputIndex++] = input[inputIndex];
            if (outputIndex == 80) { 
                output[outputIndex] = '\0'; 
                printf("%s\n", output);
                fflush(stdout);
                outputIndex = 0; 
            }
        }

        buffer_line++;
    }
    return NULL;
}

int main(void) {
    // Set up global pipeline buffers
    init_buffers();
    
    // Create variables for thread IDs
    pthread_t input_t, separator_t, plus_sign_t, output_t;

    // Create Pipeline Threads
    pthread_create(&input_t, NULL, input_thread, NULL);
    pthread_create(&separator_t, NULL, line_separator_thread, NULL);
    pthread_create(&plus_sign_t, NULL, plus_sign_thread, NULL);
    pthread_create(&output_t, NULL, output_thread, NULL);

    // Wait for threads to finish executing
    pthread_join(input_t, NULL);
    pthread_join(separator_t, NULL);
    pthread_join(plus_sign_t, NULL);
    pthread_join(output_t, NULL);

    // Deallocate memory used for global pipeline buffers
    cleanup_buffers();

    return 0;
}

