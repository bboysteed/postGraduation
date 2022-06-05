/*
 * @Descripttion:
 * @version:
 * @Author: steed
 * @Date: 2022-05-28 14:17:59
 * @LastEditors: bboysteed 18811603538@163.com
 * @LastEditTime: 2022-06-01 22:48:38
 */

package main

import (
	"MYGA/myGa"
	"encoding/hex"
	"fmt"
)

func main() {
	myga,err:= myGa.NewGaEngin("./seeds","./out")
	if err != nil {
		fmt.Println("init GaEngin failed with err: ",err)
	}

	
	fmt.Println(myga.Populations)
	fmt.Println(hex.Dump(myga.Populations[0]))
}
