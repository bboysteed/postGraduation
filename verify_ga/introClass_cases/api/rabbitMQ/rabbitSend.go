package rabbitMQ

import (
	"api/utils/log"
	"github.com/streadway/amqp"
)

var ch *amqp.Channel
var queueSend amqp.Queue
var queueRecv amqp.Queue

func Init() {
	conn, err := amqp.Dial("amqp://admin:123456@127.0.0.1:5672")
	handleError(err, "连接失败")
	ch, err = conn.Channel()
	handleError(err, "新建通道失败")


	//新建发送通道
	queueSend, err = ch.QueueDeclare(
		"pyQueue",
		true,
		false,
		false,
		false,
		nil,
	)


	//新建接收通道
	queueRecv, err = ch.QueueDeclare(
		"goQueue",
		true,
		false,
		false,
		false,
		nil,
	)

	handleError(err, "申明接收通道失败")
	log.Info().Msg("golang rabbitMQ init success")
}

func MqSendMessage(message string) error {
	err := ch.Publish(
		"",
		queueSend.Name,
		false,
		false,
		amqp.Publishing{
			ContentType:  "text/plain",
			DeliveryMode: amqp.Persistent,
			Body:         []byte(message),
		},
	)
	if err != nil {
		return err
	} else {
		return nil
	}
}


func handleError(err error, message string) {
	if err != nil {
		log.Info().Msgf("%s,err is:%s ", message, err.Error())
	}
}
