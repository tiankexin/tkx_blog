# -*- coding:utf-8 -*-

"""
    发送邮件
"""
import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from threading import Thread
from flask import render_template, current_app
from app.settings import GENERAL_MAIL_CONFIG


def send_email(server_name, sender, password, receivers, subject, attachment=None, html_text=None):
    """ 发送邮件
        :params server_name: 邮件服务地址
        :params sender: 发送者邮箱
        :params password: 密码
        :params receivers: 接受人名单
        :params ccs: 抄送人员名单
        :params subject: 邮件主题
        :params attachment: 附件内容
        :params html_text: HTML文本内容
    """
    msg = MIMEMultipart()
    msg['from'] = "来自TKXdeBlog官方通知<{}>".format(sender)
    msg['subject'] = subject
    msg['to'] = ','.join(receivers) if isinstance(receivers, (tuple, list)) else receivers

    if attachment:
        att1 = MIMEBase('application', 'octet-stream')
        att1.set_payload(attachment['fd'].read())
        encoders.encode_base64(att1)
        att1.add_header(
            'Content-Disposition', 'attachment; filename="{}"'.format(attachment['fn'])
        )
        msg.attach(att1)

    if html_text:
        html = MIMEText(html_text, 'html', 'utf-8')
        msg.attach(html)

    try:
        server = smtplib.SMTP_SSL(server_name, '465')
        server.login(sender.split('@')[0], password)
        server.sendmail(
            msg['from'],
            receivers,
            msg.as_string()
        )
        server.quit()
    except Exception as e:
        print(repr(e))


def general_send_email(to, subject, template, **kwargs):
    """
    Blog general email sender
    """
    params = dict(GENERAL_MAIL_CONFIG)
    params['receivers'] = to
    params['subject'] = subject
    params['html_text'] = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_email, kwargs=params)
    thr.start()
    return thr

