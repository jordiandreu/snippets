import subprocess

print subprocess.__file__
from subprocess import Popen, PIPE, STDOUT

def testSubprocessSimpleOutput():
    print 80*'#'

    cmd = 'ls -l'
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
     close_fds=True)
    out, err = p.communicate()
    print 'Output: \n %s' %out
    print 'Errors: \n %s' %err


def testSubprocessExtendOutput():
    print 80*'#'
    host = 'sicilia@controls01'
    cmd  = 'ls'
    rem_cmd = 'ssh %s \"%s\"' % (host, cmd)

    process = subprocess.Popen(rem_cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    data, err = process.communicate()
    print data

if __name__ == '__main__':
    testSubprocessSimpleOutput()
    testSubprocessExtendOutput()