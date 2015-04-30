#include <stdlib.h>
#include <stdio.h>

#include "pretty.h"

// metric units
#define THOUSAND_BYTES 1000
static char *size_units[]={ "B", "kB", "MB", "GB" };

// IEC units
// #define THOUSAND_BYTES 1024
// static char *size_units[]={ "B", "kB", "MB", "GB" };

char* pretty_size(size_t rawsize)
{
    int unit=0;
    float size=rawsize;
        
    while(size >= THOUSAND_BYTES)
    {
        size/=THOUSAND_BYTES;
        unit++;
    }

    char* ret=(char*)malloc(10);// room for:  NNNN.N digits, 2-char unit, and trailing null

    if( size == (float)(int)size )
        sprintf(ret,"%d%s",(int)size,size_units[unit]);
    else
        sprintf(ret,"%.1f%s",size,size_units[unit]);

    return ret;
}


static char* time_units[]={ "ns", "us", "ms", "s"};

char * pretty_time(double duration,int input_unit)
{
    int unit = input_unit;
    while(duration >1000)
    {
        duration/=1000;
        unit++;
    }

    char *ret=(char*)malloc(10); // room for NNNN.NN digits, 2-char unit, and trailing null

    if( duration == (float)(int)duration)
        sprintf(ret,"%d%s",(int)duration,time_units[unit]);
    else
        sprintf(ret,"%.2f%s",duration,time_units[unit]);

    return ret;
}
