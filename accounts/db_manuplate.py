from django.db import connection

cursor = connection.cursor()


def buy_goods(pid, bname, num, uid):
    try:
        statement = "call buy_branch(%s,'%s',%s,%d);" % (pid, bname, num, uid)
        print(statement)
        cursor.execute(statement)
        # cursor.callproc('buy_branch', (pid, bname, num, uid,))  # 注意参数应该是一个元组
        connection.connection.commit()  # 调用存储过程后，确定要进行commit执行
    except Exception as e:
        raise e
