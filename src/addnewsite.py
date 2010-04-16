#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Примерение:

$ addnewsite site.name 
"""

################ Общие модули ################

import sys
import os

import vctl

################ Переменные ################

# Testing
#vctl.USERDIRBASE = '../test/home'
#vctl.TESTING = True
#vctl.APACHETMPL = '../templates/apache_vhost.tpl'
#vctl.APACHEVHOSTS = '../test/apache_vhost'
#vctl.NGINXDOCROOT = '../test/docroot.map'
#vctl.FTPPASSDB = '../test/ftp.passwd'

################ Логика ################

def main():
    # Проверка имени сайта
    if len(sys.argv) == 2 and len(sys.argv[1].split('.')) == 2:
        try:
            username = sys.argv[1]
            sitename = 'www.%s' % username
            
            #userpw = vctl.createnewuser(username)
            userpw = {'username': username, 'uid': 777, 'gid': 888, 'homedir': '/test/my.site'}
            vctl.createftpuser(userpw, userpw['homedir'])
            exit(0)
            
            siteconfig = vctl.addnewsite(username, sitename)
            
            siteconfig['site_aliases'] = '%s *.%s' % (username, username)
            siteconfig['maxclients'] = 5
            
            a_conf = vctl.gen_apache_config(siteconfig)
            a_file = os.path.join(vctl.APACHEVHOSTS, "300_%s_vhost.conf" % username)
            
            with open(a_file, 'a') as f:
                f.write(a_conf)
                print "Конфиг apache сохранен в '%s'." % a_file
            
            with open(vctl.NGINXDOCROOT, 'a') as f:
                n_conf = ".%s        %s;\n" % (username, siteconfig['docroot'])
                f.write(n_conf)
                print "Конфиг nginx обновлен '%s'." % vctl.NGINXDOCROOT
            
        except vctl.Error, x:
            print "Ошибка: %s" % x
    else:
        print "Ошибка: не правильной имя сайта."
        exit(1)

if __name__ == '__main__':
    main()