from django.db import connection


def get_products():
    goods = []
    # 打开数据库连接
    cursor = connection.cursor()
    try:
        # 使用 execute() 方法执行 SQL 查询
        cursor.execute("call quiry_goods();")
        # 使用获取单全部数据
        dataRows = cursor.fetchall()

        for row in dataRows:
            r = {'PName': row[0], 'Pid': row[1], 'price': row[2], 'num': row[3], 'BName': row[4]}
            goods.append(r)
    except Exception as e:
        raise e

    return goods
