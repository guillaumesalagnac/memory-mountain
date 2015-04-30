#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/time.h>

#include "human.h"

// GS-2015-04-27-19:07 choosing  a small datatype (char,  short) seems
// to yield poor results. (the bottleneck is not memory any more)

/* typedef char data_t; */
/* typedef short data_t; */
/* typedef int data_t; */
typedef double data_t;

size_t size;  // size of data array. in Bytes
data_t *data; // data array itself. malloc'ed
size_t count; // nb elements in the data array
int stride;   // step size (in units of data_t)

data_t run()
{
    data_t result=0;
    size_t i;
    for( i=0; i<count; i += stride )
    {
        result += data[i];
    }
    return result;
}

void fill()
{
    size_t i;
    for( i=0; i<count; i += stride )
    {
        data[i] += i*3.14*rand();
    }
}


int main(int argc, char* argv[])
{
    if(argc != 3)
    {
        printf("wrong usage\n");
        exit(1);
    }

    size=atoll(argv[1]);
    stride=atoi(argv[2]);
    count=size/sizeof(data_t);
    printf("size=%lu (%s ; %lu items of size %lu) stride=%d\n",
           (unsigned long)size, h_size(size),
           count, sizeof(data_t), stride);

    printf("malloc(");fflush(stdout);
    data=(data_t*) malloc(size);
    printf(")");fflush(stdout);

    srand(time(NULL));
    
    printf("fill(");fflush(stdout);
    fill();
    printf(")\n");fflush(stdout);
    
    float duration=0; // in microseconds
    int repeats=1;
    while(1)
    {
        // GS-2015-04-27-19:13 volatile is required. (dont' know why
        // but it is) (might be CPU's fault)
        volatile data_t dummy;
            
        dummy+=run();//cache warm-up
        
        clock_t begin=clock();
        int r;
        
        for(r=0;r<repeats;r++)
        {
            dummy+=run();
        }

        clock_t end=clock();
        
        duration=(float)end - (float)begin ;
        
        printf("%d repeats -> %fus\n",repeats,duration);

        if(duration > 100000) // only measurements above 1/10th second make sense
            break;

        repeats = repeats*10;
    }

    duration = duration/repeats;
    
    printf("individual duration = %fus\n",duration);

    size_t quantity = (count/stride)*sizeof(data_t);// in bytes again
    
    printf("read %s in %s = %.1f MB/s\n",
           h_size(quantity),
           h_time(duration,U_MICROSECONDS),
           ((float)quantity)/duration // bytes per microseconds = megabytes per second
           );
    return 0;
}
