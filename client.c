#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include "serv_cli_fifo.h"
#include "Handlers_Cli.h"

int main(int argc, char *argv[])
{
	/*initialisation du générateur de nombres aléatoires*/
	srand(getpid());
	/* Déclarations */
	int ppid, pid = getpid(),question = rand() % 100,reponse[question],fdread2,fdwrite2,i,fdwrite;

	

	/* Installation des Handlers */
	void hand_reveil(int sig)
	{
		/* Lecture du reponse */
		/* Ouverture du tube fifo1 en lecture */
		fdread2 = open(FIFO2, O_RDONLY);
		/* Message */
		printf("Reponse: [ ");
		/* Traitement local de la réponse */
		for (i = 0; i < question; i++)
		{
			read(fdread2, &reponse[i], sizeof(int));
			printf(" %d ", reponse[i]);
		};

		printf("]\n");
		/* Fermeture du tube fifo1 en lecture */
		close(fdread2);
		/* Fermeture du server par l'envoi du signal SIGUSR2 */
		// kill(ppid,SIGUSR2);
	}

	/* retrieving l'id du processus server pour
	 etre utiliser par le client a partir du fifo2 */
	/* Ouverture du tube fifo2 en lecture */
	fdread2 = open(FIFO2, O_RDONLY);
	read(fdread2, &ppid, sizeof(int));
	/* Fermeture du tube fifo2 en lecture */
	close(fdread2);

	/* enregistrer l'id du processus client pour etre 
	utiliser par le server dans fifo2 */
	/* Ouverture du tube fifo2 en ecriture */
	fdwrite2 = open(FIFO2, O_WRONLY);
	write(fdwrite2, &pid, sizeof(int));
	/* Fermeture du tube fifo2 en ecriture */
	close(fdwrite2);
	
	/* Initialisation du signal */
	signal(SIGUSR1, hand_reveil);
	/* timeout pour affecter le traitment au signal */
	sleep(1);
	/* Envoi du signal SIGUSR1 au serveur */
	kill(ppid, SIGUSR1);
	/* Ouverture du tube fifo1 en ecriture */
	fdwrite = open(FIFO1, O_WRONLY);
	/* Envoi d’une question */
	write(fdwrite, &question, sizeof(int));
	/* Fermeture du tube fifo1 en ecriture */
	close(fdwrite);

	pause();

	return 0;
}
