from django.db import connection
import json

cursor = connection.cursor()


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


def get_staff_json(bid, is_s_manager=False):
    staffs = []
    if is_s_manager:
        try:
            cursor.execute("call query_staff_Smanage();")
            data_rows = cursor.fetchall()

            i = 0
            for row in data_rows:
                # StaNO_id,StaName,Position,BID_id,tel
                r = {'id': row[0], 'name': row[1], 'position': row[2], 'bid': row[3], 'tel': row[4], 'row': i}
                staffs.append(r)
                i += 1
        except Exception as e:
            raise e

    else:
        try:
            cursor.execute("call query_staff_Branch(" + bid + ");")
            data_rows = cursor.fetchall()

            i = 0
            for row in data_rows:
                # StaNO_id,StaName,Position,BID_id,tel
                r = {'id': row[0], 'name': row[1], 'position': row[2], 'bid': row[3], 'tel': row[4], 'row': i}
                staffs.append(r)
                i += 1
        except Exception as e:
            raise e

    return json.dumps(staffs)
