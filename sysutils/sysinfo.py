import mysubprocess
import logging


host = 'ibl1302'



def _exec_remote_cmd(host, cmd):
    rem_cmd = 'ssh %s -C \"%s\"' % (host, cmd)
    process = mysubprocess.Popen(rem_cmd, shell=True, stdout=mysubprocess.PIPE)
    process.wait()
    data, err = process.communicate()
    if process.returncode == 0 and not err:
        return data
    else:
        logging.error('Error %s with code %s' % (err, process.returncode))
        return None

def hostname(host):
    cmd = "python -c 'import platform; print platform.uname()[1]'"
    return _exec_remote_cmd(host, cmd)

def platform(host):
    cmd = "python -c 'import platform; print platform.platform()'"
    return _exec_remote_cmd(host, cmd)

def processors(host):
    # cmd = "cat /proc/cpuinfo | grep name | sed -r 's/model name*.: //'|uniq"
    cmd = "cat /proc/cpuinfo | grep name | sed -r 's/model name*.: //'"
    return _exec_remote_cmd(host, cmd)[:-1].split('\n')

def ram(host):
    cmd = "cat /proc/meminfo | grep MemTotal | sed -r 's/MemTotal://' | sed -e 's/^[ \t]*//'"
    return _exec_remote_cmd(host, cmd)

def ni(host):
    cmd = "/sbin/lspci | grep -i 'National'"
    return _exec_remote_cmd(host, cmd)

def adlink(host):
    cmd = "/sbin/lspci | grep -i 'Adlink'"
    return _exec_remote_cmd(host, cmd)

def rocketport(host):
    cmd = "/sbin/lspci | grep -i 'Rocketport'"
    return _exec_remote_cmd(host, cmd)

def date(host):
    cmd = "date +'%x %r %Z'"
    return _exec_remote_cmd(host, cmd)

def path(host):
    cmd = 'echo $PATH'
    return _exec_remote_cmd(host, cmd)[:-1].split(":")

def ldpath(host):
    cmd = 'echo $LD_LIBRARY_PATH'
    return _exec_remote_cmd(host, cmd)[:-1].split(":")

def pythonpath(host):
    cmd = 'echo $PYTHONPATH'
    return _exec_remote_cmd(host, cmd)[:-1].split(":")

def filesystem(host):
    cmd = 'df -HiTP | column -t'
    return _exec_remote_cmd(host, cmd)

print hostname(host)
print platform(host)
print processors(host)
print ram(host)
print ni(host)
print adlink(host)
print rocketport(host)
print date(host)
print path(host)
print ldpath(host)
print pythonpath(host)
print filesystem(host)