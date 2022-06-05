/*
 * @Descripttion: 
 * @version: 
 * @Author: steed
 * @Date: 2022-05-29 13:44:37
 * @LastEditors: steed
 * @LastEditTime: 2022-05-29 13:44:37
 */


/*
 * @Descripttion: 
 * @version: 
 * @Author: steed
 * @Date: 2022-05-28 18:23:05
 * @LastEditors: steed
 * @LastEditTime: 2022-05-28 21:49:15
 */
#include <stdio.h>

int addTwoNum(int a, int b){
    return a+b;
}

int main(){
    int a,b,c;
    scanf("%d %d %d",&a,&b,&c);

    // a= 1;
    // b = 2;
    // c  = 3;
    // c = addTwoNum(a,b);
    int i = 0;
    while(i<5){
        printf("loop!\n");
        i++;
    }
    if(a>99){
        printf("> : %d\n",addTwoNum(a,c));
    }else{
        printf("< : %d\n",addTwoNum(a,b));
        
    }
    
    return 0;
}