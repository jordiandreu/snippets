from bl13 import get_bl13
from xaloc import get_xaloc

bl13 = get_bl13()
print(bl13.name)
xaloc = get_xaloc()
print(xaloc.name)

print('Are bl13 and xaloc the same beamline? {}'.format(bl13 is xaloc))

print('bl13 name is {}'.format(bl13.name))
print('xaloc name is {}'.format(xaloc.name))

