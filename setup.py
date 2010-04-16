#!/usr/bin/env python

from setuptools import setup

setup(name='VHostManager',
      version='0.0.2',
      description='VHostManager',
      long_description = "My VHostManager",
      author="Konstantin vz'One Enchant",
      author_email='sirkonst@gmail.com',
      url='http://wiki.enchtex.info',
      packages = ['VHostManager'],
      package_dir = {'VHostManager': 'src'},
      #package_data = {'VHostManager': ['templates/apache_vhost.tpl']},
      entry_points = {
                      'console_scripts': ['vctl-newusersite = VHostManager.addnewsite:main',
                                          'vctl-addsite = VHostManager.addsite:main']
                      },        
     )