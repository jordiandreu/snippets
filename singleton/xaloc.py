from singleton_decorator import get_beamline


def get_xaloc():
    _xaloc = get_beamline()
    _xaloc.name = 'xaloc'
    return _xaloc
