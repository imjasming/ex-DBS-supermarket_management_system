from django.db import connection

cursor = connection.cursor()


def buy_goods(pid, bname, num, uid):
    statement = "call buy_branch(%s,'%s',%s,%d);" % (pid, bname, num, uid)
    cursor.execute(statement)
    # cursor.callproc('buy_branch', (pid, bname, num, uid,))  # 注意参数应该是一个元组
    # connection.connection.commit()  # 调用存储过程后，确定要进行commit执行


def change_goods_price(bname, pid, price):
    statement = "call modify_price('%s',%s,%s);" % (bname, pid, price)
    cursor.execute(statement)


def request_fire_staff(uid, staff_no):
    statement = "call request_staff_branch(%s,%s);" % (uid, staff_no)
    cursor.execute(statement)
