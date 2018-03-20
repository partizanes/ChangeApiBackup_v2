# -*- coding: utf-8 -*-
# by Part!zanes 2018

import smtplib
from threading import Thread
from email.mime.text import MIMEText

from const import EMAIL_FROM, MAIL_TO, SMTP_SERVER

def alertToSupport(_subject, _message):
    thr = Thread(target=send_async_email, args=[_subject, _message])
    thr.start()


def send_async_email(_subject, _message):
    msg = MIMEText('' + _message)

    msg['Subject'] =  "[WARNING] %s"%(_subject)

    msg['From'] = EMAIL_FROM

    receivers = MAIL_TO
    msg['To'] = ", ".join(MAIL_TO)

    s = smtplib.SMTP(SMTP_SERVER)
    s.sendmail(msg['From'], receivers, msg.as_string())
    s.quit()