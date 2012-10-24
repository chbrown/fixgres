#!/usr/bin/env python
import os
import subprocess
import argparse

__dir__ = os.path.dirname(__file__)
main_cf_template = open(os.path.join(__dir__, 'main.cf')).read()

def etc_postfix_virtual(domains):
    virtual_path = '/etc/postfix/virtual'
    print 'Writing %s' % virtual_path
    virtual = '\n'.join('@%(domain)s %(domain)s/' % dict(domain=domain) for domain in domains)
    with open(virtual_path, 'w') as fp:
        fp.write(virtual)
    subprocess.call(['postmap', virtual_path])

def var_mail(domains, uid, gid):
    var_mail_path = '/var/mail'
    for domain in domains:
        fullpath = os.path.join(var_mail_path, domain)
        if not os.path.exists(fullpath):
            print 'Creating directory: %s' % fullpath
            os.makedirs(fullpath)
        os.chown(fullpath, uid, gid)

def etc_postfix_main_cf(domains, uid, gid):
    main_cf_path = '/etc/postfix/main.cf'
    print 'Writing %s' % main_cf_path
    main_cf = main_cf_template % dict(domains=','.join(domains), uid=uid, gid=gid)
    with open(main_cf_path, 'w') as fp:
        fp.write(main_cf)
    subprocess.call(['postfix', 'reload'])

def main():
    parser = argparse.ArgumentParser(description='Configure catch-all postgres for given domains. Requires root.')
    parser.add_argument('domains', type=str, nargs='+')
    parser.add_argument('--uid', type=int, default=1000)
    parser.add_argument('--gid', type=int, default=1000)
    opts = parser.parse_args()

    domains = [domain.strip() for domain in opts.domains]

    etc_postfix_virtual(domains)
    var_mail(domains, opts.uid, opts.gid)
    etc_postfix_main_cf(domains, opts.uid, opts.gid)

if __name__ == '__main__':
    main()
