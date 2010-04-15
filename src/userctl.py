#!/usr/bin/python
# -*- coding: utf-8 -*-

## Создание сайта. Этапы:
# 1. создание юзера, настройка прав
# 2. создание конфига хоста apache из шаблона
# 3. конфигурирование nginx
# 4. создание ftp пользователя
# 5. перезапуск nginx и apache

#
# 
#

from shell import shell as sh, ShellError

import os
import os.path
import  tempfile
from subprocess import call
import shutil

apache_templ_file = '../tpl/apache_vhost.tpl'
apache_vhost_dir = '../test/apache_vhost'
nginx_docroot_file = '../test/docroot.map'

def genapacheconfig(site, templ_file=apache_templ_file):
    """ Генерация конфига vhost для апача. Передается словать сайта. Возращает текст по шаблону """
    with open(templ_file) as f:
        text = ''.join(f.readlines())
    return text % site

def gennginxconfig(site):
    """ Генерация конфига для nginx """
    pass

def createsiteuser(site):
    """ Создание базового пользователя для сайта """
    try:
        if os.path.isdir('/home/%(userhome)s' % site):
            raise Exception, "Папка уже сущействует"
        sh("adduser -m -U %(username)s" % site, test=True)
        sh("chmod 750 %(userhome)s" % site, test=True)
        sh("setfacl -m -u:nginx:x %(userhome)s" % site, test=True)
        sh("mkdir -p %(docroot)s" % site, test=True)
        sh("chown %(username)s:%(username)s -R %(userhome)s" % site, test=True)
        site['uid'] = 1009
        site['gid'] = 1010
    except ShellError, x:
        print x
        exit(1)
        
def createftpuser(site):
    """ Создание ftp пользователя """
    pass

def createnewsite(basename):
    """ Создание нового пользователя и сайта поумолчанию www.basename """
    site = {
            'sitename': 'www.' + basename,
            'sitename_aliases':  '%s *.%s' % (basename, basename),
            'username': basename,
            'userhome': '/home/%s' % basename,
            'docroot': '/home/%s/sites/www.%s' % (basename, basename),
            'maxclients': 5
            }
    ## Создание и настройка пользователя
    createsiteuser(site)
    # Генерация конфига для апач
    apcfg = genapacheconfig(site)
    apcfg_file = os.path.join(apache_vhost_dir, '%i_%s_vhost.conf' % (site['uid'], basename))
    if os.path.isfile(apcfg_file):
        raise Exception, "Ошибка: файл конфига '%s' apache уже существует." % apcfg_file
    with open(apcfg_file, 'w') as f:
        f.writelines(apcfg)
    call(['nano', apcfg_file])
    # TODO: Генерация конфига для nginx
    shutil.copy(nginx_docroot_file, nginx_docroot_file + '.old')
    with open(nginx_docroot_file, 'a') as f:
        line = '.%s\t\t%s;\n' % (basename, site['docroot'])
        f.write(line)
    call(['nano', nginx_docroot_file])
    ## TODO: Создание ftp пользователя
    createftpuser(site)

def addsite(name, basename):
    """ name = www, basename = site.my """
    # Проверки
    if not os.path.isdir('/home/%s/sites' % basename):
        raise Exception, "Базовая папка сайта '%s' не существует" %  basename
    sitepath = '/home/%s/sites/%s.%s' % (basename, name, basename)
    if os.path.isdir(sitepath):
        raise Exception, "Папка сайта '%s' уже существует" % sitepath
    # Создание
    os.mkdir(sitepath)
    sh("chown %s:%s %s" % (basename, basename, sitepath), test=True)

def maincreatesite(sitename):
    """ Создание и настройка сайта """
    # Определить нужно создать новый сайт или добавить поддомен
    name = sitename.split('.')
    if len(name) == 2:
        createnewsite('.'.join(name))
    if len(name) > 2:
        addsite('.'.join(name[:-2]), '.'.join(name[-2:]))

def test():
    from string import Template
    s = Template('User: $uname, uid: $uid')
    user = {'uname': 'Konst', 'uid': 777}
    print s.substitute(user)
    
    print sh('who konst', 'ls', 'ls -l')

if __name__ == "__main__":
    #maincreatesite('my.site')
    test()