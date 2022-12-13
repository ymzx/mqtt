import paho.mqtt.publish as publish

# ("<topic>", "<payload>", qos, retain)
msgs = [{'topic': "djwzl", 'payload': "multiple 1"},
        {'topic': "djwzl", 'payload': "multiple 2"},
        {'topic': "djwzl", 'payload': "multiple 3"},
        {'topic': "djwzl", 'payload': "multiple 4"},
        {'topic': "djwzl", 'payload': "multiple 5"}]*100

# 批量推送
publish.multiple(msgs, hostname="broker-cn.emqx.io")

