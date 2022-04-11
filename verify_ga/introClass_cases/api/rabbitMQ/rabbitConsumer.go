package rabbitMQ

import "api/utils/log"

func MqMessageConsumer(isok *bool){
	msgs,recErr := ch.Consume(
		queueRecv.Name,
		"",
		true,
		false,
		false,
		false,
		nil,
		)
	handleError(recErr,"接受消息错误")
	for msg := range msgs {
		log.Info().Msgf("rec message from quene:%s,%s",queueRecv.Name,msg.Body)
		//msg.Ack(true)
		messageRec := string(msg.Body)
		log.Info().Msgf("golang recv msg:%s",messageRec)
		if messageRec == "genCases ok" {
			*isok = true
			log.Info().Msgf("isok:%v",*isok)
		}
		//break
	}

}
//func handleError(err error, message string) {
//	if err != nil {
//		log.Info().Msgf("%s,err is:%s ", message, err.Error())
//	}
//}

