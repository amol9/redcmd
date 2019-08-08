from os.path import dirname as _dn, join as _j


class MainFunc:

    def __init__(self):
        pass

    
    def run(self, filename):
        code = None

        with open(_j(_dn(__file__), "main_func_template.py"), 'r') as f:
            code = f.read()

        out_file = filename
        with open(out_file, 'w') as f:
            f.write(code)
