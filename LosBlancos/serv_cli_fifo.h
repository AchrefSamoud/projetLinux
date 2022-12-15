#include <stdio.h>
#include <stdlib.h>
#define NMIN 1
#define NMAX 20
#define fifo1 "fifo1" 
#define fifo2 "fifo2" 

typedef struct question {
	int cpid;
	int number;
} question;

typedef struct reponse {
	int spid;
	int result[NMAX];
} reponse ;


