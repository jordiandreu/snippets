import subprocess
import shlex
import time
import sys

labelit = "/beamlines/bl13/commissioning/software/phenix/phenix-1.8-1069/build/intel-linux-2.6-x86_64/bin/labelit.distl"
xds = "/beamlines/bl13/commissioning/software/xds/XDS-INTEL64_Linux_x86_64/xds"
xds_wd = "cd /beamlines/bl13/controls/tmp/xds;"

image = "/beamlines/bl13/controls/tmp/mxraster/True/images/True_201510151550_0006.cbf"
host = "ssh opbl13@pcbl1304"
where = "echo from: $HOSTNAME"
sep = " "

cmds = {'testremote': [host, where],
        'testremoteadapted': str(host + sep + where),
        'labelit': [labelit, image],
        'labelitadapted': str(labelit + sep + image),
        'labelitremote': [host, labelit, image],
        'labelitremoteadapted': str(host + sep + labelit + sep + image + ";" + where),
        'xdsremoteadapted': str(host + sep + xds_wd + sep + xds + ";" + where)
}


def execute(cmd, split=False, timeout=12):
    if split:
        cmd = shlex.split(cmd)
    print cmd

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    t = time.time()

    while p.poll() is None:
        time.sleep(0.2)
        if (time.time() - t) > timeout:
            print "timeout"
            os.kill(p.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            retval = -1
            break
        else:
            out, err = p.communicate()
            retval = out

    print retval


# executed as opbl13 or sicilia in ALL machines
if __name__ == "__main__":

#    execute(cmds['testremote'], False) #from pcbl1301: Failed, from ibl1302: Failed
#    execute(cmds['testremote'], True) #from pcbl1301: Failed (parsing), from ibl1302: Failed (parsing)

#    execute(cmds['testremoteadapted'], False) #from pcbl1301: Failed, from ibl1302: Failed
#    execute(cmds['testremoteadapted'], True) #from pcbl1301: OK, from ibl1302: OK

#    execute(cmds['labelit'],False) #from pcbl1301: OK, from ibl1302:Failed (32bit?)
#    execute(cmds['labelit'],True) #from pcbl1301: Failed (parsing), from ibl1302: Failed (parsing)

#    execute(cmds['labelitadapted'],False) #from pcbl1301: Failed (parsing), from ibl1302:Failed (parsing)
#    execute(cmds['labelitadapted'],True) #from pcbl1301:OK, from ibl1302:Failed (32bit?)

#    execute(cmds['labelitremote'],False) #from pcbl1301: Failed (parsing), from ibl1302: Failed (parsing)
#    execute(cmds['labelitremote'],True) #from pcbl1301: Failed (parsing), from ibl1302: Failed (parsing)

#    execute(cmds['labelitremoteadapted'],False) #from pcbl1301: Failed (parsing), from ibl1302: Failed (parsing)
####    execute(cmds['labelitremoteadapted'],True) #from pcbl1301: OK, from ibl1302: OK

    execute(cmds['xdsremoteadapted'],True) #from pcbl1301: OK, from ibl1302: OK
