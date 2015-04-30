#ifndef __PRETTY_H
#define __PRETTY_H


char* pretty_size(size_t rawsize);// rawsize is in bytes.

char* pretty_time(double duration,int input_unit);

// the second parameter tells pretty_time() what unit your duration is expressed in.
#define U_NANOSECONDS  0
#define U_MICROSECONDS 1
#define U_MLLISECONDS  2
#define U_SECONDS      3
// NTS: used as indexes -> smallest unit should always be zero



#endif
