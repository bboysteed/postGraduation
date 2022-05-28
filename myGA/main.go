/*
 * @Descripttion:
 * @version:
 * @Author: steed
 * @Date: 2022-05-28 14:17:59
 * @LastEditors: steed
 * @LastEditTime: 2022-05-28 15:14:45
 */

package main

import (
	"MYGA/myGa"
	"encoding/hex"
	"fmt"
)

func main() {
	myga := myGa.NewGaEngin(10, 2)
	fmt.Println(myga.Populations)
	fmt.Println(hex.Dump(myga.Populations[0]))
}
