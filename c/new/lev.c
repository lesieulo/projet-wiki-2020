#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int levenshtein(const char * s, int m, const char * t, int n)
{
    int D[m+1][n+1];
    int i;
    int j;
    FILE* f_out = NULL;
    f_out = fopen("path.txt", "w");
    
    for (i=0; i<=m; i++){
        	D[i][0] = i;
    }
    for (j=0; j<=n; j++){
        	D[0][j] = j;
    }
    
    for (i=1; i<=m; i++) {
        char s_char;
            
        s_char = s[i-1];
        for (j=1; j<=n; j++) {
            char t_char;
            char operation;
            int substitutionCost;
            t_char = t[j-1];
            if (s_char == t_char) {
                substitutionCost = 0;
            }
            else {
                substitutionCost = 1;
            }
            int deletion;
            int insertion;
            int substitution;
            int minimum;
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
            fprintf (f_out, "%c", operation);
        }
        fprintf(f_out, "\n");
    }
    fclose(f_out);
    return 0;
}


int main ()
{
    const char * s;
    const char * t;
    int d;
    s = "le petit chat est là";
    t = "le petut chat esfeft à";
    int m;
    int n;
    m = 20;
    n = 22;
    d = levenshtein (s, m, t, n);
    
    
    
    
    /*FILE* fichier = NULL;
    fichier = fopen("test.txt", "w");
    if (fichier != NULL){
        fprintf(fichier,"mot %s de longueur %d", s, m);
        fprintf(fichier,"coucou\n");
        fclose(fichier); 
    }*/

    FILE* fichier = NULL;
    int length = 103;
    char mytext[length];
    fichier = fopen("test.txt", "r");
    char caractereActuel;
    int compteur = 0;
    int i;
    
    
    
    /*if (fichier != NULL)
    {
        do
        {
            caractereActuel = fgetc(fichier);
            printf("%c %d\n", caractereActuel, compteur);
            mytext[compteur] = caractereActuel;
            compteur++;
        } while (caractereActuel != EOF);
    }*/
    


    for (i=0; i<length; i++){
        caractereActuel = fgetc(fichier);
        printf("%c %d\n", caractereActuel, compteur);
        mytext[compteur] = caractereActuel;
        compteur++;
    }
    printf("\n\n\n%s", mytext);
    for (i=30; i<=35; i++){
        printf("\n%c", mytext[i]);
    }



    /* int compteur = 1;
    while (fgets(mytext, length, fichier) != NULL){
        printf("%s %d\n", mytext, compteur);
        compteur++;
    }*/
    
    
    
    fclose(fichier);
    return 0;
}







