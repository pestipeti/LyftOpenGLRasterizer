import dill
import os


def obj_save(obj, filename, dir_cache):
    with open(f'{dir_cache}/{filename}.dil', 'wb') as f:
        dill.dump(obj, f)


def obj_load(filename, dir_cache):
    with open(f'{dir_cache}/{filename}.dil', 'rb') as f:
        return dill.load(f)


def obj_exists(filename, dir_cache):
    return os.path.isfile(f'{dir_cache}/{filename}.dil')
