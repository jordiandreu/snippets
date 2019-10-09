from singleton_decorator import get_beamline


def get_bl13():
    _bl13 = get_beamline()
    _bl13.name = 'bl13'
    return _bl13

