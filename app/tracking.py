'''
    Tracking Status Class
'''

from lxml.html import fromstring
import urllib.request


class Tracking():

    def __init__(self, tracking):
        self.tracking = tracking
        self.tracking_base_url = {
            'jinmei': 'http://www.jingexpress.com/TrackSearch.aspx?TXT_TRACKNO={tracking}',
            'ems': 'http://www.kuaidi.com/index-ajaxselectcourierinfo-{tracking}-ems.html',
            'qianxi': 'http://www.qx-ex.com/cgi-bin/GInfo.dll?EmmisTrack&w=qianxi&cno={tracking}'
        }
        self.header = {'User-Agent': 'Mozilla/5.0'}

    def run(self):
        status = self.get_response()
        parsed = self.parse_status(status)
        return parsed

    def get_response(self):
        tracking_url = self.tracking_base_url['jinmei'].format(
            tracking=self.tracking)

        req = urllib.request.Request(tracking_url, headers=self.header)
        response = urllib.request.urlopen(req)
        html = str(response.read(), 'utf-8')

        root = fromstring(html)
        contents = root.xpath("//td")

        status = []
        for content in contents:
            if len(content):
                for child in content:
                    status.append(content.text + child.text)
            else:
                status.append(content.text)

        return status[3:]

    def parse_status(self, status):
        parsed = []
        for i in range(0, len(status), 3):
            headers = ['time', 'status', 'reporter']
            dct = dict(zip(headers, status[i:i + 3]))
            parsed.append(dct)

        return parsed


class JinMei(Tracking):
    

class EMS(Tracking):


class QianXi(Tracking):
    


if __name__ == '__main__':
    tracking = Tracking('8000118043')
    status = tracking.get_response()
    parsed = tracking.parse_status(status)
    print(parsed)
