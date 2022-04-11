package main

import (
	"api/module"
	"api/rabbitMQ"
	"api/utils/comMethods"
	"api/utils/log"
	"github.com/gin-gonic/gin"
	"io/ioutil"
	"net/http"
	"path"
	"strings"
)

const (
	introClassBaseDir        = "/home/steed/Desktop/session_work/git_work/case_generate/IntroClass"
	introClassCaseGenBaseDir = "/home/steed/Desktop/session_work/git_work/case_generate/introClass_cases"
)

var casesFileOk = false

func main() {
	gin.SetMode(gin.DebugMode)
	r := gin.Default()
	rabbitMQ.Init()
	r.POST("/getDirInfo", getDirInfo)
	r.GET("/getCodeContent", getCodeContent)
	r.GET("/geneCases", geneCases)
	r.GET("/consultFileContent", consultFileContent)
	err := r.Run(":8081")
	if err != nil {
		log.Error().Msgf("service is not start,because:%s", err.Error())
	}
}

func consultFileContent(context *gin.Context) {
	projectName := context.Query("projectName")

	if casesFileOk { //已完成计算任务
		buf, err := ioutil.ReadFile(path.Join(introClassCaseGenBaseDir, projectName, "tmpFile", "cases"))
		if err != nil {
			log.Error().Msgf("read file err:%s", err.Error())
			context.JSON(http.StatusOK, gin.H{
				"status": "read file err",
				"cases":  "",
			})

		}else {
			cases := make(map[int]string, 0)
			for k, v := range strings.Split(string(buf), "\n") {
				cases[k] = v
			}
			context.JSON(http.StatusOK, gin.H{
				"status": "ok",
				"cases":  cases,
			})
		}

	} else { //还未生成文件
		context.JSON(http.StatusOK, gin.H{
			"status": "still calc",
			"cases":  "",
		})
	}

}

func geneCases(context *gin.Context) {
	casesFileOk = false
	projectName := context.Query("projectName")
	err := rabbitMQ.MqSendMessage(projectName + ",start gen cases")
	if err != nil {
		log.Warn().Msgf("mq publish message failed,err is:%s", err.Error())
		context.JSON(http.StatusOK, gin.H{
			"status": "submit error",
			"reason": "mq publish message failed",
			"cases":  "",
		})
	} else {
		go func() {
			rabbitMQ.MqMessageConsumer(&casesFileOk)

		}()
		context.JSON(http.StatusOK, gin.H{
			"status": "submit ok",

		})
	}
}

func getCodeContent(context *gin.Context) {
	projectName := context.Query("projectName")
	stuName := context.Query("stuName")
	jobName := context.Query("jobName")
	//log.Info().Msgf("file path is :%s", path.Join(introClassBaseDir, projectName, stuName, jobName))
	content, err := ioutil.ReadFile(path.Join(introClassBaseDir, projectName, stuName, jobName, projectName+".c"))
	//log.Info().Msgf("file content is :%s", string(content))
	if err != nil {
		log.Info().Msgf("err open file,err is:%s", err.Error())
		context.JSON(http.StatusBadRequest, gin.H{
			"status":      "can't get file now",
			"reason":      "busy",
			"codeContent": "",
		})
	} else {
		context.JSON(http.StatusOK, gin.H{
			"status":      "ok",
			"reason":      "",
			"codeContent": string(content),
		})
	}
}

func getDirInfo(context *gin.Context) {

	log.Info().Msgf("projectName is : %s", context.PostForm("projectName"))
	projectName := context.PostForm("projectName")
	studentsInfo := module.Info{}
	studentNames := comMethods.GetFileList(path.Join(introClassBaseDir, projectName))
	for _, stuName := range studentNames {
		var std module.Student
		jobNames := comMethods.GetFileList(path.Join(introClassBaseDir, projectName, stuName))
		for _, jn := range jobNames {
			std.AppendJob(jn, jn)
			std.StuName = "stu--" + stuName[:8]
			std.StuValue = stuName
		}
		studentsInfo.AppendStudent(&std)
	}
	//log.Info().Msg(studentsInfo.AllStudents[0].StuValue)
	context.JSON(200, gin.H{
		"status":  "posted",
		"message": &studentsInfo,
	})

}
