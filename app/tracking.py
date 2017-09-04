'''
    Tracking Status Class
'''

from lxml.html import fromstring
import urllib.request


class Tracking():

    def __init__(self, tracking):
        self.tracking = tracking
        self.tracking_url =\
            'http://www.jingexpress.com/TrackSearch.aspx?TXT_TRACKNO={tracking}'.format(tracking=self.tracking)
        self.header = {'User-Agent': 'Mozilla/5.0'}

    def run(self):
        status = self.get_response()
        parsed = self.parse_status(status)
        return parsed

    def get_response(self):
        req = urllib.request.Request(self.tracking_url, headers=self.header)
        response = urllib.request.urlopen(req)
        html = str(response.read(),'utf-8')

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
            dct = dict(zip(headers, status[i : i+3]))
            parsed.append(dct)

        return parsed

    # def get_tracking_html(self):
    #     req = urllib.request.Request(self.tracking_url, headers=self.header)
    #     response = urllib.request.urlopen(req)
    #     html = str(response.read(),'utf-8')


if __name__ == '__main__':
    tracking = Tracking()
    status = tracking.get_response()
    parsed = tracking.parse_status(status)
    print(parsed)