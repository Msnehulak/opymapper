from . import diff_create, map_create


def new_diff():
    return diff_create.CreateDiff()


def new_mapset():
    return map_create.CreateMap()
