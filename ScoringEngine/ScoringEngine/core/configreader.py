class configreader(object):
    """description of class"""
    _default = {}
    _config = {}

    def __init__(self, config_file, defaults={}, fail_no_file=False):
        self._default = defaults
        if isinstance(config_file, str):
            self._parse_config(config_file)
            return
        elif isinstance(config_file, list):
            import os.path
            for f in config_file:
                if os.path.isfile(f):
                    self._parse_config(f)
                    return
        if fail_no_file:
            raise Exception("Could not load any config files")


    def _parse_config(self, config_file):
        import json
        with open(config_file, 'r') as file:
            self._config = json.loads(file.read())
            file.close()

    @staticmethod
    def _get_item_from_array(path, arr):
        d = arr
        for p in path.split('/'):
            if p in d:
                d = d[p]
            else:
                return None
        return d

    def get_item(self, path):
        c = self._get_item_from_array(path, self._config)
        if c is None:
            c = self._get_item_from_array(path, self._default)
            if c is None:
                raise Exception("Missing parameter \"%s\"" % path)
        return c

    def has_item(self, path):
        return self.get_item(path) is not None

    def put_item(self, path, value):
        raise NotImplementedError()

    def save_default(self, file):
        with open(file, "w") as conf:
            import json
            conf.write(json.dumps(self._default, indent=4))
            conf.flush()
