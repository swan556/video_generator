#include <stdio.h>

#define R return
#define P printf
#define F(a,b,c) for(a=b;a<=c;a++)

int main(){
    int i=1,n=5;
    F(i,1,n)P("%d\n",i);
    R 0;
}