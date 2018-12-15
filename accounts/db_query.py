from django.db import connection

cursor = connection.cursor()


def get_products():
    goods = []
    # 打开数据库连接
    try:
        # 使用 execute() 方法执行 SQL 查询
        cursor.execute("call quiry_goods();")
        # 使用获取单全部数据
        data_rows = cursor.fetchall()

        for row in data_rows:
            r = {'PName': row[0], 'Pid': row[1], 'price': row[2], 'num': row[3], 'BName': row[4]}
            goods.append(r)
    except Exception as e:
        raise e

    return goods


def get_supply_goods():
    goods = []
    # 打开数据库连接
    try:
        # 使用 execute() 方法执行 SQL 查询
        cursor.execute("call query_supply();")
        # 使用获取单全部数据
        data_rows = cursor.fetchall()

        for row in data_rows:
            r = {'num': row[0], 'price': row[1], 'pid': row[2], 'pname': row[3], 'sid': row[4], 'sname': row[5]}
            goods.append(r)
    except Exception as e:
        raise e

    return goods


def get_staff(bid, is_s_manager=False):
    staffs = []
    if is_s_manager:
        try:
            # 使用 execute() 方法执行 SQL 查询
            cursor.execute("call query_staff_Smanage();")
            # 使用获取单全部数据
            data_rows = cursor.fetchall()

            for row in data_rows:
                # StaNO_id,StaName,Position,BID_id,tel
                r = {'id': row[0], 'name': row[1], 'position': row[2], 'bid': row[3], 'tel': row[4]}
                staffs.append(r)
        except Exception as e:
            raise e

        return staffs
    else:
        try:
            # 使用 execute() 方法执行 SQL 查询
            cursor.execute("call query_staff_Branch(" + bid + ");")
            # 使用获取单全部数据
            data_rows = cursor.fetchall()

            for row in data_rows:
                # StaNO_id,StaName,Position,BID_id,tel
                r = {'id': row[0], 'name': row[1], 'position': row[2], 'bid': row[3], 'tel': row[4]}
                staffs.append(r)
        except Exception as e:
            raise e

        return staffs
