from django.db import connection
import json

cursor = connection.cursor()


def get_branch_goods_json(uid):
    goods = []
    try:
        statement = "call query_goods_branch(%s);" % uid
        cursor.execute(statement)
        data_rows = cursor.fetchall()

        i = 0
        for row in data_rows:
            r = {'PName': row[0], 'Pid': row[1], 'price': row[2], 'num': row[3], 'BName': row[4], 'row': i}
            goods.append(r)
            i += 1
    except Exception as e:
        raise e

    return json.dumps(goods)


def get_goods_json():
    goods = []
    try:
        cursor.execute("call query_goods();")
        data_rows = cursor.fetchall()

        i = 0
        for row in data_rows:
            r = {'PName': row[0], 'Pid': row[1], 'price': row[2], 'num': row[3], 'BName': row[4], 'row': i}
            goods.append(r)
            i += 1
    except Exception as e:
        raise e

    return json.dumps(goods)


def get_supply_goods_json():
    goods = []
    try:
        cursor.execute("call query_supply();")
        data_rows = cursor.fetchall()

        i = 0
        for row in data_rows:
            r = {'num': row[0], 'price': row[1], 'pid': row[2], 'pname': row[3], 'sid': row[4], 'sname': row[5],
                 'row': i}
            goods.append(r)
            i += 1
    except Exception as e:
        raise e

    return json.dumps(goods)


def get_staff_json(uid, is_s_manager=False):
    staffs = []
    if is_s_manager:
        try:
            cursor.execute("call query_staff_Smanage();")
            data_rows = cursor.fetchall()

            i = 0
            for row in data_rows:
                # StaNO_id,StaName,Position,BID_id,tel
                r = {'sid': row[0], 'name': row[1], 'position': row[2], 'bid': row[3], 'tel': row[4], 'row': i}
                staffs.append(r)
                i += 1
        except Exception as e:
            raise e

    else:
        try:
            cursor.execute("call query_staff_Branch(%d)" % uid)
            data_rows = cursor.fetchall()

            i = 0
            for row in data_rows:
                # StaNO_id,StaName,Position,BID_id,tel
                r = {'sid': row[0], 'name': row[1], 'position': row[2], 'bid': row[3], 'bname': row[4], 'tel': row[5],
                     'row': i}
                staffs.append(r)
                i += 1
        except Exception as e:
            raise e

    return json.dumps(staffs)


def get_staff_fire_request_json():
    requests = []
    cursor.execute("call query_staff_request();")
    data_rows = cursor.fetchall()

    i = 0
    for row in data_rows:
        r = {'bid': row[0], 'bname': row[1], 'sname': row[2], 'time': row[3],
             'uid': row[4], 'rid': row[5], 'row': i}
        requests.append(r)
        i += 1
    return json.dumps(requests)


def get_add_goods_request_json():
    requests = []
    cursor.execute("call query_goods_request();")
    data_rows = cursor.fetchall()

    i = 0
    for row in data_rows:
        r = {'rid': row[0], 'bid': row[1], 'pid': row[2], 'num': row[3],
             'time': row[4], 'uid': row[5], 'pname': row[6], 'price': row[7], 'bname': row[8], 'row': i}
        requests.append(r)
        i += 1
    return json.dumps(requests)
