from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from staking.crypto import get_crypto_prices
from .models import UserDatabase, Withdraw, Stake
from django.contrib.auth.decorators import login_required, user_passes_test
from  .yagmail import send_welcome_email
from .yagmail import withdrawal_message_crypto,  withdrawal_confirmation_crypto
from .yagmail import funding_confirmation_crypto, staking_message_crypto, staking_confirmation_crypto
from decimal import Decimal
from staking.payment import payment, confirm_payment
from staking.crypto import get_crypto_prices


def home(request):
    return render(request, 'index.html')

def error(request):
    return render(request, '404.html')

def signup(request):
    user = request.user
    if request.method == "POST":
        username = request.POST.get('name-3')
        email = request.POST.get('email-3')
        password = request.POST.get('password-3')

        if User.objects.filter(username=email):
            messages.error(request, 'Username already exist')
            return redirect('/signup/')
        
        if User.objects.filter(email=email):
            messages.error(request, 'Email already exist')
            return redirect('/signup/') 

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exist')
            return redirect('/signup/')   

        myuser = User.objects.create_user(username,email, password)
        email = email
        username = username
        send_welcome_email(email, username)
        myuser.save()
        return redirect('/signin/')
    return render(request, 'sign-up.html')


def signin(request):
    if request.method == "POST" :
        username = request.POST.get('email-3')
        password = request.POST.get('password-3')
        
        user = authenticate(username=username ,password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('dashboard'))

        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'sign-in.html')


def connect(request):
    return render(request, 'connect-wallet.html')

@login_required
def dashboard(request):
    username = request.user.username
    user = request.user

    user_database = UserDatabase.objects.filter(user=user).first()
    if user_database:
        if user_database.balance:
            balance = user_database.balance
        else:
            balance = 0
            
    else:
        balance = 0

    if user_database:
        if user_database.stake_amount:
            stake = user_database.stake_amount
        else:
            stake = 0
            
    else:
        stake = 0


    username = request.user.username
    user_database = UserDatabase.objects.get(user=user)
    balance = user_database.balance
    

    btc_price, eth_price, ltc_price, bch_price, ada_price, xlm_price  = get_crypto_prices()
   
    context = {
        'btc': (btc_price),
        'eth': (eth_price),
        'xlm': (xlm_price),
        'ltc': (ltc_price),
        'bch': (bch_price),
        'ada': (ada_price),
        'username': username,
        'balance': balance,
        'stake': stake,
    }
    if balance <= 0:
        pass

    else:

        if request.method == 'POST':
            return process_stake(request)
        
        stakes = Stake.objects.filter(user=user)
        for stake in stakes:
            if stake.crypto_asset == 'btc' and stake.btc:
                context['stake_btc'] = stake.amount
            elif stake.crypto_asset == 'eth' and stake.eth:
                context['stake_eth'] = stake.amount
            elif stake.crypto_asset == 'ltc' and stake.ltc:
                context['stake_ltc'] = stake.amount
            elif stake.crypto_asset == 'bch' and stake.bch:
                context['stake_bch'] = stake.amount
            elif stake.crypto_asset == 'xlm' and stake.xlm:
                context['stake_xlm'] = stake.amount
            elif stake.crypto_asset == 'ada' and stake.ada:
                context['stake_ada'] = stake.amount
        
        
        if 'check' in request.GET:
            check = request.GET['check']
            context['check'] = check

    return render(request, 'dashboard.html', context)

@login_required
def process_stake(request):
    check = ''
    if request.method == 'POST':
        amount = Decimal(request.POST['email'])
        duration = request.POST['field']
        crypto = request.POST['stake_type']
        user = request.user
        user_database = UserDatabase.objects.get(user=user)
        
        staking = Stake.objects.filter(user=user, crypto_asset=crypto, status = 'approved').first()
        if staking:
            
            check = 'staking has not been completed'
            return redirect('dashboard', check=check)
        else:
            if crypto == 'btc':
                stake = Stake(
                    user=user,
                    amount=amount,
                    crypto_asset=crypto.lower(),
                    duration=duration,
                    # Convert to lowercase to match your model's default value
                )
                user_database.balance = user_database.balance - (amount)
                user_database.stake_amount = user_database.stake_amount + amount
                user_database.save()
                stake.btc = True
                stake.save()
            elif crypto == 'eth':
                stake = Stake(
                    user=user,
                    amount=amount,
                    crypto_asset=crypto.lower(),
                    duration=duration,
                    # Convert to lowercase to match your model's default value
                )
                user_database.balance = user_database.balance - (amount)
                user_database.stake_amount = user_database.stake_amount + amount
                user_database.save()
                stake.eth = True
                stake.save()
            elif crypto == 'ltc':
                stake = Stake(
                    user=user,
                    amount=amount,
                    crypto_asset=crypto.lower(),
                    duration=duration
                    # Convert to lowercase to match your model's default value
                )
                user_database.balance = user_database.balance - (amount)
                user_database.stake_amount = user_database.stake_amount + amount
                user_database.save()
                stake.ltc = True
                stake.save()
            elif crypto == 'bch':
                stake = Stake(
                    user=user,
                    amount=amount,
                    crypto_asset=crypto.lower(),
                    duration=duration,
                    # Convert to lowercase to match your model's default value
                )
                user_database.balance = user_database.balance - (amount)
                user_database.stake_amount = user_database.stake_amount + amount
                user_database.save()
                stake.bch = True
                stake.save()
            elif crypto == 'ada':
                stake = Stake(
                    user=user,
                    amount=amount,
                    crypto_asset=crypto.lower(),
                    duration=duration,
                    # Convert to lowercase to match your model's default value
                )
                user_database.balance = user_database.balance - (amount)
                user_database.stake_amount = user_database.stake_amount + amount
                user_database.save()
                stake.ada = True
                stake.save()
            elif crypto == 'xlm':
                stake = Stake(
                    user=user,
                    amount=amount,
                    crypto_asset=crypto.lower(),
                    duration=duration,
                    # Convert to lowercase to match your model's default value
                )
                user_database.balance = user_database.balance - (amount)
                user_database.stake_amount = user_database.stake_amount + amount
                user_database.save()
                stake.xlm = True
                stake.save()
                # Run task asynchronously
                messages.success(request, "Stake request submitted successfully")
            user = request.user.username
            email = request.user.email
            staking_message_crypto(email, user, amount, crypto)
            return redirect('dashboard')
       
            

@login_required
def fund(request):
    if request.method == 'POST':
        amount = request.POST['Tronscan-2']
        crypto = request.POST['crypto']
        request.session['crypto'] = crypto
        request.session['amount'] = amount
        return redirect('/pay')
    return render(request, 'fund.html')

@login_required
def pay(request):
    amount = float(request.session['amount'])
    crypto = request.session['crypto']
    crypto = crypto.lower()

    # Check if payment ID is already in session
    if 'payment_id' in request.session:
        payment_id = request.session['payment_id']
        payment_status = request.session.get('payment_status', '')
        pay_address = request.session.get('pay_address', '')
    else:
        payment_id, payment_status, pay_address = payment(amount, crypto)
        
        request.session['payment_id'] = payment_id
        request.session['payment_status'] = payment_status
        request.session['pay_address'] = pay_address

    
    btc_price, eth_price, ltc_price, bch_price, ada_price, xlm_price = get_crypto_prices()
    prices = {
        "btc": btc_price,
        "eth": eth_price,
        "ltc": ltc_price,
        "bch": bch_price,
        "ada": ada_price,
        "xlm": xlm_price
    }
    if crypto in prices:
        crypto_price = prices[crypto]  # Get the price corresponding to the crypto variable
        p_crypto = amount / crypto_price  # Calculate the amount in crypto units
        crypto = crypto.upper()
        
        context = {
            'payment_id': payment_id,
            'payment_status': payment_status,
            'pay_address': pay_address,
            'price_crypto': round(p_crypto, 5),  # Round to 5 decimal places
            'crypto': crypto,
        }
        
        if request.method == 'POST':
            asset = request.POST['asset']
            if asset == payment_id:
                payment_status = confirm_payment(payment_id)
                
                if payment_status == 'waiting' or payment_status == 'confirming':
                    pass
                    
                elif payment_status == 'confirmed' or payment_status == 'finished':
                    process = "Payment is processed"
                    context['process'] = process
                    user = request.user
                    user_database = UserDatabase.objects.get(user=user)
                    user_database.balance += amount
                    user_database.save()
                    user = request.user.username
                    email = request.user.email
                    amount_in_crypto = round(p_crypto, 5)
                    funding_confirmation_crypto(email, user, amount_in_crypto, crypto )
                    del request.session['payment_id']
                    del request.session['payment_status']
                    del request.session['pay_address']
                    return redirect('/dashboard/')
                else:
                    expired = "Payment is expired"
                    context['process'] = expired
                    context['payment_status'] = payment_status
        return render(request, 'paymentt-verify.html', context)
    else:
        # Handle invalid cryptocurrency
        return HttpResponse("Error: Invalid cryptocurrency")

@login_required
def market(request):
    user = request.user.username
    context = {
        'user': user
    }
    return render(request, 'market.html', context)

def signout(request):
    logout(request)
    return redirect('/')

@login_required
def withdraw(request):
    user = request.user
    email = request.user.email
    username = request.user.username
    user_database = UserDatabase.objects.get(user=user)
    balance = user_database.balance
    if balance <= 0:
        pass
    else:
        if request.method == 'POST':
                # Process the form data here
                tronscan = request.POST['Tronscan']
                crypto = request.POST['Crypto']
                link = request.POST['link']

                # Save the data to the Withdraw model
                withdraw = Withdraw(
                    user=user,
                    amount=tronscan,
                    crypto_asset=crypto.lower(),  # Convert to lowercase to match your model's default value
                    address=link
                )
                withdraw.save()
                withdrawal_message_crypto(email, username, tronscan, crypto)
                return redirect('/dashboard/')

    return render(request, 'withdrawal.html')

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_signin(request):

    if request.method == "POST":
        username = request.POST.get('email-3')
        password = request.POST.get('password-3')
        
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('/admin-withdraw/')
        else:
            messages.error(request, "Invalid Credentials or Access Denied. Only admin users can access this page.")
    return render(request, 'admin/signadmin.html')

@login_required
@user_passes_test(is_admin)
def admin_withdraw(request):
    email = request.user.email
    username = request.user.username
    withdraws = Withdraw.objects.filter(status='pending')

    if request.method == 'POST':
        withdraw_id = request.POST.get('withdraw_id')
        action = request.POST.get('action')
        if action == 'Confirm':
            withdraw = Withdraw.objects.get(id=withdraw_id)
            withdraw.status = 'approved'
            withdraw.save()
            user_database = UserDatabase.objects.get(user=withdraw.user)
            user_database.balance = (user_database.balance) - (withdraw.amount)
            if user_database.balance <= 0:
                pass
            else:
                user_database.save()
                withdrawal_confirmation_crypto(email,username,withdraw.amount,withdraw.crypto_asset)
        elif action == 'Reject':
            withdraw = Withdraw.objects.get(id=withdraw_id)
            withdraw.status = 'rejected'
            withdraw.save()
            
   
    context = {
            'withdraws':withdraws,
        }
    return render(request, 'admin/withdraw.html', context)

@login_required
@user_passes_test(is_admin)
def stake(request):
    email = request.user.email
    username = request.user.username
    stakes = Stake.objects.filter(status='approved') 
    if request.method == 'POST':
        stake_id = request.POST.get('stake_id')
        try:
            stake = Stake.objects.get(id=stake_id)
        except ValueError:
            messages.error(request, "Invalid stake ID")
            return redirect('/stake/')
        except Stake.DoesNotExist:
            messages.error(request, "Stake not found")
            return redirect('/stake/')
        action = request.POST.get('action')
        asset = request.POST.get('asset')
        duration = request.POST.get('duration')
        if action == 'completed':
            stake = Stake.objects.get(id=stake_id)
            stake.status = 'completed'
            
            
            if asset == 'btc':
                if duration == '15 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(1.50)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.btc = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                    
                elif  duration == '30 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(4.00)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.btc = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                    
                elif  duration == '60 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(9.00)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.btc = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                    

            elif asset == 'eth':
                if duration == '15 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(0.70)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.eth = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                    
                elif duration == '30 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(2.50)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.eth = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                    
                elif duration == '60 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(5.00)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.eth = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
            elif asset == 'ltc':
                if duration == '15 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(0.50)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.ltc = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                elif duration == '30 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(1.50)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.ltc = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                elif duration == '60 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(3.50)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.ltc = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                    
            elif asset == 'bch':
                if duration == '15 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(0.25)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.bch = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                    
                elif duration == '30 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(0.55)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.bch = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                elif duration == '60 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(1.25)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.bch = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
            elif asset == 'ada':
                if duration == '15 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(0.25)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.ada = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                elif duration == '30 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(0.55)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.ada = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                         
                elif duration == '60 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(1.25)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.ada = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
            elif asset == 'xlm':
                if duration == '15 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(0.25)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.xlm = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                elif duration == '30 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(0.55)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.xlm = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    
                elif duration == '60 Days':
                    user_database = UserDatabase.objects.get(user=stake.user)
                    interest = stake.amount  * Decimal(1.25)
                    balanced = stake.amount  + interest
                    user_database.balance = user_database.balance + balanced
                    if user_database.stake_amount >= 0:
                        user_database.stake_amount = user_database.stake_amount - stake.amount
                        user_database.save()
                        stake.xlm = False
                        stake.save()
                        staking_confirmation_crypto(email, username, interest, asset, duration)
                        
                    else:
                        pass
                    


    context = {
        'stakes': stakes,

    }
    return render (request, 'admin/stake.html', context)


def stake_view(request):
    username = request.user.username
    context = {
        'username': username,
    }
    return render(request, 'before-you-stake.html', context)
