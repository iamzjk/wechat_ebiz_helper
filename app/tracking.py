# -*- coding: utf-8 -*-
'''
    Tracking Status Class
'''

import json
from lxml.html import fromstring
import requests


class Tracking():
    '''
        Base Tracking Class
    '''

    tracking_base_url = '{tracking}'
    header = {'User-Agent': 'Mozilla/5.0'}

    def __init__(self, tracking):
        self.tracking = tracking
        self.tracking_url = self.tracking_base_url.format(tracking=tracking)

    @staticmethod
    def get_tracking_object(tracking, carrier):

        if carrier == '锦美':
            return JinMei(tracking)
        elif carrier is None:
            return EMS(tracking)
        elif carrier == 'EMS':
            return EMS(tracking)
        elif carrier == '千喜':
            return QianXi(tracking)
        else:
            return None

    def track(self):
        html = self.get_html()
        return self.parse_html(html)

    def get_html(self):
        '''
            Getting HTML String From Tracking URL
        '''

        response = requests.get(self.tracking_url, headers=self.header)
        return response.text

    def parse_statuses(self, statuses, headers):
        statuses = statuses[3:]
        parsed = []
        for i in range(0, len(statuses), 3):
            headers = headers
            dct = dict(zip(headers, statuses[i:i + 3]))
            parsed.append(dct)

        return parsed


class JinMei(Tracking):
    '''
        锦美
    '''

    tracking_base_url = (
        'http://www.jingexpress.com/TrackSearch.aspx?TXT_TRACKNO={tracking}'
    )

    def parse_html(self, html):
        root = fromstring(html)
        contents = root.xpath("//td")

        forward_tracking = None
        statuses = []
        for content in contents:
            if len(content):
                for child in content:
                    statuses.append('EMS' + content.text + child.text)
                    if content.text.startswith('国内速运'):
                        forward_tracking = child.text
            else:
                statuses.append(content.text)

        headers = ['time', 'status', 'reporter']
        parsed = self.parse_statuses(statuses, headers)

        if forward_tracking:
            try:
                ems = EMS(forward_tracking)
                ems_statuses = ems.track()
            except Exception:
                pass

            parsed += ems_statuses

        return parsed


class EMS(Tracking):
    '''
        EMS
    '''

    tracking_base_url = (
        'https://www.kuaidi100.com/query?type=ems&postid={tracking}&id=1&valicode=&temp='
    )

    def track(self):
        '''
            EMS tracking
        '''
        response = json.loads(self.get_html())

        statuses = []
        for status in response['data']:
            new_status = {}
            new_status['time'] = status['time']
            new_status['status'] = status['context']
            new_status['reporter'] = status['location']
            statuses.append(new_status)

        return statuses[::-1]

    def get_html(self):
        '''
            Getting HTML String From Tracking URL
        '''

        response = requests.get(self.tracking_url, headers=self.header)
        return response.text


class QianXi(Tracking):
    '''
        千喜
    '''

    tracking_base_url = (
        'http://www.qx-ex.com/cgi-bin/GInfo.dll?EmmisTrack&w=qianxi&cno={tracking}'
    )

    def parse_html(self, html):
        root = fromstring(html)
        contents = root.xpath('//table[@id="oTHtable"]//td')

        statuses = [content.text for content in contents]

        statuses[3:] = [status.replace('洛杉矶', '美国') for status in statuses[3:]]

        headers = ['time', 'reporter', 'status']
        return self.parse_statuses(
            statuses, headers=headers)


if __name__ == '__main__':
    # 8000118040
    # QX900355101
    tracking = Tracking.get_tracking_object('8000118040', '锦美')
    parsed = tracking.track()
    print(parsed)
