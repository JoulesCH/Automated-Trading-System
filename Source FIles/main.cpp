// BUILT-IN HEADERS
#include <stdlib.h> // para malloc
#include <string.h> // unicamente para strcat
#include <stdio.h> 
#include <wchar.h> // para usar caracteres especiales
#include <locale.h>
#include <string>
#include <fstream>
#include <math.h>

// LOCAL HEADERS
#include "models.h"

#define MAX_SIZE_FILE_NAME 256
#define WINDOW 20-1
#define ERROR 0.01
#define MAX_INV 0.8

int main(int argc, char * argv[]){
    
    char *inputFile = (char*) malloc(MAX_SIZE_FILE_NAME*sizeof(char));
    char *outputFile = (char*) malloc(MAX_SIZE_FILE_NAME*sizeof(char));
    float capital = 2000;
    DoubleList Data = DoubleList();
    
    if(argc == 1){ //Si el usuario no ingresa ningun argumento, se le solicita el nombre de archivo a leer
        printf("Ingresa el nombre del archivo a leer: ");
        fgets(inputFile, MAX_SIZE_FILE_NAME, stdin);
        inputFile[strlen(inputFile)-1]='\0';
        strcat(outputFile, inputFile);
        strcat(outputFile, ".json");

    } else if(argc == 3){ 
        // Si el usuario ingresa dos argumentos, se toma el primero como el nombre de archivo a leer
        // y el segundo como el capital inicial
        capital = atof(argv[2]);
        inputFile = argv[1];
        outputFile = argv[1];
        strcat(outputFile, ".json");
    }

    std::fstream myfile("GOOGL.txt", std::ios_base::in);

    double a;
    
    while (myfile >> a)
    {
        Data.append(a);
    }
    int j = 0;
    double sum = 0, std, mean, upper, lower, data, capital_a_invertir, num;
    for(int i = 0; i< Data.len; i++){
        data = Data.get(i)->info;
        sum+=data;
        if(i>= WINDOW){
            mean = sum/(WINDOW+1);
            num = 0;
            for(int k = i-WINDOW; k<WINDOW+1; k++){
                num= num + (Data.get(k)->info - mean)*(Data.get(k)->info - mean);
            }
            std = sqrt(num/(WINDOW));
            upper = mean + 2*std;
            lower = mean - 2*std; 
            
            printf("\n\n\n***** %d PRECIO: %f upper: %f lower: %f mean: %f std: %f*****\n", i, data, upper, lower, mean, std);  

            if( abs(data-upper)/data < ERROR  || abs(data-lower)/data < ERROR || data>upper || data< lower ){
                capital_a_invertir = capital *MAX_INV;
                if(abs(data-upper)/data < ERROR || data>upper){
                    printf("Vendiendo accion!!! DIF: %f",  abs(data-upper)/data);
                }
                else{
                    
                    printf("\nComprando accion!!! Volumen: %f DIF: %f", capital_a_invertir/data, abs(data-lower)/data );
                }
            }

            sum-= Data.get(j)->info;
            j++;
        }
    }
    //printf("%f\t", Data.get(i)->info);

    printf("\n\n%s %s %f ",inputFile, outputFile, capital);
}