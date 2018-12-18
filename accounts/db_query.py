from django.db import connection
import json
import datetime

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
    try:
        cursor.execute("call query_staff_request();")
        data_rows = cursor.fetchall()

        i = 0
        for row in data_rows:
            r = {'bid': row[0], 'bname': row[1], 'sname': row[2],
                 'uid': row[3], 'rid': row[4], 'status': row[5], 'row': i}
            requests.append(r)
            i += 1
    except Exception as e:
        raise e
    return json.dumps(requests)


def get_add_goods_request_json():
    requests = []
    try:
        cursor.execute("call query_goods_request();")
        data_rows = cursor.fetchall()

        i = 0
        for row in data_rows:
            # date = row[4].strftime("%Y-%m-%d %H:%M:%S")
            r = {'rid': row[0], 'bid': row[1], 'pid': row[2], 'num': row[3],
                 'uid': row[4], 'pname': row[5], 'price': row[6], 'bname': row[7], 'status': row[8],
                 'row': i}
            requests.append(r)
            i += 1
    except Exception as e:
        raise e
    return json.dumps(requests)


def get_record_by_statement(statement):
    records = []
    try:
        cursor.execute(statement)
        data_rows = cursor.fetchall()

        i = 0
        for row in data_rows:
            date = row[3].strftime("%Y-%m-%d %H:%M:%S")
            r = {'pname': row[0], 'num': row[1], 'price': row[2],
                 'time': date, 'bname': row[4], 'uname': row[5], 'row': i}
            records.append(r)
            i += 1
    except Exception as e:
        raise e
    return json.dumps(records)


def get_all_record_json():
    statement = "call query_record();"
    return get_record_by_statement(statement)


def get_branch_record_json(uid):
    statement = "call quert_goods_stfforbranch(%d);" % uid
    return get_record_by_statement(statement)


def get_customer_record_json(uid):
    statement = "call query_customer_record(%d);" % uid
    return get_record_by_statement(statement)
