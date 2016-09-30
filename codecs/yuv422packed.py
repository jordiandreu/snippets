import numpy as np

frame = []
for p in range(0,16,2):
    frame.append('U%i' % p)
    frame.append('Y%i' % p)
    frame.append('V%i' % p)
    frame.append('Y%i' % (p+1))

#print frame

frame = np.asarray(frame)
Y = frame[1::2]
U = frame[0::4]
V = frame[2::4]

U = U.repeat(2,axis=0)
V = V.repeat(2,axis=0)

print "Y: %s" % Y
print "U: %s" % U
print "V: %s" % V