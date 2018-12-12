from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, tel=0, right=0):
        user = self.model(
            username=username,
            tel=tel,
            right=right
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyBaseUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    right = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'id'
    
    objects = MyUserManager()

    def __str__(self):
        return self.id

    def get_id(self):
        return self.id


class Branch(models.Model):  # 分支超市模型
    BID = models.OneToOneField(MyBaseUser, related_name="Branch_id", primary_key=True, on_delete=models.CASCADE)
    Bname = models.CharField(max_length=20)
    Baddress = models.CharField(max_length=20)
    Tel = models.IntegerField()
    StaNO = models.IntegerField()  # 经理编号，经理是员工的一员，体现经理的存在是Staff表中的Position一项是manage


class Customer(models.Model):  # 客户端模型
    CID = models.OneToOneField(MyBaseUser, related_name="Client_id", primary_key=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, unique=True)
    tel = models.IntegerField()


class Staff(models.Model):  # 员工模型
    StaNO = models.OneToOneField(MyBaseUser, related_name="Stuff_id", primary_key=True, on_delete=models.CASCADE)
    SPassword = models.CharField(max_length=20)
    StaName = models.CharField(max_length=20)
    Position = models.CharField(max_length=20)  # 如果职位这项是manage，下面的BID默认为属于该Staff管理
    BID = models.ForeignKey(Branch, on_delete=models.CASCADE)


class Goods(models.Model):  # 商品模型
    PID = models.IntegerField(primary_key=True)  # 工厂编码,同一商品的编码是一样，例如五百瓶冰红茶将只有一个ID，而其属性在GOODS表中只有这三项，数量存在下面两个表中
    PName = models.CharField(max_length=20)
    price = models.FloatField()


class Supplier(models.Model):  # 商品供货商的模型
    SuppID = models.IntegerField(primary_key=True)
    Suppname = models.CharField(max_length=20)
    tel = models.IntegerField
    Suppaddress = models.CharField(max_length=20)


class repository(models.Model):  # 商品存在供货商的仓库的模型
    SuppID = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    PID = models.ForeignKey(Goods, on_delete=models.CASCADE)
    num = models.IntegerField()
    price = models.FloatField()

    class Meta:
        unique_together = ("SuppID", "PID")


class store(models.Model):  # 商品存分支超市的仓库的模型
    BID = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    PID = models.ForeignKey(Goods, on_delete=models.CASCADE)
    num = models.IntegerField()
    price = models.FloatField()

    class Meta:
        unique_together = ("BID", "PID")


class Supply(models.Model):  # 商品从供货商到具体分支超市的模型
    SuppID = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    SMID = models.ForeignKey(Staff, on_delete=models.CASCADE)  # 显示是哪个总部管理者确认的进货请求
    PID = models.ForeignKey(Goods, on_delete=models.CASCADE)
    PName = models.CharField(max_length=20)
    price = models.FloatField()
    num = models.IntegerField()
    Time = models.DateTimeField(auto_now=False)  # 进货日期
    BID = models.ForeignKey(Branch, on_delete=models.CASCADE)  # 具体的分支超市

    class Meta:
        unique_together = ("SuppID", "SMID", "PID")


class Record(models.Model):  # customer购买记录模型
    RID = models.IntegerField(primary_key=True, default=0)  # 记录编号，类似于订单码
    CID = models.ForeignKey(Customer, on_delete=models.CASCADE)  # 客户端编号
    PID = models.ForeignKey(Goods, on_delete=models.CASCADE)  # 商品编号
    PName = models.CharField(max_length=20)  # 商品名称
    BID = models.ForeignKey(Branch, on_delete=models.CASCADE)
    Time = models.DateTimeField(auto_now=False)
    price = models.FloatField()


class sell(models.Model):  # 员工销售商品的记录
    SID = models.IntegerField(primary_key=True, default=0)  # 记录编号，类似于订单码
    PID = models.ForeignKey(Goods, on_delete=models.CASCADE)  # 商品编号
    StaNO = models.ForeignKey(Staff, on_delete=models.CASCADE)  # 员工编号
    PName = models.CharField(max_length=20)  # 商品名称
    num = models.IntegerField()
    price = models.FloatField()
    BID = models.ForeignKey(Branch, on_delete=models.CASCADE)
    Time = models.DateTimeField(auto_now=False)  # 销售日期
