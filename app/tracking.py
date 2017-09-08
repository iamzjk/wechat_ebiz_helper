# -*- coding: utf-8 -*-
'''
    Tracking Status Class
'''

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

    def run(self):
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
                    statuses.append(content.text + child.text)
                    if content.text.startswith('国内速运'):
                        forward_tracking = child.text
            else:
                statuses.append(content.text)

        # TODO: parse EMS and append to statuses
        # if forward_tracking:
        #     try:
        #         ems = EMS(forward_tracking)
        #         ems_html = ems.get_html()
        #         ems.parse_html(ems_html)
        #     except Exception:
        #         pass

        headers = ['time', 'status', 'reporter']
        return self.parse_statuses(statuses, headers)


class EMS(Tracking):
    '''
        EMS
    '''
    # 'https://www.kuaidi100.com/query?type=ems&postid={tracking}&id=1&valicode=&temp='
    tracking_base_url = (
        'http://www.kuaidi.com/index-ajaxselectcourierinfo-{tracking}-ems.html'
    )

    def get_html(self):
        '''
            Getting HTML String From Tracking URL
        '''

        response = requests.get(self.tracking_url, headers=self.header)
        print(response.text)
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
    html = tracking.get_html()
    parsed = tracking.parse_html(html)
    print(parsed)
