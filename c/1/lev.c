#include <string.h>
#include <stdio.h>

void connect()
{
    printf("Connected to C extension...\n");
}

int addNum(int a, int b)
{
    int nAdd = a + b;
    return nAdd;
}

int distance (const char * word1, const char * word2)
{
    int len1 = strlen (word1);
    int len2 = strlen (word2);
    int matrix[len1 + 1][len2 + 1];
    int i;
    int j;
    for (i = 0; i <= len1; i++) {
        matrix[i][0] = i;
    }
    for (i = 0; i <= len2; i++) {
        matrix[0][i] = i;
    }
    for (i = 1; i <= len1; i++) {
        int j;
        char c1;

        c1 = word1[i-1];
        for (j = 1; j <= len2; j++) {
            char c2;

            c2 = word2[j-1];
            if (c1 == c2) {
                matrix[i][j] = matrix[i-1][j-1];
            }
            else {
                int delete;
                int insert;
                int substitute;
                int minimum;

                delete = matrix[i-1][j] + 1;
                insert = matrix[i][j-1] + 1;
                substitute = matrix[i-1][j-1] + 1;
                minimum = delete;
                if (insert < minimum) {
                    minimum = insert;
                }
                if (substitute < minimum) {
                    minimum = substitute;
                }
                matrix[i][j] = minimum;
            }
        }
    }   
    return matrix[len1][len2];
}

int lenchar (const char * word)
{
    int len1 = strlen (word);
    return len1;
}

int *creer_tableau(void)
{
    static int tableau[5];
    int i;
    
    for (i=0; i<5; i++)
        tableau[i] = i * 3;
        
    return tableau;
}

int main ()
{
    const char * word1;
    const char * word2;
    int d;
    word1 = "niche";
    word2 = "chien";
    d = distance (word1, word2);
    printf ("Distance between %s and %s is %d.\n", word1, word2, d);
    
    const char * word = "coucou";
    int l = lenchar(word);
    printf ("Len of %s is %d.\n", word1, l);
    
    return 0;
}







