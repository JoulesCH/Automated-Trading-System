#pragma once

#include <stdio.h>
#include <stdlib.h>

typedef struct Movement{
    char  *id;
    double volumen;
    double openValue;
    int openIdx;
    double closeValue;
    int closeIdx;
    double balance;
    struct Movement *next;
    struct Movement *prev;
}Movement;

Movement* newNode(char  *id, double volumen, double openValue, int openIdx, double closeValue, int closeIdx, double balance){
    Movement *p = (Movement *) malloc(sizeof(Movement));
    p->next = NULL;
    p->prev = NULL;
    p->volumen = volumen;
    p->openValue = openValue;
    p->openIdx = openIdx;
    p->closeValue = closeValue;
    p->closeIdx = closeIdx;
    p->balance = balance;
    return p;
}

void freeNodes(Movement *node){
    Movement *next = node->next;
    free(node);
    if(next != NULL)
        freeNodes(next);
}


class DoubleListMove{
    public:
        Movement *head;
        Movement *tail;
        int len;
        Movement *iterCurrent;
        DoubleListMove();
        
        void append(char  *id, double volumen, double openValue, int openIdx, double closeValue, int closeIdx, double balance);
        Movement *get(int index);
        Movement *next(void);
        void free();
};

DoubleListMove::DoubleListMove(void){
    head = (Movement *) malloc(sizeof(Movement));
    head->next = NULL;
    head->prev = NULL;
    iterCurrent = NULL;
    tail = head; 
    len = 0;
}
Movement *DoubleListMove::next(void){
    if(!iterCurrent || iterCurrent == tail)
        iterCurrent = head;
    else 
        iterCurrent = iterCurrent->next;
    return iterCurrent;
}
void DoubleListMove::append(char  *id, double volumen, double openValue, int openIdx, double closeValue, int closeIdx, double balance){
    Movement *p = newNode(id, volumen, openValue, openIdx, closeValue, closeIdx, balance);
    
    if (len == 0){
        len++;
        head = p;
        tail = p;
        return;
    }
    len++;
    (*tail).next = p;
    p->prev = tail;
    tail = p;
}

Movement * DoubleListMove::get(int index){
    Movement * p = head;
    int i = 0;
    while(i<index){
        if(!p->next)
            return NULL;
        p = p -> next;
        i++;
    }
    return p;
}

void DoubleListMove::free(void){
    freeNodes(head);
}
