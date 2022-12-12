import paho.mqtt.client as mqtt
import logging
from cfgparser import CfgParser
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class MQTTKit:
    def __init__(self, cfg_path=None, log=False, section=None, encoding='utf-8', clean_session=None, userdata=None):
        self.host = 'broker-cn.emqx.io'
        self.port = 1883
        self.keep_alive = 60
        self.name = None
        self.pwd = None
        self.mqtt_client = None
        self.log = log
        self.config = CfgParser(cfg_path=cfg_path, section=section, encoding=encoding)() if cfg_path else None
        self.userdata = userdata
        self.clean_session = clean_session
        self._init_mqtt()

    def _init_mqtt(self):
        # 配置文件参数解析
        self.host = self.config['host'] if self.config else self.host
        self.port = self.config['port'] if self.config else self.port
        self.keep_alive = self.config['keep_alive'] if self.config else self.keep_alive
        self.name = self.config['name'] if self.config else self.name
        self.pwd = self.config['pwd'] if self.config else self.pwd
        if self.config is None:
            logging.warning(msg='without config file, here use default mqtt server, '
                                'which is {host: %s, port: %s, keep_alive: %s, name: %s, pwd: %s'
                                % (self.host, self.port, self.keep_alive, self.name, self.pwd))
        # 建立mqtt客户端, MQTTv31 -> 3,MQTTv311 -> 4, MQTTv5 -> 5
        self.mqtt_client = mqtt.Client(protocol=4, clean_session=self.clean_session, userdata=self.userdata)
        if self.name and self.pwd:
            self.mqtt_client.username_pw_set(self.name, self.pwd)

        # 召回函数 callbacks
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_publish = self.on_publish
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_subscribe = self.on_subscribe
        self.mqtt_client.on_unsubscribe = self.on_unsubscribe
        if self.log: self.mqtt_client.on_log = self.on_log

        # 状态
        self.connected_flag = False
        self.disconnect_flag = True

        # connect
        self.mqtt_client.connect(host=self.host, port=int(self.port), keepalive=int(self.keep_alive))

        # 发布和订阅
        # self.mqtt_client.publish(topic, payload=None, qos=0, retain=False, properties=None)
        # self.mqtt_client.subscribe(topic, qos=0, options=None, properties=None)

    @staticmethod
    def on_publish(client, userdata, mid):
        logging.info(msg='your message published ok')

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.connected_flag = True
            logging.info(msg="mqtt connected OK, returned code=%d" % rc)
        else:
            logging.error(msg="Bad connection, returned code=%d" % rc)

    @staticmethod
    def on_disconnect(client, userdata, rc):
        logging.info(msg="client disconnected OK, Returned code=%d" % rc)
        client.connected_flag = False
        client.disconnect_flag = True

    @staticmethod
    def on_unsubscribe(client, userdata, mid):
        logging.info(msg='client unsubscribe ok')

    @staticmethod
    def on_subscribe(client, userdata, mid, granted_qos):
        logging.info(msg='client subscribe ok')

    @staticmethod
    def on_log(client, userdata, level, buf):
        logging.info(msg=buf)

    @staticmethod
    def on_message(client, userdata, message):
        logging.info("message received:%s,topic:%s, retained: %s" %
                     (str(message.payload.decode('utf-8')), message.topic, message.retain))
        if message.retain == 1:
            logging.info(msg="This is a retained message")


if __name__ == '__main__':
    mymqtt = MQTTKit(cfg_path='mqtt_config.ini')
    mymqtt.mqtt_client.publish(topic='djwzl', payload='wocnm', qos=1)
    # mymqtt.mqtt_client.subscribe(topic='djwzl', qos=1)





