import paho.mqtt.subscribe as subscribe

msg = subscribe.simple("djwzl", hostname="broker-cn.emqx.io")
print("%s %s" % (msg.topic, msg.payload))