from setuptools import setup
import os


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


version = '2.0.dev0'
shortdesc = "Uchronian Logic: UPBGE Logic Nodes."
longdesc = '\n\n'.join([read_file(name) for name in [
    'README.md'
]])


setup(
    name='uplogic',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python',
    ],
    keywords='Blender UPBGE Gameengine Logic Nodes',
    author='Leopold Auersperg-Castell',
    author_email='lauersperg@gmx.at',
    url='https://github.com/IzaZed/Uchronian-Logic-UPBGE-Logic-Nodes',
    license='GPLv2',
    packages=[
        'uplogic'
    ],
    zip_safe=True,
    install_requires=['setuptools']
)
