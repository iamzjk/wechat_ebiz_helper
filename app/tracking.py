# -*- coding: utf-8 -*-
'''
    Tracking Status Class
'''

from datetime import datetime
import json
from lxml.html import fromstring
import requests

KUAIDI100_CARRIERS = {
    '申通': 'shentong',
    '圆通': 'yuantong',
    '顺丰': 'shunfeng',
    '中通': 'zhongtong',
    'EMS': 'ems',
    '韵达': 'yunda',
    '天天': 'tiantian',
}

HUAREN_CARRIERS = ['锦美', '千喜']

SUPPORTED_CARRIERS = HUAREN_CARRIERS + list(KUAIDI100_CARRIERS.keys())


def tracking_shipment(tracking_number, carrier):

    now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    if carrier in HUAREN_CARRIERS:
        tracking_obj = Tracking.get_tracking_object(tracking_number, carrier)
        statuses = tracking_obj.track()
    elif carrier in KUAIDI100_CARRIERS:
        statuses = track_via_kuaidi100(tracking_number, carrier)
    else:
        error_msg = '暂时不支持查询<{0}>'.format(carrier)
        statuses = [{'time': now, 'status': error_msg}]

    if not statuses:
        statuses = [{'time': now, 'status': '暂无物流状态， 请稍后再试。'}]

    return statuses


def track_via_kuaidi100(tracking_number, carrier):
    """
        tracking shipment using kuaidi100 api
    """

    base_api_url = (
        'https://www.kuaidi100.com/query?type={carrier_code}&postid={tracking_number}'
    )

    if carrier not in KUAIDI100_CARRIERS:
        return []

    state_code_map = {
        "0": "在途",  # 即货物处于运输过程中
        "1": "揽件",  # 货物已由快递公司揽收并且产生了第一条跟踪信息
        "2": "疑难",  # 货物寄送过程出了问题
        "3": "签收",  # 收件人已签收
        "4": "退签",  # 即货物由于用户拒签、超区等原因退回，而且发件人已经签收
        "5": "派件",  # 即快递正在进行同城派件
        "6": "退回",  # 货物正处于退回发件人的途中
    }

    status_code_map = {
        "0": "物流单暂无结果",
        "1": "查询成功",
        "2": "接口出现异常",
    }

    header = {
        'User-Agent': 'Mozilla/5.0',
    }

    api_url = base_api_url.format(
        carrier_code=KUAIDI100_CARRIERS[carrier],
        tracking_number=tracking_number
    )

    response = requests.get(api_url, headers=header)
    data = json.loads(response.text)

    statuses = []
    for status in data['data']:
        new_status = {}
        new_status['time'] = status['time']
        new_status['status'] = status['context']
        new_status['reporter'] = status['location']
        statuses.append(new_status)

    return statuses


class Tracking():
    '''
        Base Tracking Class
    '''

    tracking_base_url = '{tracking}'
    header = {
        'User-Agent': 'Mozilla/5.0',
    }

    def __init__(self, tracking):
        self.tracking = tracking
        self.tracking_url = self.tracking_base_url.format(tracking=tracking)

    @staticmethod
    def get_tracking_object(tracking, carrier):

        if carrier == '锦美':
            return JinMei(tracking)
        elif carrier is None:
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

        return parsed[::-1]


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

        # forward_tracking = None
        statuses = []
        for content in contents:
            if len(content):
                for child in content:
                    statuses.append('EMS' + content.text + child.text)
                    # if content.text.startswith('国内速运'):
                    #     forward_tracking = child.text
            else:
                statuses.append(content.text)

        headers = ['time', 'status', 'reporter']
        parsed = self.parse_statuses(statuses, headers)

        # if forward_tracking:
        #     try:
        #         ems = EMS(forward_tracking)
        #         ems_statuses = ems.track()
        #         parsed += ems_statuses
        #     except Exception as err:
        #         print(err)

        return parsed


# class EMS(Tracking):
#     '''
#         EMS
#     '''

#     tracking_base_url = (
#         'https://www.kuaidi100.com/query?type=ems&postid={tracking}&id=1&valicode=&temp='
#     )

#     def track(self):
#         '''
#             EMS tracking
#         '''
#         response = json.loads(self.get_html())

#         statuses = []
#         for status in response['data']:
#             new_status = {}
#             new_status['time'] = status['time']
#             new_status['status'] = status['context']
#             new_status['reporter'] = status['location']
#             statuses.append(new_status)

#         return statuses[::-1]

#     def get_html(self):
#         '''
#             Getting HTML String From Tracking URL
#         '''

#         response = requests.get(self.tracking_url, headers=self.header)
#         return response.text


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


# class YuanTong(Tracking):
#     '''
#         圆通
#     '''

#     tracking_base_url = (
#         'https://www.kuaidi100.com/query?type=yuantong&postid={tracking}'
#     )

#     def track(self):
#         '''
#             圆通 tracking
#         '''
#         response = json.loads(self.get_html())

#         statuses = []
#         for status in response['data']:
#             new_status = {}
#             new_status['time'] = status['time']
#             new_status['status'] = status['context']
#             new_status['reporter'] = status['location']
#             statuses.append(new_status)

#         return statuses[::-1]

#     def get_html(self):
#         '''
#             Getting HTML String From Tracking URL
#         '''

#         response = requests.get(self.tracking_url, headers=self.header)
#         return response.text


if __name__ == '__main__':
    # 8000118040
    # QX900355101
    tracking = Tracking.get_tracking_object('8000118040', '锦美')
    parsed = tracking.track()
    print(parsed)
