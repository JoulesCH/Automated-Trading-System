#pragma once
#include <stdio.h>
#include <stdlib.h>

typedef struct Node{
    double info;
    struct Node *next;
    struct Node *prev;
}Node;

Node* newNode(double info){
    Node *p = (Node *) malloc(sizeof(Node));
    p->next = NULL;
    p->prev = NULL;
    p->info = info;
    return p;
}

void freeNodes(Node *node){
    Node *next = node->next;
    free(node);
    if(next != NULL)
        freeNodes(next);
}


class DoubleList{
    public:
        Node *head;
        Node *tail;
        int len;
        Node *iterCurrent;
        DoubleList();
        
        void append(double info);
        Node *get(int index);
        Node *next(void);
        void remove(int index);
        void pushFront(double info);
        void popFront(void);
        void pushBack(double info);
        void popBack(void);
        void insertAfter(double nuevo, double anterior);
        Node* search(double info);
        void free();
};

DoubleList::DoubleList(void){
    head = (Node *) malloc(sizeof(Node));
    head->next = NULL;
    head->prev = NULL;
    iterCurrent = NULL;
    tail = head; 
    len = 0;
}
Node *DoubleList::next(void){
    if(!iterCurrent || iterCurrent == tail)
        iterCurrent = head;
    else 
        iterCurrent = iterCurrent->next;
    return iterCurrent;
}
void DoubleList::append(double info){
    Node *p = newNode(info);
    
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

void DoubleList::pushFront(double info){
    Node *p = newNode(info);
    if (len == 0){
        len++;
        head = p;
        tail = p;
        return;
    }
    len++;
    (*head).prev = p;
    p -> next = head;
    head = p;
}

void DoubleList::popFront(void){
    Node *aux = head;
    
    head = head->next;
    head->prev = NULL;
    len--;
    std::free(aux);
}
void DoubleList::popBack(void){
    Node *aux = tail;
    
    tail = tail->prev;
    tail->next = NULL;
    len--;
    std::free(aux);
}
void DoubleList::pushBack(double info){
    Node *p = newNode(info);
    tail->next = p;
    p->prev = tail;
    tail = p;
    len++;
}

Node * DoubleList::get(int index){
    Node * p = head;
    int i = 0;
    while(i<index){
        if(!p->next)
            return NULL;
        p = p -> next;
        i++;
    }
    return p;
}

// o - o
void DoubleList::remove(int index){
    Node *toDelete = get(index);
    if(index == 0){
        head = get(index+1);
    }
    else{
        Node *anterior = get(index-1);
        anterior->next = toDelete->next;
    }
    len--;
    std::free(toDelete);
}
Node* DoubleList::search(double info){
    Node * aux = head; 
    while(aux->info != info )
        printf("Buscando...");
        if(aux == tail){
            return NULL;
        }
        aux = aux-> next;
    return aux;
}
void DoubleList::insertAfter(double nuevo, double anterior){
    Node *aux = search(anterior);
    if(aux){
        Node *p = newNode(nuevo);
        p->next = aux -> next;
        p->prev = aux;
        aux->next = p;
        p->next->prev = p;
        len++;
    }
}
void DoubleList::free(void){
    freeNodes(head);
}
