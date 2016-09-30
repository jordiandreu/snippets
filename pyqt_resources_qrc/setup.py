
from __future__ import print_function

import os, sys
from distutils.core import setup, Command
from distutils.command.build import build as dftbuild


def abspath(*path):
    """A method to determine absolute path for a given relative path to the
    directory where this setup.py script is located"""
    setup_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(setup_dir, *path)

package_dir = {'mytestmodule': abspath('src', 'mytestmodule')}
packages = ['mytestmodule', 'mytestmodule.resources']
package_data = {'': ['*.png', '*.svg'],}


class build_resources(Command):

    description = "\"build\" Qt resource files"
    user_options = []

    def initialize_options(self):
        self.resource_dir = abspath('src/mytestmodule/resources')
        print("res dir:", self.resource_dir)
        self.logo = os.path.join(self.resource_dir, 'alba-logo.png')
        self.rcc_exec = None#"rcc"
        self.pyrcc4_exec = "pyrcc4"

    def finalize_options(self):
        pass

    def run(self):
        print("***************************")
        print("run")
        orig_dir = os.path.abspath(os.curdir)
        print (orig_dir)
        os.chdir(self.resource_dir)
        try:
            self._build_general_res()
        finally:
            os.chdir(orig_dir)

    def _build_general_res(self):
        qrc_filename = 'resources.qrc'
        rcc_filename = 'qrc_resources.rcc'
        rc_filename = 'resources_rc.py'
        out = sys.stdout
        print("Generating %s... " % qrc_filename, file=out, end = '')
        out.flush()
        f = file(qrc_filename, 'w')
        try:
            logo_relpath = os.path.relpath(self.logo)
            f.write('<!DOCTYPE RCC ><RCC version = "1.0" >\n')
            f.write('<qresource>\n')
            f.write('\t<file alias = "alba-logo.png">%s</file>\n' % logo_relpath)
            f.write('</qresource>\n')
            f.write('</RCC>\n')
        except Exception, e:
            print("[FAILED]\nDescription:\n%s" % str(e), file=out)
            raise e
        finally:
            f.close()
        print("[DONE]", file=out)

        # Generate python rc file
        if self.pyrcc4_exec:
            print("Generating %s... " % rc_filename, file=out, end = '')
            out.flush()
#            cmd = '%s -binary %s -o %s' % (self.rcc_exec,
#                                           qrc_filename, rcc_filename)
            cmd = '%s -o %s %s' % (self.pyrcc4_exec, rc_filename, qrc_filename)
            if os.system(cmd):
                print("[FAILED]", file=out)
            else:
                print("[DONE]", file=out)

                return [[qrc_filename], [rc_filename]]

        # Generate binary rcc file
        if self.rcc_exec:
            print("Generating %s... " % rcc_filename, file=out, end = '')
            out.flush()
            cmd = '%s -binary %s -o %s' % (self.rcc_exec,
                                           qrc_filename, rcc_filename)
            if os.system(cmd):
                print("[FAILED]", file=out)
            else:
                print("[DONE]", file=out)
                return [[qrc_filename], [rcc_filename]]


class build(dftbuild):

    def initialize_options(self):
        dftbuild.initialize_options(self)
        # self.logo = None

    def finalize_options(self):
        dftbuild.finalize_options(self)
        # if self.logo is None:
        #     self.logo = abspath('lib', 'taurus', 'qt',
        #                         'qtgui', 'resources', 'taurus.png')

    def run(self):
        dftbuild.run(self)

    def has_resources(self):
        return os.path.isdir(abspath('src/mytestmodule/resources'))

    sub_commands = [('build_resources', has_resources)] + \
        dftbuild.sub_commands


cmdclass = {'build': build,
            'build_resources': build_resources
            }


def main():
    setup(
        name="pyqt_resources_qrc",
        version="0.1.0",
        packages=packages,
        package_dir=package_dir,
        package_data=package_data,
        cmdclass=cmdclass
    )

if __name__ == "__main__":
    try:
        main()
        print("Setup finished")
    except Exception as e:
        print("A error occured: %s\n\nSetup aborted" % str(e))