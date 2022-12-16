#include "serv_cli_fifo.h"
#include "Handlers_serv.h"
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

void hand_reveil(int sig)
{
	printf("\n--------------------		Bingo ! All Received 	---------------------------\n");

	printf("\n--------------------		Another One ?	---------------------------\n");
}


void fin_serveur(int sig)
{	
	printf("\n\n----------------------		Good Bye !		-------------------------\n\n");
	exit(1);
}


int main ()
{
	printf("\n\n----------------------	Welcome to server	-------------------------\n\n");

	/*		Declarations		*/

	/*			Request 			*/
	question request;
	/*			Response	 		*/
	reponse response; 
	/*		Number Of Signal	*/
	int sig; 
	/*Cleaning of named pipes*/
	unlink (fifo1);
	unlink(fifo2);
	/**/
	int mk1=mkfifo(fifo1,S_IRUSR | S_IWUSR);
	/**/
	int mk2=mkfifo(fifo2,S_IRUSR | S_IWUSR);




	/*			Creation of named pipes			*/
	if (mk1<0)
		{
		
		fprintf(stderr, "\n 		!!!!!!	 Erreur of creating FIFO1 	!!!!!!  	\n");
		exit(EXIT_FAILURE);
		
		}
		
	if (mk2<0)
		{
		
		fprintf(stderr, "\n 		!!!!!! 	Erreur of creating FIFO2 	!!!!!! 		\n");
		exit(EXIT_FAILURE);
		
		}
	
	/*		Random Number Generator		*/
	srand(getpid());
	
	
	/*			Opening of named pipes		*/
	mk1= open(fifo1, O_RDWR);

	if (mk1<0)
		{

		fprintf(stderr, "\n 		!!!!!!	 Erreur Opening FIFO1	 !!!!!! 		\n");
		exit(EXIT_FAILURE);
		
		}
	mk2= open(fifo2, O_WRONLY);
	if (mk2<0)
		{
		
		fprintf(stderr, "\n 		!!!!!! 	Erreur Opening FIFO2 	!!!!!! 		\n");
		exit(EXIT_FAILURE);
		
		}
	
	
	/*			Installing Handlers				*/
	signal(SIGUSR1,hand_reveil);
	for (sig=1;sig<NSIG;sig++)
		if (sig!=SIGUSR1)
			signal(sig,fin_serveur);

	
	while (1)
	{
		/* 		Reading Client Request		*/
		read(mk1,&request,sizeof(question));
		printf("\n 	PID of Client -------------->  %d \n",request.cpid);
		printf("\n 	Choosing Number ------------>  %d \n",request.number);

		FILE *fp;
        char res[100];
        char int_str[100];
        sprintf(int_str,"%d",request.number);
        char str[] = "Choosed Number: ";
        strcat(str,int_str);
        strcat(str,"\n");
        /*		Traitement of Result		*/
		response.spid=getpid();
		printf("\n 	PID of Server -------------->  %d \n",response.spid);
		printf("\n 	Random Number generated --------------> \t");
		for (int i=0;i<request.number;i++)
		{

			response.result[i]=rand() % 1000;
			printf("%d\t",response.result[i]);
			sprintf(int_str,"%d",response.result[i]);
            strcat(str,int_str);
            strcat(str,"\n");
			
		}
			
		/*Envoi de la réponse*/
		write(mk2,&response,sizeof(reponse));
		printf("\n----------	All Sent ! ^_^	 ----------\n");
		
		printf("\n");
		strcat(str,"\t");
        fp = fopen("server.txt","w");
           int i=0;
           while(1){
          if (str[i]=='\t') break;
          else{
            fputc(str[i],fp);
            i++;
          } 
        
        }
       
        fclose(fp);
	
		/*		Send SIGUSR1 signal		*/
		sleep(1);
		kill(request.cpid,SIGUSR1);
        
		
	
	}
	/*		Closing of Named pipes	*/
	close(mk1);
	close(mk2);

}
