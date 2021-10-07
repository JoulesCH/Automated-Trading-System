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
// #define ERROR 0.01
// #define MAX_INV 0.7
// #define STOP_LOSS 1000
// #define TAKE_PROFIT 1

int main(int argc, char * argv[]){
    
    char *inputFile = (char*) malloc(MAX_SIZE_FILE_NAME*sizeof(char));
    char *outputFile = (char*) malloc(MAX_SIZE_FILE_NAME*sizeof(char));
    float capital = 2000, ERROR=0.01, MAX_INV=0.7, STOP_LOSS=1000, TAKE_PROFIT=1;

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

    } else{ 
        // Si el usuario ingresa dos argumentos, se toma el primero como el nombre de archivo a leer
        // y el segundo como el capital inicial
        printf("\n0: %s 1: %s 2: %s 3:%s\n", argv[0], argv[1],argv[2],argv[3]);
        capital = atof(argv[2]);
        inputFile = argv[1];
        strcpy(outputFile, argv[1]);
        //outputFile = argv[1];
        strcat(outputFile, ".json");
        printf("\n0: %s 1: %s 2: %s 3:%s\n", argv[0], argv[1],argv[2],argv[3]);
    
    }
    
    double a;
    DoubleListMove DataOutput = DoubleListMove();
    
    if(argc <= 3){
        std::fstream myfile(inputFile, std::ios_base::in);

        while (myfile >> a)
            Data.append(a);

    }else{
        ERROR=atof(argv[3]);
        MAX_INV=atof(argv[4]);
        STOP_LOSS=atof(argv[5]);
        TAKE_PROFIT=atof(argv[6]);
        for(int i = 7; i<argc; i++)
            Data.append(atof(argv[i]));
        printf("%f %f %f %f", ERROR, MAX_INV, STOP_LOSS, TAKE_PROFIT);
    }

    int j = 0,volumen;
    double sum = 0, std, mean, upper, lower, data, capital_a_invertir, num, balance, gain=0, loss=0;
    Movement * Aux;
    for(int i = 0; i< Data.len; i++){
        data = Data.get(i)->info;
        sum+=data;
        for(int b = 0; b<DataOutput.len; b++){
            Aux = DataOutput.get(b);
            if(Aux->closeIdx==-98765){
                balance= (data - Aux->openValue)*Aux->volumen;
                if(balance<=(-1*STOP_LOSS)){
                    printf("\nVendiendo accion por STOP LOSS!!! balance: %f\n",  balance);
                    loss -= balance;
                    Aux->closeValue = data;
                    Aux->closeIdx =i;
                    Aux->balance= balance;
                    capital += data*Aux->volumen;
                }
            }
        }
        if(i>= WINDOW){
            mean = sum/(WINDOW+1); //19-4
            num = 0;
            for(int k = 0; k<= WINDOW; k++){
                num= num + (Data.get(i-k)->info - mean)*(Data.get(i-k)->info - mean);
            }
            std = sqrt(num/(WINDOW+1));
            upper = mean + 2*std;
            lower = mean - 2*std; 
            
            printf("\n\n***** %d PRECIO: %f upper: %f lower: %f mean: %f std: %f*****\n", i, data, upper, lower, mean, std);  

            if( abs(data-upper)/data < ERROR  || abs(data-lower)/data < ERROR || data>upper || data< lower ){
                if(abs(data-upper)/data < ERROR || data>upper){
                    //
                    for(int b = 0; b<DataOutput.len; b++){
                        Aux = DataOutput.get(b);
                        if( ((Aux->openValue)*TAKE_PROFIT) <= data &&   Aux->closeIdx == -98765 ){
                            printf("\nVendiendo accion en un máximo!!! DIF: %f\n",  abs(data-upper)/data);
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
                    capital_a_invertir = capital * MAX_INV;
                    volumen = ((int)capital_a_invertir/(int)data);
                    if(volumen> 0 ){

                        for (int i = 0; i < 7; ++i) 
                            *(tmp_s+i*sizeof(char)) = alphanum[rand() % (sizeof(alphanum) - 1)];
                        *(tmp_s+7*sizeof(char)) = '\0';

                        printf("\nID: %s Comprando accion en un mínimo!!! Volumen: %d DIF: %f COSTO: %f", tmp_s,volumen, abs(data-lower)/data,volumen*data);
                        capital -= (data*volumen); //Verficar
                        srand( (unsigned) time(NULL) * getpid());
                        DataOutput.append( tmp_s, volumen, data, i, -98765, -98765, -98765 );
                    }
                }
            }

            printf("\n\n\n####### CAPITAL : %f #######", capital);
            if(capital <= 0)
                break;

            sum-= Data.get(j)->info;
            j++;
        }
    }
    //printf("%f\t", Data.get(i)->info);
    if(argc <= 3){
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
            fprintf(json," %cVolumen%c: %i,",34, 34, Aux->volumen); 
            fprintf(json," %cOpenValue%c: %f,",34,34, Aux->openValue);
            fprintf(json," %cOpenIdx%c: %d,",34,34, Aux->openIdx);  
            if( Aux->closeValue > 0){
                fprintf(json," %cCloseValue%c: %f,",34,34, Aux->closeValue);
                fprintf(json," %cCloseIdx%c: %d,",34,34, Aux->closeIdx);
                fprintf(json," %cBalance%c: %f}",34,34, Aux->balance);  
            }else{
                fprintf(json," %cCloseValue%c: null,",34,34);
                fprintf(json," %cCloseIdx%c: null,",34,34);
                fprintf(json," %cBalance%c: null}",34,34);  
            }
            if(b != DataOutput.len-1)
                fprintf(json,","); 
        }
        fprintf(json,"\n\t],");
        fprintf(json,"\n\t%ccapitalFinal%c:%f,", 34,34,capital);
        fprintf(json,"\n\t%cgain%c:%f,", 34,34,gain);
        fprintf(json,"\n\t%closs%c:%f", 34,34,loss);
        fprintf(json, "\n}");
        fclose(json);
        printf("\n\nCAPITAL FINAL: %f \n Se genero un archivo json (%s) con los movimientos", capital, outputFile);
    }else{
        printf("{\n");
        printf("\t%cdata%c:[",34,34);
        for(int b=0; b< DataOutput.len; b++){
            Aux = DataOutput.get(b);
            for (int i = 0; i < 7; ++i) 
                *(tmp_s+i*sizeof(char)) = alphanum[rand() % (sizeof(alphanum) - 1)];
            *(tmp_s+7*sizeof(char)) = '\0';
            printf("\n\t\t{%cMovimiento%c: %c%s%c,",34,34,34, tmp_s,34); 
            printf(" %cVolumen%c: %i,",34, 34, Aux->volumen); 
            printf(" %cOpenValue%c: %f,",34,34, Aux->openValue);
            printf(" %cOpenIdx%c: %d,",34,34, Aux->openIdx);  
            if( Aux->closeValue > 0){
                printf(" %cCloseValue%c: %f,",34,34, Aux->closeValue);
                printf(" %cCloseIdx%c: %d,",34,34, Aux->closeIdx);
                printf(" %cBalance%c: %f}",34,34, Aux->balance);  
            }else{
                printf(" %cCloseValue%c: null,",34,34);
                printf(" %cCloseIdx%c: null,",34,34);
                printf(" %cBalance%c: null}",34,34);  
            }
            if(b != DataOutput.len-1)
                printf(","); 
        }
        printf("\n\t],");
        printf("\n\t%ccapitalFinal%c:%f,", 34,34,capital);
        printf("\n\t%cgain%c:%f,", 34,34,gain);
        printf("\n\t%closs%c:%f", 34,34,loss);
        printf( "\n}");
    }

    Data.free();
    return 0;
}