#include <stdio.h>
#include <string.h>

int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);



/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  char* rcpt = argv[1];
  char* filepath = argv[2];
  char fileBuffer[1000];
  FILE* file;
  FILE* charCounter;
  
  int charCount=0;
  if((charCounter=fopen(filepath,"r"))==NULL){
    perror("File not found");
    return 0;
  }
  while(fgetc(charCounter)!=EOF){
    charCount++;
  }
  
  if(charCount>4096){
    perror("File is too large");
    return 0;
  }
  fclose(charCounter);
  
  
  if((file=fopen(filepath,"r"))==NULL){
    perror("File not found");
    return -1;
  }
  char inputTemp[10000];
  while(fgets(fileBuffer,1000,file)){
    strcat(inputTemp,fileBuffer);
  }
  
  char input[100000];
  
  //sprintf(input,"HELO iu.edu\r\nMAIL FROM:jeeres@iu.edu\r\nRCPT TO:%s\r\nDATA\n%s\r\n.\r\nQUIT\r\n\r\n",rcpt,inputTemp);

  int socket = connect_smtp("lunar.open.sice.indiana.edu", 25);
  char response[100000];
  memset(response,'\0',10000);
  //send_smtp(socket, input, response, 10000);
  send_smtp(socket,"HELO iu.edu\r\n",response,10000);
  printf("%s\n", response);
  memset(response,'\0',10000);
  char temp[1000];
  sprintf(temp,"MAIL FROM:%s\r\n",rcpt);
  send_smtp(socket,temp,response,10000);
  printf("%s\n", response);
  memset(response,'\0',10000);
  char to[1000];
  strcat(to,"RCPT TO:");
  strcat(to,rcpt);
  strcat(to,"\r\n");
  send_smtp(socket,to,response,10000);
  printf("%s\n", response);
  memset(response,'\0',10000);
  //send_smtp(socket,"DATA\r\n",response,10000);
  //printf("%s\n", response);
  strcat(input,"DATA\r\n\r\n");
  
  strcat(inputTemp,"\r\n.\r\n\r\n");
  strcat(input,inputTemp);
  send_smtp(socket,input,response,10000);
  printf("%s\n", response);
  memset(response,'\0',10000);
  send_smtp(socket,"QUIT\r\n\r\n",response,10000);
  int white=9999;
  while(response[white]=='\0'||response[white]=='\n'||response[white]=='\r'){
    white--;
  }
  
  for(int i=white+1;i<9999;i++){
    response[i]='\0';
  }
  printf("%s\n", response);
  memset(response,'\0',10000);

  //printf("%s\n",input);
  fclose(file);
  
  
  return 0;
}
