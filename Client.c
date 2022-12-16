#include "serv_cli_fifo.h"
#include "Handlers_cli.h"
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>



void hand_reveil(int sig)
{
	printf("\n\n ------------------	Client Wake up	----------------\n\n");
}

int main ()
{
	printf("\n\n ------------------	Client Activated ----------------\n\n");

	/*		Declarations		*/

	/*			Request 			*/
	question request; 
	/*			Response	 		*/
	reponse response; 

	int mk1= open(fifo1, O_WRONLY);
	int mk2= open(fifo2, O_RDONLY);

	/*		Random Number Generator		*/
	srand(getpid());
	
	/*			Opening of named pipes		*/
	if (mk1<0)
		{
		
		fprintf(stderr, "\n 		!!!!!!	 Erreur of creating FIFO1 	!!!!!!  	\n");
		exit(EXIT_FAILURE);
		
		}
	if (mk2<0)
		{
		
		fprintf(stderr, "\n 		!!!!!!	 Erreur of creating FIFO2 	!!!!!!  	\n");
		exit(EXIT_FAILURE);
		
		}
	
	/*			Installing Handlers				*/
	signal(SIGUSR1,hand_reveil);
	
	/*		Sending Request		*/
	request.cpid=getpid();
	request.number=rand() % (NMAX - NMIN + 1) + NMIN;  
	printf("\n 	PID of Client -------------->  %d \n",request.cpid);
	printf("\n 	Choosing Number ------------>  %d \n",request.number);
	FILE *fp;
        char res[100];
        char int_str[100];
        char int_str2[100];
        sprintf(int_str,"%d",request.cpid);
        char str[] = "PID of Client --------------> ";
        strcat(str,int_str);
        strcat(str,"\n");
        char str2[] = "\n Choosing Number ------------> ";
        sprintf(int_str2,"%d",request.number);
        strcat(str2,int_str);
        strcat(str2,"\n");
        strcat(str,str2);
          
	write(mk1,&request,sizeof(question));

	close(mk1);
	
	/*		Waiting		*/
	pause();
	
	/*		Reading Server Response		*/
	read(mk2,&response,sizeof(reponse));
	close(mk2);
	
	printf("\n-------------	 All Received ! ^_^	------------\n");
	
	/*		Send SIGUSR1 signal		*/
	sleep(1);	
	kill(response.spid, SIGUSR1);
	
	/*		Local response Traitement		*/
	printf("\n 	PID of Server -------------->  %d \n",response.spid);
	printf("\n 	Random Number generated ---> \t");

		for (int i=0;i<request.number;i++)
		{

			printf("%d\t",response.result[i]);
			char int_str3[100];
			sprintf(int_str3,"%d",response.result[i]);
			strcat(str,int_str3);
            strcat(str,"\n");
		}
		strcat(str,"\t");
		fp = fopen("client.txt","w");
		printf("%s",str);
           int j=0;
           while(1){
          if (str[j]=='\t') break;
          else{
            fputc(str[j],fp);
            j++;
          } 
        
        }
       
        fclose(fp);

    }
