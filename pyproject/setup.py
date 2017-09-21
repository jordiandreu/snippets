from setuptools import setup, find_packages

# The version is updated automatically with bumpversion
# Do not update manually
__version = '0.1.0'

name = 'project'

package_list=['doc/*.txt',
              'strategy/doc_strategy/*.txt',
              'transmission/ScatteringFactors/*.txt']

console_scripts = []
gui_scripts = []

entry_points = {
        'console_scripts': console_scripts,
        'gui_scripts': gui_scripts
    }

description = ''

long_description = ''

setup(
    name=name,
    version=__version,
    packages=find_packages(),
#    packages=find_packages(name),
#    package_dir={'':name},
    entry_points=entry_points,
    author='',
    author_email='',
    description=description,
    long_description=long_description,
    url='',
    platforms='all',
    package_data={'': package_list},
    include_package_data=True,
    install_requires=['setuptools', 'python'],
    requires=[],
)

