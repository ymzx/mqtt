from mqtt_kits import MQTTKit
import logging


def on_message(client, userdata, message):
    logging.info(msg='the message is [%s]' % str(message.payload.decode('utf-8')))


if __name__ == '__main__':
    mymqtt = MQTTKit(cfg_path='mqtt_config.ini', section='server', log=True)
    mymqtt.mqtt_client.subscribe(topic='djwzl', qos=1)
    mymqtt.mqtt_client.on_message = on_message
    mymqtt.mqtt_client.loop_forever()

