from mqtt_kits import MQTTKit

if __name__ == '__main__':
    # log=True显示mqtt框架消息和自定义消息，log=False仅显示自定义消息
    mymqtt = MQTTKit(cfg_path='mqtt_config.ini', section='server', log=False)
    mymqtt.mqtt_client.publish(topic='djwzl', payload='mmmmmmmm', qos=1)
    mymqtt.mqtt_client.loop_forever()

