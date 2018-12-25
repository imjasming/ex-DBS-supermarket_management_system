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


def request_add_goods(pid, uid, num, sid):
    statement = "call request_buygoods_branch(%s,%d,'%s',%s);" % (pid, uid, num, sid)
    cursor.execute(statement)


def response_fire_staff(rid, status):
    statement = "call responce_staffmanage_request(%s,'%s');" % (rid, status)
    cursor.execute(statement)


def response_add_goods(rid, uid, status):
    statement = "call responce_supply_request(%s,%d,'%s');" % (rid, uid, status)
    cursor.execute(statement)


def add_to_shopping_cart(uid, pid, pname, bname, num, price):
    statement = "Insert into buycar(BNAME,num,uid,price,PID,PNAME) values('%s',%s,%d,%s,%s,%s);" % (
        bname, num, uid, price, pid, pname)
    cursor.execute(statement)


def remove_cart_item_by_id(rid):
    statement = "delete from buycar where id=(%s);" % rid
    cursor.execute(statement)
