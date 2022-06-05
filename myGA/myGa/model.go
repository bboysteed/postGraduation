/*
 * @Descripttion:
 * @version:
 * @Author: steed
 * @Date: 2022-05-28 14:21:16
 * @LastEditors: bboysteed 18811603538@163.com
 * @LastEditTime: 2022-06-01 22:41:28
 */

package myGa

import (
	"errors"
	"fmt"
	"io/fs"
	"io/ioutil"
	"os"
	"path/filepath"
)

type GaEngin struct {

	Populations [][]byte `default:""`//queue的测试用例

}

/**
 * @description: 
 * @param {*} iter
 * @param {int} popSize 
 * @param {*} seedp 输入路径
 * @param {string} outp 输出路径
 * @return {*}
 */
func NewGaEngin(seedp, outp string) (*GaEngin,error){
	//获取文件
	inputSeeds := make([]string,0,10)
	err := filepath.WalkDir(seedp,func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir(){
			return nil
		}
		absPath,_ := filepath.Abs(path)
		inputSeeds = append(inputSeeds, absPath)
		return nil
		
	})
	if err != nil {
		return nil,fmt.Errorf("read seeds failed with err: %s",err.Error())
	}
	if len(inputSeeds)==0{
		return nil,errors.New("用例为空,请补充用例")
	}

	// fmt.Println(inputSeeds)
	//2.导入种子
	pops := make([][]byte,0)
	// aCase := make([]byte, 1024)
	for i := 0; i < len(inputSeeds); i++ {
		file,err := os.OpenFile(inputSeeds[i],os.O_RDONLY,0755)
		if err != nil {
			return nil,fmt.Errorf("读取seed文件失败,原因：%s",err.Error())
		}
		
		aCase,err := ioutil.ReadAll(file)
		if err != nil {
			return nil,fmt.Errorf("read seed files failed with err: %s",err.Error())
		}
		// fmt.Println(string(aCase))
		pops = append(pops, aCase)
		// pops[i] = []byte{0xff, 0xff, 0xff, 0xff}
	}

	return &GaEngin{
		Populations: pops,
	},nil
}

/**
 * @Descripttion: bit反转
 * @Author: steed
 * @msg:
 * @param {[]byte} outBuf
 * @param {int} curIdx 范围[0,len(outBuf)<<3)
 * @return {*}
 */
func (ga *GaEngin) BitFlip(outBuf []byte, curIdx int) {
	outBuf[curIdx>>3] ^= (128 >> (curIdx & 7))
	//runTarget

}

func (ga *GaEngin) SelectOP() {

}

func (ga *GaEngin) CossoverOP() {

}

func (ga *GaEngin) MutaionOP() {
	//stage one bit flip 1/1

}
