from django.db import connection

cursor = connection.cursor()


def buy_goods(pid, bname, num, uid):
    try:
        cursor.execute("call buy_branch(" + pid + "," + bname + ","+ num + "," + uid)
    except Exception as e:
        raise e