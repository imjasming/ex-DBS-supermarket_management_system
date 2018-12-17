from django.db import connection

cursor = connection.cursor()


def buy_goods(pid, bname, num, uid):
    try:
        statement = "call buy_branch(%s,'%s',%s,%d);" % (pid, bname, num, uid)
        cursor.execute(statement)
        # cursor.callproc('buy_branch', (pid, bname, num, uid,))  # 注意参数应该是一个元组
        # connection.connection.commit()  # 调用存储过程后，确定要进行commit执行
    except Exception as e:
        raise e


def change_goods_price(bname, pid, price):
    try:
        statement = "call modify_price('%s',%s,%s);" % (bname, pid, price)
        cursor.execute(statement)
    except Exception as e:
        raise e
