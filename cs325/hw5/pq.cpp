/*
 * In this file, you will write the structures and functions needed to
 * implement a priority queue.  Feel free to implement any helper functions
 * you need in this file to implement a priority queue.  Make sure to add your
 * name and @oregonstate.edu email address below:
 *
 * Name:  Lyon Kee
 * Email: keel@oregonstate.edu
 */

#include <stdlib.h>

#include "pq.h"
#include "dynarray.h"

/*
 * This is the structure that represents a priority queue.  You must define
 * this struct to contain the data needed to implement a priority queue.
 */
 struct node{
   int priority;
   void* value;
 };

struct pq{
  struct dynarray* data;
};


/*
 * This function should allocate and initialize an empty priority queue and
 * return a pointer to it.
 */
struct pq* pq_create() {
  struct pq* queue = new struct pq;
  queue->data = dynarray_create();
  return queue;
}


/*
 * This function should free the memory allocated to a given priority queue.
 * Note that this function SHOULD NOT free the individual elements stored in
 * the priority queue.  That is the responsibility of the caller.
 *
 * Params:
 *   pq - the priority queue to be destroyed.  May not be NULL.
 */
void pq_free(struct pq* pq) {
  if(pq){
    dynarray_free(pq->data);
    free(pq);
    pq = NULL;
  }
  return;
}


/*
 * This function should return 1 if the specified priority queue is empty and
 * 0 otherwise.
 *
 * Params:
 *   pq - the priority queue whose emptiness is to be checked.  May not be
 *     NULL.
 *
 * Return:
 *   Should return 1 if pq is empty and 0 otherwise.
 */
int pq_isempty(struct pq* pq) {
  if(!pq || !pq->data)
    return 1;
  return !dynarray_size(pq->data);
}


/*
 * This function should insert a given element into a priority queue with a
 * specified priority value.  Note that in this implementation, LOWER priority
 * values are assigned to elements with HIGHER priority.  In other words, the
 * element in the priority queue with the LOWEST priority value should be the
 * FIRST one returned.
 *
 * Params:
 *   pq - the priority queue into which to insert an element.  May not be
 *     NULL.
 *   value - the value to be inserted into pq.
 *   priority - the priority value to be assigned to the newly-inserted
 *     element.  Note that in this implementation, LOWER priority values
 *     should correspond to elements with HIGHER priority.  In other words,
 *     the element in the priority queue with the LOWEST priority value should
 *     be the FIRST one returned.
 */
void pq_insert(struct pq* pq, void* value, int priority) {
  if(pq){
    int i = dynarray_size(pq->data);
    struct node* n = new struct node;
    n->value = value;
    n->priority = priority;
    dynarray_insert(pq->data, n);
    while(i > 0 && n->priority < ((struct node*) dynarray_get(pq->data, (i-1)>>1))->priority){
      dynarray_set(pq->data, i, dynarray_get(pq->data, (i-1)>>1));
      dynarray_set(pq->data, (i-1)>>1, n);
      i = (i-1) / 2;
    }
  }
  return;
}


/*
 * This function should return the value of the first item in a priority
 * queue, i.e. the item with LOWEST priority value.
 *
 * Params:
 *   pq - the priority queue from which to fetch a value.  May not be NULL or
 *     empty.
 *
 * Return:
 *   Should return the value of the first item in pq, i.e. the item with
 *   LOWEST priority value.
 */
void* pq_first(struct pq* pq) {
  if(pq)
    return ((struct node*) dynarray_get(pq->data, 0))->value;
  return NULL;
}


/*
 * This function should return the priority value of the first item in a
 * priority queue, i.e. the item with LOWEST priority value.
 *
 * Params:
 *   pq - the priority queue from which to fetch a priority value.  May not be
 *     NULL or empty.
 *
 * Return:
 *   Should return the priority value of the first item in pq, i.e. the item
 *   with LOWEST priority value.
 */
int pq_first_priority(struct pq* pq) {
  if(pq)
    return ((struct node*) dynarray_get(pq->data, 0))->priority;
  return -1;
}


/*
 * This function should return the value of the first item in a priority
 * queue, i.e. the item with LOWEST priority value, and then remove that item
 * from the queue.
 *
 * Params:
 *   pq - the priority queue from which to remove a value.  May not be NULL or
 *     empty.
 *
 * Return:
 *   Should return the value of the first item in pq, i.e. the item with
 *   LOWEST priority value.
 */
void* pq_remove_first(struct pq* pq) {
  if(pq && dynarray_size(pq->data) > 0){
    int i = 0;
    struct node* first = dynarray_get(pq->data, 0), 
      *current = dynarray_get(pq->data, dynarray_size(pq->data)-1);
    void* val = first->value;
    dynarray_set(pq->data, 0, current);
    dynarray_remove(pq->data, dynarray_size(pq->data)-1);
    while((i<<1) + 1 < dynarray_size(pq->data)){
      struct node* left = dynarray_get(pq->data, (i<<1) + 1), *right = NULL;
      if((i<<1) + 2 < dynarray_size(pq->data))
        right = dynarray_get(pq->data, (i<<1) + 2);
      if(right && current->priority > right->priority && right->priority < left->priority){
        i = (i<<1) + 2;
      }else if(current->priority > left->priority){
        i = (i<<1) + 1;
      }
      else{
        break;
      }
      dynarray_set(pq->data, (i-1)>>1, dynarray_get(pq->data, i));
      dynarray_set(pq->data, i, current);
    }
    free(first);
    return val;
  }
  return NULL;
}
