// BUILT-IN HEADERS
#include <stdlib.h> // para malloc
#include <string.h> // unicamente para strcat
#include <stdio.h> 
#include <wchar.h> // para usar caracteres especiales
#include <locale.h>
#include <string>
#include <fstream>
#include <math.h>
#include <ctime>
#include <unistd.h>

// LOCAL HEADERS
#include "models.h"
#include "utils.h"

#define MAX_SIZE_FILE_NAME 256
#define WINDOW 20-1
#define ERROR 0.01
#define MAX_INV 0.7
#define STOP_LOSS 1000
#define TAKE_PROFIT 1.05

int main(int argc, char * argv[]){
    
    char *inputFile = (char*) malloc(MAX_SIZE_FILE_NAME*sizeof(char));
    char *outputFile = (char*) malloc(MAX_SIZE_FILE_NAME*sizeof(char));
    float capital = 2000;

    static const char alphanum[] =
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz";
    char* tmp_s=(char*)malloc(sizeof(char)*8);

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
    DoubleListMove DataOutput = DoubleListMove();
    while (myfile >> a)
    {
        Data.append(a);
    }
    int j = 0;
    double sum = 0, std, mean, upper, lower, data, capital_a_invertir, num, volumen, balance, gain=0, loss=0;
    Movement * Aux;
    for(int i = 0; i< Data.len; i++){
        data = Data.get(i)->info;
        sum+=data;
        for(int b = 0; b<DataOutput.len; b++){
            Aux = DataOutput.get(b);
            if(Aux->closeIdx==-98765){
                balance= (data - Aux->openValue)*Aux->volumen;
                if(balance<=(-1*STOP_LOSS)){
                    printf("Vendiendo accion por STOP LOSS!!! balance: %f\n",  balance);
                    loss -= balance;
                    Aux->closeValue = data;
                    Aux->closeIdx =i;
                    Aux->balance= (Aux->openValue - Aux->closeValue)*Aux->volumen;
                }
            }
        }
        if(i>= WINDOW){
            mean = sum/(WINDOW+1);
            num = 0;
            for(int k = i-WINDOW; k<=i; k++){
                num= num + (Data.get(k)->info - mean)*(Data.get(k)->info - mean);
            }
            std = sqrt(num/(WINDOW));
            upper = mean + 2*std;
            lower = mean - 2*std; 
            
            printf("\n\n***** %d PRECIO: %f upper: %f lower: %f mean: %f std: %f*****\n", i, data, upper, lower, mean, std);  

            if( abs(data-upper)/data < ERROR  || abs(data-lower)/data < ERROR || data>upper || data< lower ){
                capital_a_invertir = capital * MAX_INV;
                if(abs(data-upper)/data < ERROR || data>upper){
                    //
                    for(int b = 0; b<DataOutput.len; b++){
                        Aux = DataOutput.get(b);
                        if( ((Aux->openValue)*TAKE_PROFIT) <= data &&   Aux->closeIdx == -98765 ){
                            printf("Vendiendo accion en un máximo!!! DIF: %f\n",  abs(data-upper)/data);
                            Aux->closeValue = data;
                            Aux->closeIdx =i;
                            Aux->balance= ( Aux->closeValue-Aux->openValue )*Aux->volumen;
                            capital += Aux->volumen * data;
                            if(Aux->balance > 0)
                                gain+=Aux->balance;
                            else
                                loss-=Aux->balance;
                        }
                    }
                
                }
                else{
                    volumen = capital_a_invertir/data;
                    if(volumen> 0 ){

                        for (int i = 0; i < 7; ++i) 
                            *(tmp_s+i*sizeof(char)) = alphanum[rand() % (sizeof(alphanum) - 1)];
                        *(tmp_s+7*sizeof(char)) = '\0';

                        printf("\nID: %s Comprando accion en un mínimo!!! Volumen: %f DIF: %f COSTO: %f", tmp_s,volumen, abs(data-lower)/data,volumen*data);
                        capital -= capital_a_invertir;
                        srand( (unsigned) time(NULL) * getpid());
                        DataOutput.append( tmp_s, volumen, data, i, -98765, -98765, -98765 );
                    }
                }
            }

            printf("\n\n\n####### CAPITAL : %f #######\n\n\n", capital);
            if(capital <= 0)
                break;

            sum-= Data.get(j)->info;
            j++;
        }
    }
    //printf("%f\t", Data.get(i)->info);
    FILE * json;
    json = fopen(outputFile, "w+");
    fprintf(json, "{\n");

    fprintf(json,"\t%cdata%c:[",34,34);
    for(int b=0; b< DataOutput.len; b++){
        Aux = DataOutput.get(b);
        for (int i = 0; i < 7; ++i) 
            *(tmp_s+i*sizeof(char)) = alphanum[rand() % (sizeof(alphanum) - 1)];
        *(tmp_s+7*sizeof(char)) = '\0';
        fprintf(json,"\n\t\t{%cMovimiento%c: %c%s%c,",34,34,34, tmp_s,34); 
        fprintf(json," %cVolumen%c: %f,",34, 34, Aux->volumen); 
        fprintf(json," %cOpenValue%c: %f,",34,34, Aux->openValue);
        fprintf(json," %cOpenIdx%c: %d,",34,34, Aux->openIdx);  
        fprintf(json," %cCloseValue%c: %f,",34,34, Aux->closeValue);
        fprintf(json," %cCloseIdx%c: %d,",34,34, Aux->closeIdx);
        fprintf(json," %cBalance%c: %f}",34,34, Aux->balance);  
        if(b != DataOutput.len-1)
            fprintf(json,","); 
    }
    fprintf(json,"\n\t],");
    fprintf(json,"\n\t%ccapitalFinal%c:%f,", 34,34,capital);
    fprintf(json,"\n\t%cgain%c:%f,", 34,34,gain);
    fprintf(json,"\n\t%closs%c:%f", 34,34,loss);
    fprintf(json, "\n}");
    fclose(json);

    printf("\n\n%s %s %f ",inputFile, outputFile, capital);
    Data.free();
    return 0;
}