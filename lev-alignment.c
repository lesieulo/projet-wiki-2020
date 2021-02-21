#include <string.h>
#include <stdio.h>
#include <stdlib.h>

unsigned long s[100000];
unsigned long t[100000];

int main ()
{
    /*
    1. Lecture des fichiers (non vides) s1.uni et t1.uni, qui sont des fichiers d'une ligne,
        contenant des caractères sous forme d'entiers séparés par des espaces. Les entiers
        sont stockés dans les listes s et t. 
    2. Algorithme de Levenshtein avec un tableau des distances intermédiaires et un tableau
        pathMatrix contenant les opérations à chaque étape.
    3. "Alignement": réécriture des chaînes de caractères à partir de pathMatrix: les entiers
        sont réécris dans s2.uni et t2.uni à l'envers, la chaîne vide étant codée par -1.
    */

    unsigned long u = 0; //Caractère courant

    // Get string s as unicode integers
    long m = 0;
    FILE* s_file = fopen ("s1.uni", "r");
    while (!feof (s_file)){  
        if (fscanf (s_file, "%lu", &u)){
            s[m] = u;
            m++; 
        }
    }
    fclose (s_file);
    
    // Get string t as unicode integers
    long n = 0;
    FILE* t_file = fopen ("t1.uni", "r");
    while (!feof (t_file)){  
        if (fscanf (t_file, "%lu", &u)){
            t[n] = u;
            n++; 
        }
    }
    fclose (t_file);
    
    // Levenshtein algorithm
    long D[m+1][n+1];
    char pathMatrix[m][n];
    long i;
    long j;
    unsigned long s_char;
    unsigned long t_char;
    char operation;
    for (i=0; i<=m; i++)
        	D[i][0] = i;
    for (j=0; j<=n; j++)
        	D[0][j] = j;
    for (i=1; i<=m; i++){
        s_char = s[i-1];
        for (j=1; j<=n; j++) {
            int substitutionCost;
            t_char = t[j-1];
            if (s_char == t_char)
                substitutionCost = 0;
            else
                substitutionCost = 1;
            long deletion;
            long insertion;
            long substitution;
            long minimum;
            deletion = D[i-1][j] + 1;
            insertion = D[i][j-1] + 1;
            substitution = D[i-1][j-1] + substitutionCost;
            minimum = deletion;
            operation = 'D';
            if (insertion < minimum) {
                minimum = insertion;
                operation = 'I';
            }
            if (substitution < minimum) {
                minimum = substitution;
                operation = 'S';
            }
            D[i][j] = minimum;
            pathMatrix[i-1][j-1] = operation;
        }
    }
    
    // Test pathMatrix
    /*for (i=0; i<m; i++){
        for (j=0; j<n; j++){
            printf("%c", pathMatrix[i][j]);
        }
        printf("\n");    
    }*/

    // Alignment
    FILE* align_s_file = fopen ("s2.uni", "w");
    FILE* align_t_file = fopen ("t2.uni", "w");
    i = m-1;
    j = n-1;
    if (align_s_file != NULL && align_t_file != NULL){

        while (i>=0 || j>=0){
            if (i>=0 && j>=0){
                s_char = s[i];
                t_char = t[j];
                operation = pathMatrix[i][j];
            }
            else if (i<0){
                t_char = t[j];
                operation = 'I';
            }
            else if (j<0){
                s_char = s[i];
                operation = 'D';
            }
            //printf("\n%c %llu %llu", operation, s_char, t_char);
            if (operation=='S'){
                fprintf (align_s_file, "%lu ", s_char);
                fprintf (align_t_file, "%lu ", t_char);
                i--;
                j--;
            }
            else if (operation=='D'){
                fprintf (align_s_file, "%lu ", s_char);
                fprintf (align_t_file, "%d ", -1);
                i--;
            }
            else if (operation=='I'){
                fprintf (align_s_file, "%d ", -1);
                fprintf (align_t_file, "%lu ", t_char);
                j--;
            }
        }

    fclose (align_s_file);
    fclose (align_t_file);
    }
    
    return 0;
}