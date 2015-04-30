char* h_size(size_t rawsize);

// macros for specifying input unit

#define U_NANOSECONDS  0
#define U_MICROSECONDS 1
#define U_MLLISECONDS  2
#define U_SECONDS      3
// (used as indexes -> smallest unit should always be zero)

char* h_time(double duration,int input_unit);
