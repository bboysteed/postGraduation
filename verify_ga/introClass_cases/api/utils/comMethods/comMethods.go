package comMethods

import "io/ioutil"

func GetFileList(pathIn string) []string{
	var fileList []string
	fs, _ := ioutil.ReadDir(pathIn)
	for _, file := range fs {
		if file.IsDir() {
			//fmt.Println(file.Name())
			if file.Name()!="tests"{
				fileList = append(fileList, file.Name())
			}
		}
	}
	return fileList
}
