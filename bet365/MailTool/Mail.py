from email.mime.text import MIMEText
from email.header import Header
import smtplib
import json
import threading
from multiprocessing import Process
import time

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst


class Mail():
    def __init__(self):
        self.from_addr = 'xcg19865@126.com'
        self.to_addr = 'xucg021@163.com'
        self.pwd = 'jhjh159'
        self.smtp_server = 'smtp.126.com'
        self.server = smtplib.SMTP(self.smtp_server, 25)
        self.server.login(self.from_addr, self.pwd)
        self.server.set_debuglevel(0)


    def run(self, subject, message):
        # print(subject, message)
        message_send = MIMEText(message, 'plain', 'utf-8')
        message_send['to'] = self.to_addr
        message_send['from'] = self.from_addr
        message_send['Subject'] = Header(subject, 'utf-8').encode()
        self.server.sendmail(self.from_addr, [self.to_addr], message_send.as_string())
        self.server.quit()

    @classmethod
    def class_run(cls, subject, message):
        cls().run(subject, message)

    @classmethod
    def send(cls, subject, message):
        t = threading.Thread(target=cls.class_run, args=(subject, message))
        t.daemon = True
        t.start()
        t.join()

if __name__ == '__main__':
    dict = {'a':123}
    # Mail.send('恭喜您！',json.dumps(dict))
    Mail.send('恭喜您！', json.dumps('fdsfdsafsaf', ensure_ascii=False))
    #
    # Mail().run('恭喜您！',json.dumps(dict))

    print('112343244323423')


