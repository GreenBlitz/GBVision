
def import_all_algorithms():
    ignore_files = {'__init__.py', 'test_open_usb_camera.py'}
    import os
    import importlib
    dir_name = os.path.dirname(__file__)
    for path, dirs, files in os.walk(dir_name):
        for file in files:
            if file.endswith('.py') and file not in ignore_files:
                module = '.' + file[:-3]  # remove .py
                mdl = importlib.import_module(module, package='test.tests')
                if "__all__" in mdl.__dict__:
                    names = mdl.__dict__["__all__"]
                else:
                    # otherwise we import all names that don't begin with _
                    names = [x for x in mdl.__dict__ if not x.startswith("_")]

                # now drag them in
                globals().update({k: getattr(mdl, k) for k in names})


import_all_algorithms()
del import_all_algorithms
