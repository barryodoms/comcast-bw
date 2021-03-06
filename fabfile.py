#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import task

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime
import os

import commands

username = os.environ.get('SENDGRID_USERNAME')
password = os.environ.get('SENDGRID_PASSWORD')
to_email = os.environ.get('CRON_EMAIL')

def send_email(email_msg):
    print "Emailing bandwidth usage at %s" % datetime.datetime.now()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Comcast Bandwidth Usage"
    msg['From'] = username
    msg['To'] = to_email
    msg.attach(MIMEText(email_msg, 'plain'))

    s = smtplib.SMTP('smtp.sendgrid.net', 587)
    s.login(username, password)
    s.sendmail(username, to_email, msg.as_string())
    s.quit()

@task
def email_usage():
    """ send an email with your bandwidth usage to CRON_EMAIL """
    output = commands.getoutput('python comcastBandwidth.py')
    send_email(output)

@task
def email_warn_usage():
    """ if bandwidth usage over 200GB, send an email to CRON_EMAIL """
    output = commands.getoutput('python comcastBandwidth.py -w')
    if output:
        send_email(output)
