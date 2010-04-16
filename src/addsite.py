#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Добавление нового сайта к пользователю.

Команда:
$ addsite site.my mail.site.my

создаст папку сайта mail.site.my для пользователя site.my, добавит конфиг апача и настройки в nginx, и ftp доступ к папке сайта.
"""

################ Общие модули ################

import sys
import os
import shutil

import vctl

################ Переменные ################

## Testing
#vctl.TESTING = True

################ Логика ################

def main():
    if len(sys.argv) == 3:
        try:
            username, sitename = sys.argv[1], sys.argv[2]
            userpw = vctl.get_userpw(username)
            userpw['username'] = sitename
            
            site = vctl.addnewsite(username, sitename)
            print "Создан сайт %(sitename)s в папке %(docroot)s" % site
            
            vctl.createftpuser(userpw, site['docroot'])
            print "Добавлен FTP доступ пользователю %s (%s) к папке %s" % (userpw['username'], username, site['docroot'])
            
            site['maxclients'] = 5
            site['site_aliases'] = sitename
            a_conf = vctl.gen_apache_config(site)
            
            a_file = os.path.join(vctl.APACHEVHOSTS, "%i_%s_vhost.conf" % (userpw['uid'], username))
            
            with open(a_file, 'a') as f:
                f.write(a_conf)
                print "Конфиг apache сохранен в '%s'." % a_file
                
            shutil.copy(vctl.NGINXDOCROOT, vctl.NGINXDOCROOT + '.bak')
            with open(vctl.NGINXDOCROOT, 'a') as f:
                n_conf = "%s        %s;\n" % (sitename, site['docroot'])
                f.write(n_conf)
                print "Конфиг nginx обновлен '%s'." % vctl.NGINXDOCROOT
        except vctl.Error, x:
            print "Ошибка: %s" % x
            exit(1)
    else:
        print "Ошибка: введите <имя пользователя> и <имя сайта>."
        exit(1)

if __name__ == '__main__':
    main()