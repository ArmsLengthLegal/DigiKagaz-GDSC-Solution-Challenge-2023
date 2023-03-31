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

setup(name='docassemble.DigiKagaz',
      version='0.0.1',
      description=('A docassemble extension.'),
      long_description='DigiKagaz is a self-help tool that addresses the challenges of limited resources and language barriers faced by indigent individuals seeking legal aid services in India. Our solution enables users to generate relevant legal documents quickly and easily, regardless of their language proficiency or financial situation.\r\n\r\nOur team comprises individuals from diverse backgrounds, including legal and technology expertise. We have actively worked on two modules, namely the BAIL Module and the DOMESTIC VIOLENCE MODULE, to address critical issues that require urgent attention. Our modules can also help advocates doing pro bono work to increase their power to handle cases.\r\n\r\nWe have actively tested our solution with real users and have collected valuable feedback that we used to improve our solution. Our goals have been evidenced by the positive feedback we received from users and the increase in the number of users generating legal documents on\xa0our\xa0platform.',
      long_description_content_type='text/markdown',
      author='DigiKagaz Technovation',
      author_email='dev.app@digikagaz.com',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=['googletrans>=3.1.0a0'],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/DigiKagaz/', package='docassemble.DigiKagaz'),
     )

