from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, password=None, right=0):
        user = self.model(
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
    id=models.AutoField(primary_key=True)
    right=models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    def __str__(self):
        return self.id

    def get_id(self):
        return self.id


class SMANAGE(MyBaseUser):
    SMID       =models.ForeignKey(MyBaseUser, related_name="SMANAGE_id",primary_key=True,on_delete=models.CASCADE)




class Branch(MyBaseUser):
    BID       =models.ForeignKey(MyBaseUser, related_name="Branch_id",primary_key=True,on_delete=models.CASCADE)
    Bname     =models.CharField(max_length=20)
    Baddress  =models.CharField(max_length=20)
    Tel       =models.IntegerField
    SMID      =models.ForeignKey(SMANAGE,on_delete=models.CASCADE)


class Client(MyBaseUser):
    CID       =models.ForeignKey(MyBaseUser, related_name="Client_id",primary_key=True,on_delete=models.CASCADE)
    CPassword =models.CharField(max_length=20)
    CName     =models.CharField(max_length=20)
    Tel       =models.IntegerField

class Stuff(MyBaseUser):
    StaNO     =models.ForeignKey(MyBaseUser, related_name="Stuff_id",primary_key=True,on_delete=models.CASCADE)
    SPassword =models.CharField(max_length=20)
    StaName   =models.CharField(max_length=20)
    Position  =models.CharField(max_length=20)
    BID       =models.ForeignKey(Branch,on_delete=models.CASCADE)

class Goods(models.Model):
    PID       =models.IntegerField(primary_key=True)
    PName     =models.CharField(max_length=20)
    price     =models.FloatField
    BID       =models.ForeignKey(Branch,on_delete=models.CASCADE)

class Product(models.Model):
    PID       =models.IntegerField(primary_key=True)
    PName     =models.CharField(max_length=20)
    PTime     =models.DateTimeField(auto_now=False)

class Supplier(models.Model):
    SuppID    =models.IntegerField(primary_key=True)
    tel       =models.IntegerField
    Suppaddress =models.CharField(max_length=20)

class repository(models.Model):
    SuppID    =models.ForeignKey(Supplier,on_delete=models.CASCADE)
    PID       =models.ForeignKey(Product,on_delete=models.CASCADE)
    class Meta:
        unique_together=("SuppID","PID")

class Supply(models.Model):
    SuppID    =models.ForeignKey(Supplier,on_delete=models.CASCADE)
    SMID      =models.ForeignKey(SMANAGE,on_delete=models.CASCADE)
    PID       =models.ForeignKey(Product,on_delete=models.CASCADE)
    Name = models.CharField(max_length=20)
    Time = models.DateTimeField(auto_now=False)
    BID  =models.ForeignKey(Branch,on_delete=models.CASCADE)
    class Meta:
        unique_together=("SuppID","SMID")

class Record(models.Model):
    CID       =models.ForeignKey(Client,on_delete=models.CASCADE)
    PID       =models.ForeignKey(Goods,on_delete=models.CASCADE)
    PName     = models.CharField(max_length=20)
    BID       =models.ForeignKey(Branch,on_delete=models.CASCADE)
    DateTime  =models.DateTimeField(auto_now=False)
    price     =models.FloatField
    class Meta:
        unique_together=("CID","PID")
