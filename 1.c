#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <direct.h>  // For getcwd on Windows

// Function to trim newline from string
void trim_newline(char *str) {
    size_t len = strlen(str);
    if (len > 0 && str[len-1] == '\n') str[len-1] = '\0';
}

// Function to check if a command contains all words
int contains_all_words(const char *cmd, const char *words) {
    char cmd_copy[256];
    char words_copy[256];
    strcpy(cmd_copy, cmd);
    strcpy(words_copy, words);
    
    char *cmd_word = strtok(cmd_copy, " ");
    char *check_word = strtok(words_copy, " ");
    
    while (check_word != NULL) {
        int found = 0;
        char *temp_cmd = _strdup(cmd);
        char *temp_word = strtok(temp_cmd, " ");
        
        while (temp_word != NULL) {
            if (strcmp(temp_word, check_word) == 0) {
                found = 1;
                break;
            }
            temp_word = strtok(NULL, " ");
        }
        
        free(temp_cmd);
        if (!found) return 0;
        check_word = strtok(NULL, " ");
    }
    
    return 1;
}

// Function to map voice command to shell command
void execute_command(const char *cmd) {
    char command[512];
    
    // System information commands
    if (strstr(cmd, "system info") || strstr(cmd, "about")) {
        system("systeminfo");
    }
    // File and directory commands
    else if (strstr(cmd, "list") || strstr(cmd, "files")) {
        system("dir");
    }
    else if (strstr(cmd, "create directory") || strstr(cmd, "make folder")) {
        system("mkdir new_folder");
        printf("Created directory 'new_folder'\n");
    }
    // Time and date commands
    else if (strstr(cmd, "date") || strstr(cmd, "time")) {
        system("date /t && time /t");
    }
    else if (strstr(cmd, "calendar")) {
        time_t t = time(NULL);
        struct tm *tm = localtime(&t);
        char month[3];
        sprintf(month, "%d", tm->tm_mon + 1);
        sprintf(command, "cal %s", month);
        system(command);
    }
    // Network commands
    else if (strstr(cmd, "ip") || strstr(cmd, "network")) {
        system("ipconfig /all");
    }
    else if (strstr(cmd, "ping google")) {
        system("ping google.com -n 4");
    }
    else if (strstr(cmd, "network connections")) {
        system("netstat -an");
    }
    // System performance commands
    else if (strstr(cmd, "memory") || strstr(cmd, "ram")) {
        system("systeminfo | findstr \"Memory\"");
    }
    else if (strstr(cmd, "cpu") || strstr(cmd, "processor")) {
        system("wmic cpu get name, numberofcores, maxclockspeed");
    }
    else if (strstr(cmd, "disk") || strstr(cmd, "drive")) {
        system("wmic logicaldisk get size,freespace,caption");
    }
    // Process management
    else if (strstr(cmd, "processes") || strstr(cmd, "tasks")) {
        system("tasklist");
    }
    else if (strstr(cmd, "services")) {
        system("net start");
    }
    // Browser and applications
    else if (strstr(cmd, "open browser")) {
        system("start https://www.google.com");
    }
    else if (strstr(cmd, "open notepad")) {
        system("start notepad");
    }
    else if (strstr(cmd, "open calculator")) {
        system("calc");
    }
    // System controls
    else if (strstr(cmd, "clear") || strstr(cmd, "cls")) {
        system("cls");
    }
    // Volume control using PowerShell
    else if (strstr(cmd, "volume up")) {
        system("powershell -c \"(New-Object -ComObject WScript.Shell).SendKeys([char]175)\"");
    }
    else if (strstr(cmd, "volume down")) {
        system("powershell -c \"(New-Object -ComObject WScript.Shell).SendKeys([char]174)\"");
    }
    // User information
    else if (strstr(cmd, "whoami")) {
        system("whoami");
    }
    else if (strstr(cmd, "user info")) {
        system("net user %username%");
    }
    // Search commands
    else if (strstr(cmd, "search")) {
        char query[512] = {0};
        char url[1024] = {0};
        char *search_term = strstr(cmd, "search");
        
        if (search_term) {
            search_term += 6; // Skip "search"
            while (*search_term == ' ') search_term++; // Skip spaces
            
            if (*search_term != '\0') {
                // Copy the search term and clean it
                strcpy(query, search_term);
                
                // Replace spaces with '+' for URL encoding
                for (int i = 0; query[i]; i++) {
                    if (query[i] == ' ') query[i] = '+';
                }
                
                // Check for specific search types
                if (strstr(cmd, "song") || strstr(cmd, "music")) {
                    // Remove "song" or "music" from the query
                    char *song_term = strstr(query, "song");
                    if (song_term) {
                        *song_term = '\0';
                        strcat(query, song_term + 4);
                    }
                    song_term = strstr(query, "music");
                    if (song_term) {
                        *song_term = '\0';
                        strcat(query, song_term + 5);
                    }
                    sprintf(url, "start https://www.youtube.com/results?search_query=%s", query);
                    printf("Searching for song: %s\n", query);
                }
                else if (strstr(cmd, "movie") || strstr(cmd, "film")) {
                    // Remove "movie" or "film" from the query
                    char *movie_term = strstr(query, "movie");
                    if (movie_term) {
                        *movie_term = '\0';
                        strcat(query, movie_term + 5);
                    }
                    movie_term = strstr(query, "film");
                    if (movie_term) {
                        *movie_term = '\0';
                        strcat(query, movie_term + 4);
                    }
                    sprintf(url, "start https://www.imdb.com/find?q=%s", query);
                    printf("Searching for movie: %s\n", query);
                }
                else if (strstr(cmd, "youtube") || strstr(cmd, "yt")) {
                    sprintf(url, "start https://www.youtube.com");
                    printf("Opening YouTube\n");
                }
                else if (strstr(cmd, "netflix")) {
                    sprintf(url, "start https://www.netflix.com");
                    printf("Opening Netflix\n");
                }
                else if (strstr(cmd, "spotify")) {
                    sprintf(url, "start https://open.spotify.com");
                    printf("Opening Spotify\n");
                }
                else {
                    // Default to Google search
                    sprintf(url, "start https://www.google.com/search?q=%s", query);
                    printf("Searching for: %s\n", query);
                }
                
                // Execute the search command
                if (strlen(url) > 0) {
                    system(url);
                } else {
                    printf("Error: Could not generate search URL\n");
                }
            } else {
                printf("Please specify what you want to search for.\n");
                printf("Examples:\n");
                printf("  - search song Shape of You\n");
                printf("  - search movie Inception\n");
                printf("  - search youtube\n");
                printf("  - search netflix\n");
                printf("  - search spotify\n");
                printf("  - search how to make pasta\n");
            }
        }
    }
    // Help and unknown commands
    else if (strstr(cmd, "help") || strstr(cmd, "commands")) {
        printf("\nAvailable commands:\n");
        printf("System Information:\n");
        printf("  - system info, about\n");
        printf("  - memory, ram\n");
        printf("  - cpu, processor\n");
        printf("  - disk, drive\n\n");
        printf("File Operations:\n");
        printf("  - list files\n");
        printf("  - create directory, make folder\n\n");
        printf("Time and Date:\n");
        printf("  - date, time\n");
        printf("  - calendar\n\n");
        printf("Network:\n");
        printf("  - ip, network\n");
        printf("  - ping google\n");
        printf("  - network connections\n\n");
        printf("Applications:\n");
        printf("  - open browser\n");
        printf("  - open notepad\n");
        printf("  - open calculator\n\n");
        printf("System Control:\n");
        printf("  - clear, cls\n");
        printf("  - volume up\n");
        printf("  - volume down\n\n");
        printf("Search Commands:\n");
        printf("  - search [query]\n\n");
        printf("User Info:\n");
        printf("  - whoami\n");
        printf("  - user info\n");
    }
    else {
        printf("Command not recognized: %s\n", cmd);
        printf("Say 'help' or 'commands' to see available commands.\n");
    }
}

int main() {
    char buffer[256];
    FILE *fp;
    char python_cmd[512];
    char current_dir[256];

    printf("Voice Command System\n");
    printf("Say 'help' or 'commands' to see available commands\n");
    printf("Type 'exit' to quit\n\n");

    // Get current directory
    if (getcwd(current_dir, sizeof(current_dir)) == NULL) {
        fprintf(stderr, "Failed to get current directory\n");
        return 1;
    }

    // Construct the Python command with full path
    sprintf(python_cmd, "python \"%s\\1.py\"", current_dir);
    
    while (1) {
        printf("Listening...\n");
        
        // Call Python script and read its output
        fp = popen(python_cmd, "r");
        if (fp == NULL) {
            fprintf(stderr, "Failed to run Python recognizer. Make sure Python and required packages are installed.\n");
            return 1;
        }

        // Read output from Python
        if (fgets(buffer, sizeof(buffer), fp) != NULL) {
            trim_newline(buffer);
            printf("Recognized: '%s'\n", buffer);
            
            // Check for exit command
            if (strcmp(buffer, "exit") == 0) {
                printf("Goodbye!\n");
                pclose(fp);
                break;
            }
            
            execute_command(buffer);
        } else {
            printf("No output from recognizer.\n");
        }

        pclose(fp);
        printf("\n");
    }

    return 0;
}