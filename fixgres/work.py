#!/usr/bin/env python
import sys
import os
from email.parser import Parser

from models import Email, Session
from dateutil import parser

session = Session()

def stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def walk_domain(domain, path):
    new_path = os.path.join(path, 'new')
    email_filenames = os.listdir(new_path)
    email_count = len(email_filenames)
    print 'Reading %s, %d emails.' % (domain, email_count)
    for i, email_filename in enumerate(email_filenames):
        email_filepath = os.path.join(new_path, email_filename)

        try:
            message = Parser().parse(open(email_filepath, 'r'))
            email = Email()
            email.domain = domain
            email.header_from = message['from']
            email.header_to = message['to']
            email.header_subject = message['subject']
            email.header_date = parser.parse(message['date'])

            email.postgres_filename = email_filename
            email.original = message.as_string()

            session.add(email)
            session.commit()

            cur_path = os.path.join(path, 'cur')
            os.rename(email_filepath, os.path.join(cur_path, email_filename))

        except Exception, exc:
            print exc

            fail_path = os.path.join(path, 'fail')
            if not os.path.exists(fail_path):
                os.makedirs(fail_path)

            os.rename(email_filepath, os.path.join(fail_path, email_filename))

        stdout('\r%5d/%5d : %0.2f%%' % (i, email_count, i * 100.0 / email_count))
    stdout('\rDone.                \n')

def main():
    for domain in os.listdir('/var/mail'):
        domain_path = os.path.join('/var/mail', domain)
        if os.path.isdir(domain_path):
            walk_domain(domain, domain_path)

if __name__ == '__main__':
    main()
