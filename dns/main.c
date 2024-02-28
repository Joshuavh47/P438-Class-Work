#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <arpa/inet.h>

/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }
  char* host = argv[1];
  //long port = atoi(argv[2]);
  
  
  
  
  struct addrinfo hints, *res;
  memset(&hints,'\0',sizeof(hints));
  hints.ai_flags=AI_PASSIVE;
  hints.ai_family=PF_UNSPEC;
  hints.ai_socktype=SOCK_STREAM;
  hints.ai_protocol=IPPROTO_TCP;

  

  
  getaddrinfo(host, argv[2], &hints, &res);
  
  
 struct addrinfo *info;
 for(info=res; info!=NULL; info=info->ai_next){
   void* raw_addr;
   char str[INET6_ADDRSTRLEN];
   if (info->ai_family == AF_INET) { // Address is IPv4
     struct sockaddr_in* tmp = (struct sockaddr_in*)info->ai_addr; // Cast addr into AF_INET container
     raw_addr = &(tmp->sin_addr); // Extract the address from the container
     printf("IPv4 %s\n",inet_ntop(AF_INET, raw_addr, str, sizeof(str)));
   }
   else { // Address is IPv6
     struct sockaddr_in6* tmp = (struct sockaddr_in6*)info->ai_addr; // Cast addr into AF_INET6 container
     raw_addr = &(tmp->sin6_addr); // Extract the address from the container
     printf("IPv6 %s\n",inet_ntop(AF_INET6, raw_addr, str, sizeof(str)));
   }
 }

  return 0;
}
