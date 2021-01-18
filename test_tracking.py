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
        {"time": "", "status": "国内快递公司：顺丰速递,单号："},
        {"time": "", "status": "SF1163587967471"},
    ]
    assert len(parsed) == len(expected)
    assert parsed == expected


def test_tracking_usbbgo_format2():
    tracking = Tracking.get_tracking_object("BG103416882", "USBBGO")
    parsed = tracking.track()
    expected = [
        {"time": "1/5/2020 12:10:09 PM", "status": "运单创建成功"},
        {"time": "1/6/2021 1:47:23 PM", "status": "包裹已揽收,待分拣。操作人【Jason】"},
        {"time": "1/6/2021 1:47:23 PM", "status": "分拣完毕,待发货。操作人【Becks】"},
        {"time": "1/7/2021 2:45:17 PM", "status": "已出库,货物运往LAX国际机场。交接人【自营卡车司机JAX】"},
        {"time": "1/7/2021 2:52:04 PM", "status": "货物操作完毕，待运往LAX机场。操作人【洛杉矶操作中心待出库】"},
        {"time": "1/9/2021 2:52:51 AM", "status": "航班起飞中，目的地清关口岸。操作人【国际出口发展部】"},
        {"time": "1/10/2021 9:29:31 PM", "status": "第三方机场转机清关口岸中。操作人【国际出口发展部】"},
        {"time": "1/11/2021 11:44:25 AM", "status": "航班到达清关口岸,提货完毕, 等待申报。负责人【国际进口事业部】"},
        {"time": "1/11/2021 9:01:17 PM", "status": "申报完毕,等待海关审核。负责人【国际进口事业部Grace Wu】"},
        {"time": "1/11/2021 9:03:48 PM", "status": "境外包裹到达,海关集中消毒.请耐心等待。"},
        {
            "time": "1/13/2021 2:06:45 AM",
            "status": "海关清关结束，待转国内转运中心提货派送中。负责人【国际进口事业部Alison Zhao】",
        },
        {"time": "", "status": "转运至：中通快递（73145722693189）"},
        {
            "time": "2021-01-14 14:03:58",
            "status": "【青岛市场一部】（0532-67774065） 的 xt高（18563982239） 已揽收",
        },
        {"time": "2021-01-14 14:04:03", "status": "快件离开 【青岛市场一部】 已发往 【青岛中转部】"},
        {"time": "2021-01-14 16:54:15", "status": "快件已经到达 【青岛中转部】"},
        {"time": "2021-01-14 19:03:07", "status": "快件离开 【青岛中转部】 已发往 【宁波中转部】"},
        {"time": "2021-01-16 03:22:58", "status": "快件离开 【潍坊中转部】 已发往 【绍兴中转部】"},
        {"time": "2021-01-16 20:22:30", "status": "快件已经到达 【绍兴中转部】"},
        {"time": "2021-01-16 22:32:12", "status": "快件离开 【绍兴中转部】 已发往 【宁波中转部】"},
        {"time": "2021-01-16 22:33:23", "status": "快件已经到达 【宁波中转部】"},
        {"time": "2021-01-16 22:43:55", "status": "快件离开 【宁波中转部】 已发往 【奉化】"},
        {"time": "2021-01-17 05:12:45", "status": "快件已经到达 【奉化】"},
        {
            "time": "2021-01-17 08:04:50",
            "status": "【奉化】 的何佳乐（17816197660） 正在第1次派件, 请保持电话畅通,并耐心等待（95720为中通快递员外呼专属号码，请放心接听）",
        },
        {
            "time": "2021-01-17 13:14:55",
            "status": "快件已在 【奉化】 签收, 签收人: 邮政收发章, 如有疑问请电联:（17816197660）, 投诉电话:（0574-88903335）, 您的快递已经妥投。风里来雨里去, 只为客官您满意。上有老下有小, 赏个好评好不好？【请在评价快递员处帮忙点亮五颗星星哦~】",
        },
    ]
    assert parsed == expected
