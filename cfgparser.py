import json, os, sys
import configparser, yaml, toml
import logging


class CfgParser:
    def __init__(self, cfg_path=None, section=None, encoding='utf-8'):
        self.type_id = {'.json': 0, '.yaml': 1, '.yml': 1, '.ini': 2, '.conf': 2, '.toml': 3, '.tml': 3}
        self.func_map = {0: self._parser_json, 1: self._parser_yaml, 2: self._parser_ini, 3: self._parser_toml}
        self.cfg_path = cfg_path
        self.encoding = encoding
        self.section = section

    def __call__(self, *args, **kwargs):
        return self.parser_cfg()

    def parser_cfg(self):
        _id = self.parser_cfg_type()
        cfg = self.func_map.get(_id, self._parser_none)()
        return cfg

    def parser_cfg_type(self):
        filepath, shotname, extension = self.filepath_filename_fileext()
        try:
            cfg_type_id = self.type_id[extension]
            return cfg_type_id
        except KeyError:
            logging.error(msg='this configparser not support %s' % extension)

    def _parser_json(self):
        with open(self.cfg_path, encoding=self.encoding) as fr:
            cfg = json.load(fr)
        return cfg

    def _parser_ini(self):
        config = configparser.ConfigParser()
        try:
            config.read(self.cfg_path, encoding=self.encoding)
        except configparser.MissingSectionHeaderError:
            logging.error(msg='File contains no section headers.')
            sys.exit()
        sections = config.sections()
        if not self.section:
            logging.warning(msg="The first section is selected by default, You'd better specify section, "
                                "such as ConfigParser(cfg_path=cfg_path, section='abc')")
            self.section = sections[0]  # 如果没指定section，默认第一个section
        cfg = dict(config.items(section=self.section))
        return cfg

    def _parser_yaml(self):
        # you need 'pip install pyyaml' first
        with open(self.cfg_path, 'r', encoding=self.encoding) as fr:
            cfg = yaml.safe_load(fr)
        return cfg

    def _parser_toml(self):
        # you need 'pip install toml' first
        cfg = toml.load(self.cfg_path)
        return cfg

    def _parser_none(self):
        return "Can't parser this type, support %s only!" % self.type_id.keys()

    def filepath_filename_fileext(self):
        filepath, filename = os.path.split(self.cfg_path)
        shotname, extension = os.path.splitext(filename)
        return filepath, shotname, extension


if __name__ == '__main__':
    cfg_path = 'mqtt_config.ini'
    config_info = CfgParser(cfg_path=cfg_path)
    print(config_info())

