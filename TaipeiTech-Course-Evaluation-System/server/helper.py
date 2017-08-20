import smtplib
import requests
import hashlib
import hmac
import datetime
from email.mime.text import MIMEText
from urllib import parse
from bs4 import BeautifulSoup
from settings import SETTING

def current_time() -> datetime:
    return datetime.datetime.utcnow()

def sha256hash(data: str) -> str:
    if 'SECRET_KEY' not in SETTING:
        raise Exception('SECRET_KEY 尚未設定')
    
    data = '%' + str(len(data)) + '%' + data

    return hmac.new(
        SETTING['SECRET_KEY'].encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()

def sha512hash(data: str) -> str:
    if 'SECRET_KEY' not in SETTING:
        raise Exception('SECRET_KEY 尚未設定')
    
    data = '%' + str(len(data)) + '%' + data
    return hmac.new(
        SETTING['SECRET_KEY'].encode(),
        data.encode(),
        hashlib.sha512
    ).hexdigest()


class TaipeiTechCourseCrawler:
    
    query_course_url = 'http://aps.ntut.edu.tw/course/tw/QueryCourse.jsp'
    course_description_url = 'http://aps.ntut.edu.tw/course/tw/Curr.jsp?format=-2&code={}'

    def __init__(self):
        pass
    
    def _parse_course(self, html) -> list:
        soup = BeautifulSoup(html, "html5lib")
        courses = []
        for tr in soup.find_all('tr'):
            td = tr.find_all('td')
            if td:
                course = {
                    'ccode': td[1].find('a').get('href').split('code=')[1],
                    'code': td[0].get_text().strip('\n '),
                    'cname': td[1].get_text().strip('\n '),
                    'credits': td[3].get_text().strip('\n '),
                    'hours': td[4].get_text().strip('\n '),
                    'cprog': td[5].get_text().strip('\n '),
                    'class': td[6].get_text().strip('\n '),
                    'tname': td[7].get_text().strip('\n '),
                    'classroom': td[15].get_text().strip('\n '),
                }
                courses.append(course)
        return courses

    def _parse_course_description(self, html) -> dict:
        soup = BeautifulSoup(html, "html5lib")
        #print(html)
        if len(soup.find_all('tr')) <= 1:
            return None
        _ = soup.find_all('tr')[1].find_all('td')
        result = {
            'ccode': _[0].get_text().strip('\n '),
            'name': _[1].get_text().strip('\n ') + '\n' + _[2].get_text().strip('\n '),
            'credits': _[3].get_text().strip('\n '),
            'hours': _[4].get_text().strip('\n '),
            'chinese_description': soup.find_all('tr')[2].find('td').get_text().strip('\n '),
            'english_description': soup.find_all('tr')[3].find('td').get_text().strip('\n ')
        }
        return result

    def get_course_description(self, ccode) -> dict:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'TaipeiTech CES Crawler',
            'Referer': TaipeiTechCourseCrawler.course_description_url,
            'Origin': 'http://aps.ntut.edu.tw'
        }
        response = requests.get(
            TaipeiTechCourseCrawler.course_description_url.format(ccode),
            headers=headers
        )
        print(ccode)
        return self._parse_course_description(response.text)

    def query_by_course_name(self, params: dict) -> list:
        params['stime'] = '0'
        params['matric'] = "'0','1','4','5','6','7','8','9','A','C','D','E','F'"
        params['unit'] = '**'
        params['tname'] = ''

        ccodes = []
        result = []
        for i in range(7):
            params['D{}'.format(i)] = 'ON'
        for i in range(14):
            params['P{}'.format(i)] = 'ON'
        for sem in range(1, 3):
            params['sem'] = sem
            for year in range(90, 107):
                params['year'] = year
                courses = self.query_by_course_time(params)
                for course in courses:
                    if course['ccode'] not in ccodes:
                        ccodes.append(course['ccode'])
        for ccode in ccodes:
            course = self.get_course_description(ccode)
            if course is not None:
                result.append(self.get_course_description(ccode))
        return result

    def query_by_course_time(self, params: dict) -> list:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'TaipeiTech CES Crawler',
            'Referer': TaipeiTechCourseCrawler.query_course_url,
            'Origin': 'http://aps.ntut.edu.tw'
        }
        # fuck big 5 encoding
        data = ''
        for key in params:
            data += '&{}={}'.format(key, parse.quote_plus(str(params[key]), encoding='BIG5'))
        data = data.strip('&')
        response = requests.post(
            TaipeiTechCourseCrawler.query_course_url,
            data=data,
            headers=headers
        )
        if response.status_code == requests.codes.ok:
            return self._parse_course(response.text)
        else:
            print('None')

class MailSender:

    smtp = SETTING['MAIL_SMTP']
    sender = SETTING['MAIL_SENDER']
    password = SETTING['MAIL_SENDER_PASSWORD']
    template = """
<p>Dear, {}</p>
<p>感謝您註冊 TaipeiTech CES，請點擊以下連結完成註冊。</p>
<a href="{}">{}</a>
<p>Sincerely, TaipeiTech CES 團隊</p>
<p>(此封信為系統自動寄送，請勿回信)</p>
"""

    
    def send(self, content, receiver):
        message = MIMEText(content, 'html')
        message['From'] = 'TaipeiTechCES'
        message['To'] = '<{}>'.format(receiver)
        message['Subject'] = 'TapeiTechCES 北科課程評價平台 註冊認證'

        msg_full = message.as_string()

        server = smtplib.SMTP(MailSender.smtp)
        server.starttls()
        server.login('t104590048', MailSender.password)
        server.sendmail(
            MailSender.sender,
            [
                receiver
            ],
            msg_full
        )
        server.quit()

if __name__ == '__main__':
    c = TaipeiTechCourseCrawler()
    '''
    params = {
        'stime': 0,
        'year': 106,
        'matric': "'1','5','6','7','8','9'",
        'sem': 1,
        'unit': '**',
        'cname': '程式',
        'ccode': '',
        'tname': '',
        'D0': 'ON',
        'D1': 'ON',
        'D2': 'ON',
        'D3': 'ON',
        'D4': 'ON',
        'D5': 'ON',
        'D6': 'ON',
        'P1': 'ON',
        'P2': 'ON',
        'P3': 'ON',
        'P4': 'ON',
        'P5': 'ON',
        'P6': 'ON',
        'P7': 'ON',
        'P8': 'ON',
        'P9': 'ON',
        'P10': 'ON',
        'P11': 'ON',
        'P12': 'ON',
        'P13': 'ON',
        'search': '開始查詢'
    }
    c.query(params)
    c.get_course_description('5903301')
    '''
    sender = MailSender()
    sender.send(MailSender.template, 't104590048@ntut.edu.tw')