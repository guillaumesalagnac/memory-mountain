#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/time.h>

#include "pretty.h"

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

data_t test()
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
    srand(time(NULL));

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
        printf("usage: %s SIZE STRIDE\n",argv[0]);
        printf("\n");
        printf("Allocate a memory buffer and walk it, reporting read throughput.\n");
        printf("  SIZE is the size of the buffer (in bytes).\n");
        printf("  STRIDE is the distance between two successive reads (in 64bit items).\n");
        exit(1);
    }

    size=atoll(argv[1]);
    stride=atoi(argv[2]);
    count=size/sizeof(data_t);
    printf("size=%ju (%s ; %ju items of size %ju) stride=%d\n",
           (uintmax_t)size, pretty_size(size),
           (uintmax_t)count, (uintmax_t)sizeof(data_t), stride);

    data=(data_t*) malloc(size);

    // GS-2015-04-30-14:00 sometimes filling the buffer with non-zero data changes the
    // results. But it is slow so we leave it out for now
    /* printf("filling the buffer...");fflush(stdout); */
    /* fill(); */
    /* printf("OK\n");fflush(stdout); */
    
    double duration=0; // in microseconds
    int repeats=1;
    while(1)
    {
        // GS-2015-04-27-19:13 volatile is required. (dont' know why
        // but it is) (might be CPU's fault)
        volatile data_t dummy=0;
            
        dummy+=test();//cache warm-up
        
        clock_t begin=clock();
        int r;
        
        for(r=0;r<repeats;r++)
        {
            dummy+=test();
        }

        clock_t end=clock();
        
        duration=(uintmax_t)end - (uintmax_t)begin ;
        
        printf("%d repeats -> %s\n",repeats,pretty_time(duration,U_MICROSECONDS));

        if(duration > 1000)
            break;

        repeats = repeats*10;
    }

    duration = duration/repeats;
    
    printf("=> one repeat -> %s\n",pretty_time(duration,U_MICROSECONDS));

    size_t quantity = (count/stride)*sizeof(data_t);// in bytes again
    
    printf("read %s in %s = %.1f MB/s\n",
           pretty_size(quantity),
           pretty_time(duration,U_MICROSECONDS),
           ((float)quantity)/duration // bytes per microseconds = megabytes per second
           );
    return 0;
}
