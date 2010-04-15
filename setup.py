#!/usr/bin/env python

from setuptools import setup

setup(name='VHostManager',
      version='0.0.1',
      description='VHostManager',
      long_description = "My VHostManager",
      author="Konstantin vz'One Enchant",
      author_email='sirkonst@gmail.com',
      url='http://wiki.enchtex.info',
      packages = ['VHostManager'],
      package_dir = {'VHostManager': 'src'},
      package_data = {'templates': ['templates/*']},
      entry_points = {
                      'console_scripts': ['vctl-newsite = VHostManager.addnewsite:main']
                      },        
     )