from django import http


class JsonDict(http.QueryDict):

    def __init__(self, json_dict=None, mutable=False):
        if json_dict:
            for key, value in json_dict.items():
                if isinstance(value, list):
                    # treat list values as set of values of MultiValueDict
                    self.setlist(key, value)
                else:
                    self[key] = value
        super().__init__(mutable=mutable)
