from django.shortcuts import render, redirect
from details.models import UserRegister, LoanApplication, UserAccount, MoneyDeposit, MoneyTransfer
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from random import random, randint
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
import psycopg2

# Create your views here.

# Create your views here.
def Register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        password = request.POST['psw']
        print(password)
        ph = request.POST['ph']
        acno = request.POST['acno']
        ifsc = request.POST['ifsc']

        if UserRegister.objects.filter(phone = ph).exists():

            messages.info(request, "User Already Exist,Please Login with same phone number")
            return redirect('Register')

        else:

            details_user = UserRegister.objects.create(first_name=fname, last_name=lname, user_name=name, address=address, email=email,
            phone=ph, acno=acno, ifsc=ifsc)

            details_user.set_password(password)


            details_user.save()
            details_account = UserAccount(user_name=name, acno=acno, ifsc=ifsc, user=details_user)
            details_account.save()
            messages.info(request, "user Created!")
            return redirect('Register')



    else:
        return render(request, 'register.html')

def About(request):
    return render(request, 'about.html')


def Contact(request):
    return render(request, 'contact.html')


def Term(request):
    return render(request, 'terms.html')


def Login(request):
    if request.method == 'POST':
        ph = request.POST['ph']
        password = request.POST['psw']
        user = UserRegister.objects.filter(phone = ph).first()
        user = authenticate(request, phone = ph, password = password)

        if user is not None:
            messages.info(request, "Logged Succesfully")
            auth.login(request, user)
            return HttpResponseRedirect(reverse('Main'))
        else:
            messages.info(request, "Invalid Phone Number or Password")

            return HttpResponseRedirect(reverse('Login'))



    else:
        return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('/')

def Forgot(request):
    return render(request, 'forgot.html')

def Main(request):
    return render(request, 'main.html')


def Loan(request):
    if request.method == 'POST':
        name = request.POST['name']
        acno = request.POST['acno']
        address = request.POST['address']
        email = request.POST['email']
        ph = request.POST['ph']
        la = request.POST['la']
        tennure = request.POST['tennure']

        loan_id = randint(10000000, 100000000000)

        details_user1 = LoanApplication.objects.create(name=name, address=address, email=email,phone=ph, acno=acno,
         loan_amount=la,tennure=tennure, loan_id = loan_id )

        details_user1.save()
        lid = loan_id

        data3 = {"lid":lid}
        context3 = {"data3":data3}
        messages.info(request, "Loan Applied")


        return render(request, 'loan.html', context3)




    else:
        return render(request, 'loan.html')

def Deposit(request):
    if request.method == 'POST':
        user = UserRegister.objects.filter(id = request.user.id).first()
        useraccount = UserAccount.objects.filter(user_id=user.id).first()
        amount = request.POST.get('amount')
        deposit = MoneyDeposit.objects.create(account_id=useraccount.id, amount = amount)
        deposit.save()
        useraccount.balance = useraccount.balance + float(deposit.amount)
        useraccount.save()

        return redirect('Main')

    else:
        return render(request, 'deposit.html')



def Transfer(request):
    if request.method == 'POST':
        user = UserRegister.objects.filter(id = request.user.id).first()
        useraccount_sender = UserAccount.objects.filter(user_id=user.id).first()
        phone = request.POST.get('ph')
        if UserRegister.objects.filter(phone = phone).exists():

            user_reciever = UserRegister.objects.filter(phone=phone).first()
            useraccount_reciever = UserAccount.objects.filter(user_id=user_reciever.id).first()
            amount = request.POST.get('amount')


            if useraccount_sender.balance <= float(amount) or useraccount_sender.balance <=1000 :
                messages.info(request, "Transaction Failed")
                messages.info(request, "Insufficent balance, Make sure your account have enough balance and maintain a minimum balance of RS.1000")
                messages.info(request, "Thank you for using Easy Pay!, Banking made simple.")
                return HttpResponseRedirect(reverse('Transfer'))

            else:
                useraccount_sender.balance = useraccount_sender.balance - float(amount)
                if useraccount_sender.balance < 1000:
                    messages.info(request, "Transaction Failed, Please maintain a minimum balance of 1000.")
                    return HttpResponseRedirect(reverse('Transfer'))

                else:


                    money = MoneyTransfer.objects.create(amount_received_id = user.id,account_id = useraccount_reciever.id, phone = phone, amount = amount)
                    money.save()
                    amount1 = int(amount)
                    print(amount1)
                    cashback = 0
                    if amount1 > 1000 :
                        cashback = randint(0,200)
                        print("cashback1", cashback)
                    elif amount1 >= 500 and amount1 <= 1000:
                        cashback = randint(0,20)
                        print("cashback2", cashback)
                    elif amount1 >= 150 and amount1 < 500:
                        cashback = randint(0,15)
                        print("cashback3", cashback)
                    else:
                        cashback = randint(0,1)

                    print("cashback",cashback)


                    #return cashback
                    if cashback == 0:
                        messages.info(request, "Better Luck Next Time")

                    useraccount_sender.cashback = useraccount_sender.cashback + cashback;
                    useraccount_sender.balance = useraccount_sender.balance + cashback
                    useraccount_sender.save()
                    useraccount_reciever.balance = useraccount_reciever.balance + float(amount)
                    useraccount_reciever.save()
                    messages.info(request,"Transaction Successfull!")
                    messages.info(request,"Thank you for using Easy pay!, Banking made simple.")






        else:
         messages.info(request,"Invalid Phone Number")
         return HttpResponseRedirect(reverse('Transfer'))


        data = {"cashback":cashback}
        context = {"data":data}
        return render(request, 'transfer.html', context)

    else:
        return render(request, 'transfer.html')


def Balance(request):
    user = UserRegister.objects.filter(id = request.user.id).first()
    useraccount = UserAccount.objects.filter(user_id=user.id).first()
    balance = useraccount.balance

    data = {"balance":balance}
    context = {"data":data}



    return render(request, 'balance.html', context)


def Reward(request):
    user = UserRegister.objects.filter(id = request.user.id).first()
    useraccount = UserAccount.objects.filter(user_id=user.id).first()
    reward = useraccount.cashback

    data2 = {"reward":reward}
    context2 = {"data2":data2}




    return render(request, 'reward.html', context2)

def Stored(request):
    if request.method == 'POST':
        result = []
        try:
            print("$$$$$$$$$$")
            ps_connection = psycopg2.connect(user = "postgres", password = "pass6671", host = "127.0.0.1", port = "5432", database = "bankmini" )
            user_id = 1
            cursor = ps_connection.cursor()
            cursor.callproc('public.getuser', [1])
            result = cursor.fetchall()
            print(result)

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting", error)

        finally:
            if(ps_connection):
                cursor.close()
                ps_connection.close()


        data5 = {"result":result}
        context5 = {"data5":data5}



        return render(request, 'transfer.html', context5)
