from app.tracking import Tracking
import pytest


@pytest.mark.skip(reason="no longer in business")
def test_tracking_jinmei():
    tracking = Tracking.get_tracking_object("8000118040", "锦美")
    parsed = tracking.track()
    assert parsed


def test_tracking_qianxi1():
    tracking = Tracking.get_tracking_object("QX900355101", "千喜")
    parsed = tracking.track()
    expected = [
        {
            "time": "2017-09-04 14:17",
            "reporter": "钟楼发投\u3000",
            "status": "已签收,本人 收【钟楼发投】\u3000",
        },
        {
            "time": "2017-09-04 10:29",
            "reporter": "钟楼发投\u3000",
            "status": "【钟楼发投】正在投递,投递员：蒙小军 18591798006\u3000",
        },
        {
            "time": "2017-09-04 07:44",
            "reporter": "钟楼发投\u3000",
            "status": "到达【钟楼发投】\u3000",
        },
        {
            "time": "2017-09-04 07:44",
            "reporter": "钟楼发投\u3000",
            "status": "【钟楼发投】趟车到达\u3000",
        },
        {
            "time": "2017-09-03 16:39",
            "reporter": "西安中心\u3000",
            "status": "离开【西安中心】，下一站【钟楼发投】\u3000",
        },
        {
            "time": "2017-09-03 14:46",
            "reporter": "西安中心\u3000",
            "status": "【西安中心】已经封发\u3000",
        },
        {
            "time": "2017-09-03 13:10",
            "reporter": "西安中心\u3000",
            "status": "到达【西安中心】\u3000",
        },
        {
            "time": "2017-09-02 07:52",
            "reporter": "广州中心\u3000",
            "status": "离开【广州中心】，下一站【西安中心】\u3000",
        },
        {
            "time": "2017-09-02 07:34",
            "reporter": "广州中心\u3000",
            "status": "到达【广州中心】\u3000",
        },
        {
            "time": "2017-09-02 04:43",
            "reporter": "广州中心\u3000",
            "status": "【广州中心】已经封发\u3000",
        },
        {
            "time": "2017-09-01 21:55",
            "reporter": "江门中心\u3000",
            "status": "离开【江门中心】，下一站【广州中心】\u3000",
        },
        {
            "time": "2017-09-01 21:37",
            "reporter": "中国邮政集团公司江门市函件集邮分局\u3000",
            "status": "离开【中国邮政集团公司江门市函件集邮分局】，下一站【江门中心】\u3000",
        },
        {
            "time": "2017-09-01 20:37",
            "reporter": "中国邮政集团公司江门市函件集邮分局\u3000",
            "status": "【广东省中国邮政集团公司江门市函件集邮分局】已经收寄\u3000",
        },
        {"time": "2017-08-11 20:35", "reporter": "中国\u3000", "status": "海关清关中\u3000"},
        {
            "time": "2017-08-08 22:48",
            "reporter": "美国\u3000",
            "status": "包裹离开美国操作中心，发往中国\u3000",
        },
        {
            "time": "2017-08-08 09:20",
            "reporter": "美国\u3000",
            "status": "美国操作中心收到运单信息\u3000",
        },
    ]
    assert parsed == expected


def test_tracking_qianxi2():
    tracking = Tracking.get_tracking_object("QX900489673", "千喜")
    parsed = tracking.track()
    expected = [
        {"time": "2018-08-04 14:11", "reporter": "中国\u3000", "status": "海关清关中\u3000"},
        {
            "time": "2018-08-01 00:57",
            "reporter": "美国\u3000",
            "status": "包裹离开美国操作中心，发往中国\u3000",
        },
        {
            "time": "2018-07-29 22:14",
            "reporter": "美国\u3000",
            "status": "美国操作中心收到运单信息\u3000",
        },
    ]
    assert parsed == expected


@pytest.mark.skip(reason="test tracking number expired")
def test_tracking_fenghai():
    tracking = Tracking.get_tracking_object("FH1688013550", "峰海")
    parsed = tracking.track()
    assert parsed


def test_tracking_beihai():
    tracking = Tracking.get_tracking_object("DB2655122687US", "贝海")
    parsed = tracking.track()
    assert parsed


def test_tracking_meicang():
    tracking = Tracking.get_tracking_object("MC924916", "美仓")
    parsed = tracking.track()
    expected = [
        {
            "time": "2017/12/1 2:18:38",
            "status": "国内快递公司：圆通速递，单号：812117239236",
            "reporter": "工作人员",
        },
        {"time": "2017/12/1 2:13:06", "status": "转国内派送", "reporter": "Admin"},
        {"time": "2017/11/25 3:32:56", "status": "正在清关中", "reporter": "Admin"},
        {"time": "2017/11/23 4:48:57", "status": "二乘转机中", "reporter": "Admin"},
        {"time": "2017/11/21 2:15:29", "status": "飞往国内", "reporter": "Admin"},
        {"time": "2017/11/19 8:45:03", "status": "送往机场", "reporter": "Admin"},
        {"time": "2017/11/17 7:42:37", "status": "运单创建，等待发货", "reporter": "xingguang"},
    ]
    assert parsed == expected


def test_tracking_yueyang():
    tracking = Tracking.get_tracking_object("8000163467", "越洋")
    parsed = tracking.track()
    assert parsed


@pytest.mark.skip(reason="test tracking number expired")
def test_tracking_sifang():
    tracking = Tracking.get_tracking_object("0711XG05", "四方")
    parsed = tracking.track()
    assert parsed


@pytest.mark.skip(reason="Tracking page changed, needs work")
def test_tracking_huazhong():
    tracking = Tracking.get_tracking_object("HZ1904124452SN", "华中")
    parsed = tracking.track()
    assert parsed


def test_tracking_usbbgo_format1():
    tracking = Tracking.get_tracking_object("BG103390720", "USBBGO")
    parsed = tracking.track()
    expected = [
        {"time": "", "status": "目的地:浙江省舟山市"},
        {"time": "12/11/2020 3:49:38 PM", "status": "运单创建"},
        {"time": "12/11/2020 3:49:38 PM", "status": "等待处理"},
        {"time": "12/15/2020 9:32:00 AM", "status": "门店已交接出店"},
        {"time": "12/16/2020 7:32:02 AM", "status": "美国仓库中心已签收"},
        {"time": "12/16/2020 8:39:46 AM", "status": "美国仓库中心称重处理"},
        {"time": "12/17/2020 3:12:11 PM", "status": "美国仓库中心已交接出库发送机场"},
        {"time": "12/19/2020 5:58:03 AM", "status": "飞往中国"},
        {"time": "12/22/2020 9:36:13 PM", "status": "海关清关中"},
        {"time": "12/25/2020 5:28:10 PM", "status": "中国段转运中"},
    ]
    assert parsed == expected


def test_tracking_usbbgo_format1_with_transfer():
    # TODO: add support for transfer tracking
    tracking = Tracking.get_tracking_object("BG103416673", "USBBGO")
    parsed = tracking.track()
    expected = []
    assert parsed[-1]


def test_tracking_usbbgo_format2():
    tracking = Tracking.get_tracking_object("BG103416882", "USBBGO")
    parsed = tracking.track()
    expected = [
        {"time": "1/5/2020 12:10:09 PM", "status": "运单创建成功 "},
        {"time": "1/6/2021 1:47:23 PM", "status": "包裹已揽收,待分拣。操作人【Jason】 "},
        {"time": "1/6/2021 1:47:23 PM", "status": "分拣完毕,待发货。操作人【Becks】 "},
    ]
    assert parsed == expected
