from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.core.exceptions import ValidationError
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError('Users must have a  phone number')

        user = self.model(
            phone=self.normalize_userid(phone),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        """
        Creates and saves a superuser with the given phone and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.save(using=self._db)
        return user


class UserRegister(AbstractBaseUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    user_name = models.CharField(max_length=150)
    address = models.CharField(max_length=250)
    email = models.EmailField(verbose_name='email address',max_length=100)
    password = models.CharField(max_length=150)
    phone = models.CharField(max_length=150,unique=True)
    acno = models.CharField(max_length=150,unique=True)
    ifsc = models.CharField(max_length=150)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = UserManager()


class UserAccount(models.Model):
    user_name = models.CharField(max_length=150)
    user = models.ForeignKey(UserRegister, related_name = "User_Account", on_delete = False)
    acno = models.CharField(max_length=150,unique=True)
    ifsc = models.CharField(max_length=150)
    balance = models.FloatField(max_length = 20, default = 10000)
    cashback = models.FloatField(max_length = 150, default = 0)




class LoanApplication(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    acno = models.CharField(max_length=150)
    loan_amount = models.CharField(max_length=150)
    tennure = models.CharField(max_length=150)
    loan_id = models.FloatField(max_length = 150, default = 10000000)

class MoneyTransfer(models.Model):
    phone = models.CharField(max_length=150)
    amount_received =  models.ForeignKey(UserRegister, related_name = "User_moneyrecievedfrom", on_delete = False, null=True)
    account = models.ForeignKey(UserAccount, related_name = "User_moneytransfer", on_delete = False, null=True)
    amount = models.FloatField(max_length = 150)

class MoneyDeposit(models.Model):
    # acno = models.CharField(max_length=150)
    account = models.ForeignKey(UserAccount, related_name = "User_moneydeposit", on_delete = False, null=True)
    amount = models.FloatField(max_length = 150)
