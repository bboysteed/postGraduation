/*
 * @Descripttion:
 * @version:
 * @Author: steed
 * @Date: 2022-05-28 14:21:16
 * @LastEditors: steed
 * @LastEditTime: 2022-05-28 16:34:36
 */

package myGa

type GaEngin struct {
	Populations [][]byte
}

func NewGaEngin(iter, popSize int) *GaEngin {
	pops := make([][]byte, popSize)
	for i := 0; i < popSize; i++ {
		pops[i] = []byte{0xff, 0xff, 0xff, 0xff}
	}

	return &GaEngin{
		Populations: pops,
	}
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

}
