import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.rpi',
      version='0.0.1',
      description=('A test interview for running Docassemble on the Raspberry Pi'),
      long_description='This package demonstrates how Docassemble can be integrated with the \r\nRaspberry Pi, using a Christmas-themed interview, a red LED, and a \r\ngreen LED.\r\n[See a video of the interview in action](https://twitter.com/docassemble/status/1211025053263040512)\r\n\r\nUse a Raspberry Pi with at least 4GB of RAM.\r\n\r\nConnect pin 23 to the positive end of a green LED.  \r\nConnect the negative end of the LED to a 220 ohm resistor, and connect the \r\nother end of the resistor to ground (pin 22 or pin 25).\r\n\r\nDo the same for pin 24, except use a red LED.\r\n\r\nThe idea is that 5 volts on pin 23 or 24 will cause current to flow through\r\nthe LED.\r\n\r\nInstall Docker on the Raspberry Pi and grant access to the user `pi`:\r\n\r\n```\r\nsudo apt-get -y install docker.io\r\nsudo usermod -a -G docker pi\r\n```\r\n\r\nYou might need to restart the Raspberry Pi after doing `usermod` in order to ensure\r\nthat the user `pi` can run Docker commands.\r\n\r\nSince the standard images are not built for the ARM architecture, you need to build\r\nthem yourself.\r\n\r\n```\r\ngit clone https://github.com/jhpyle/docassemble-os\r\ncd docassemble-os\r\ndocker build -t jhpyle/docassemble-os .\r\ncd ..\r\ngit clone https://github.com/jhpyle/docassemble\r\ncd docassemble\r\ndocker build -t jhpyle/docassemble .\r\ncd ..\r\n```\r\n\r\nThen create a Docassemble container that has privileged access:\r\n\r\n```\r\ndocker run --privileged --restart=always -d -p 80:80 --env DAPYTHONVERSION=3 jhpyle/docassemble\r\n```\r\n\r\nNext, `docker exec` inside of the container.\r\n\r\nGive the user `www-user` (inside the container) access to `/dev/gpiomem`.\r\nOn the Raspberry Pi host, the owner of this file is `root` and the group is\r\n`gpio`.  But the group `gpio` does not exist inside the container.\r\nWhen you do `ls -l /dev/gpiomem` inside the container, you will likely see that \r\nthe "group" for the file is a number, like 997.  It might be something else for\r\nyou.  You need to add the user `www-data` to that group so that the Docassemble\r\nweb application can access the GPIO pins of the Raspberry Pi.  But if the group \r\nis a number, you can\'t add the user to the group, so first create the group, and\r\nthen add `www-data` to it:\r\n\r\n```\r\naddgroup --gid 997 gpio\r\naddgroup www-data gpio\r\n```\r\n\r\nThen restart the services:\r\n\r\n```\r\nsupervisorctl start reset\r\n```\r\n\r\nBecause the processor is underpowered, things can take a very long time.\r\ncheck `supervisorctl status` to see what is happening, and be patient.',
      long_description_content_type='text/markdown',
      author='Jonathan Pyle',
      author_email='jhpyle@gmail.com',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=['RPi.GPIO'],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/rpi/', package='docassemble.rpi'),
     )

