# -*- coding: utf-8 -*-
# by Part!zanes 2018

import smtplib
from threading import Thread
from email.mime.text import MIMEText

from const import EMAIL_FROM, MAIL_TO, SMTP_SERVER

def alertToSupport(_subject, _message, _recivers=MAIL_TO):
    thr = Thread(target=send_async_email, args=[_subject, _message, _recivers])
    thr.start()


def send_async_email(_subject, _message, _recivers):
    msg = MIMEText('' + _message)

    msg['Subject'] =  "[BACKUP] %s"%(_subject)

    msg['From'] = EMAIL_FROM

    receivers = _recivers
    msg['To'] = ", ".join(_recivers)

    s = smtplib.SMTP(SMTP_SERVER)
    s.sendmail(msg['From'], receivers, msg.as_string())
    s.quit()