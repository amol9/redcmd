
from .main_func import MainFunc

class Map:
    init_types = {
        'main_func': MainFunc
    }

    def __init__(self):
        pass


    def run(self, init_type, *args, **kwargs):
        init_type_class = self.init_types.get(init_type, None)

        if init_type_class is None:
            raise Exception("invalid init type")

        init_type_instance = init_type_class()
        init_type_instance.run(*args, **kwargs)
