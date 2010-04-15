#!/usr/bin/python
# -*- coding: utf-8 -*-

################ Общие модули ################

import os
import pwd
from string import Template

from shell import ShellError, shell as sh

################ Переменные ################

USERDIRBASE = '/home'
APACHETMPL = ''
APACHEVHOSTS = '/etc/apache2/vhosts.d/'
NGINXDOCROOT = '/etc/nginx/docroot.map'

TESTING = False

################ Логика ################

class Error(Exception): pass

def createnewuser(username):
    """ Создание базового пользователя для сайта """
    userhome = os.path.join(USERDIRBASE, username)
    if os.path.exists(userhome):
        raise Error, "Папка пользователя '%s' уже существует" %  userhome
    
    TESTING or sh("adduser -m -U %s" % username)
    pw = TESTING or pwd.getpwnam(username)
    TESTING or os.chmod(userhome, 750)
    TESTING or sh("setfacl -m -u:nginx:x %s" % userhome)
    os.mkdir( os.path.join(userhome, 'sites') )
    TESTING or os.chown(os.path.join(userhome, 'sites'), pw[2], pw[3])

def addnewsite(username, sitename):
    """ Создание папки сайта. Возвращает в словаре параменты сайта: {docroot, sitename, username} """
    sitesdir = os.path.join(USERDIRBASE, username, 'sites')
    sitedir = os.path.join(sitesdir, sitename)
    if not os.path.isdir(sitesdir):
        raise Error, "Папка для сайтов '%s' не существует" % sitesdir
    
    TESTING or os.mkdir(sitedir)
    pw = TESTING or pwd.getpwnam(username)
    TESTING or os.chown(sitedir, pw[2], pw[3])
    
    return {'docroot': os.path.abspath(sitedir), 'sitename': sitename, 'username': username}

def gen_apache_config(siteconfig):
    """ Генерит текст конфига апача по шаблону
    siteconfig - словарь: {docroot, sitename, username, site_aliases, maxclients}
    """
    with open(APACHETMPL, 'r') as f:
        a_tpl = Template(f.read())
    return a_tpl.substitute(siteconfig)
    