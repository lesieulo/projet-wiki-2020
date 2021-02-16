#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main ()
{
    unsigned long long u = 0;
        
    // Get string s as unicode integers
    unsigned long long s[10000];
    int m = 0;
    FILE* s_file = fopen ("s1.uni", "r");
    while (!feof (s_file)){  
        fscanf (s_file, "%llu", &u);
        s[m] = u;
        //printf ("%llu ", u);
        m++; 
    }
    fclose (s_file);
    
    //printf ("\n");
    
    // Get string t as unicode integers
    unsigned long long t[10000];
    int n = 0;
    FILE* t_file = fopen ("t1.uni", "r");
    while (!feof (t_file)){  
        fscanf (t_file, "%llu", &u);
        t[n] = u;
        //printf ("%llu ", u);
        n++; 
    }
    fclose (t_file);
    
    // Tests
    /*printf("\ncompteur s = %d", m);
    printf("\ncompteur t = %d", n);
    int ind;
    for (ind=1; ind<=n; ind++)
        printf ("\n %d %llu", ind-1, t[ind-1]);
    printf("\n");*/
    
    // Levenshtein algorithm
    int D[m+1][n+1];
    char pathMatrix[m][n];
    int i;
    int j;
    unsigned long long s_char;
    unsigned long long t_char;
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
    while (i>=0 && j>=0){
        s_char = s[i];
        t_char = t[j];
        operation = pathMatrix[i][j];
        //printf("\n%c %llu %llu", operation, s_char, t_char);
        if (operation=='S'){
            //printf ("\ns:%llu, t:%llu", s_char, t_char);
            fprintf (align_s_file, "%llu ", s_char);
            fprintf (align_t_file, "%llu ", t_char);
            i--;
            j--;
        }
        else if (operation=='D'){
            //printf ("\ns:%llu, t:%d", s_char, -1);
            fprintf (align_s_file, "%llu ", s_char);
            fprintf (align_t_file, "%d ", -1);
            i--;
        }
        else if (operation=='I'){
            //printf ("\ns:%d, t:%llu", -1, t_char);
            fprintf (align_s_file, "%d ", -1);
            fprintf (align_t_file, "%llu ", t_char);
            j--;
        }
    }

    while (i>=0){
        s_char = s[i];
        //printf ("\ns:%llu, t:%d", s_char, -1);
        fprintf (align_s_file, "%llu ", s_char);
        fprintf (align_t_file, "%d ", -1);
        i--;
    }

    while (j>=0){
        t_char = t[j];
        //printf ("\ns:%d, t:%llu", -1, t_char);
        fprintf (align_s_file, "%d ", -1);
        fprintf (align_t_file, "%llu ", t_char);
        j--;
    }
    
    return 0;
}

