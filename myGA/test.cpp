/*
 * @Descripttion: 
 * @version: 
 * @Author: steed
 * @Date: 2022-05-28 18:23:05
 * @LastEditors: steed
 * @LastEditTime: 2022-05-28 21:49:15
 */
#include <iostream>
using namespace std;

int addTwoNum(int a, int b){
    return a+b;
}

int main(){
    int a,b,c;
    cin>>a >>b>>c;

    // a= 1;
    // b = 2;
    // c  = 3;
    // c = addTwoNum(a,b);
    int i = 0;
    while(i<5){
        cout << "loop!" << endl;
        i++;
    }
    if(a>99){
        cout << addTwoNum(a,c) << endl;
    }else{
        cout << addTwoNum(a,b) << endl;
        
    }
    
    return 0;
}