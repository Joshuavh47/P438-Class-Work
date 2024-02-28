#include <stdio.h>
#include <string.h>

void send_http(char* host, char* msg, char* resp, size_t len);


/*
  Implement a program that takes a host, verb, and path and
  prints the contents of the response from the request
  represented by that request.
 */
int main(int argc, char* argv[]) {
  if (argc != 4) {
    printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
    return -1;
  }
  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];

  char response[10000];
  char request[10000];
  sprintf(request,"%s %s HTTP/1.0\r\nHost: %s\r\n\r\n",verb,path,host);
  //printf("%s %s",host,request);
  send_http(host,request,response,10000);
  
  printf("%s\n",response);
  
  return 0;
}
