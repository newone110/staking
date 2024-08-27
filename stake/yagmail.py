import yagmail
from .models import UserDatabase
from django.contrib.auth.models import User

def send_welcome_email(to_email, username):
    yag = yagmail.SMTP('wpetss01@gmail.com', 'ahadmfycskhubweu', host='smtp.gmail.com', port=465)
    yag.default_sender = 'BEC Staking <wpetss01@gmail.com>'
    subject = 'Welcome to BEC staking!'
    body = f'Thanks for signing up, {username}!'
    yag.send(to_email, subject, body)

def withdrawal_message_crypto(to_email, username, deposit_amount, deposit_asset):
    yag = yagmail.SMTP('wpetss01@gmail.com', 'ahadmfycskhubweu', host='smtp.gmail.com', port=465)
    yag.default_sender = 'BEC Staking <wpetss01@gmail.com>'
    subject = 'Withdrawal Request Received'
    body = f"Your withdrawal of ${deposit_amount} worth of {deposit_asset} will be confirmed and approved soon. Take some money out and live a little {username}"
    yag.send(to_email, subject, body)

def withdrawal_confirmation_crypto(to_email, username, deposit_amount, deposit_asset):
    yag = yagmail.SMTP('wpetss01@gmail.com', 'ahadmfycskhubweu', host='smtp.gmail.com', port=465)
    yag.default_sender = 'BEC Staking <wpetss01@gmail.com>'
    subject = f'Withdrawal has been confirmed: {username}'
    body = f"Your funds of #{deposit_amount} worth of {deposit_asset} have been confirmed and withdrawn from your BEC staking account."
    yag.send(to_email, subject, body)

def funding_confirmation_crypto(to_email, username, deposit_amount, asset):
    yag = yagmail.SMTP('wpetss01@gmail.com', 'ahadmfycskhubweu', host='smtp.gmail.com', port=465)
    yag.default_sender = 'BEC Staking <wpetss01@gmail.com>'
    subject = f'Funding has been confirmed:  {username}'
    body = f"Your funds of {deposit_amount}{asset} have been confirmed and deposited into your BEC staking."
    yag.send(to_email, subject, body)

def staking_message_crypto(to_email, username, deposit_amount, asset):
    yag = yagmail.SMTP('wpetss01@gmail.com', 'ahadmfycskhubweu', host='smtp.gmail.com', port=465)
    yag.default_sender = 'BEC Staking <wpetss01@gmail.com>'
    subject = f'Staking has been confirmed:  {username}'
    body = f"Your stake of {deposit_amount} worth of {asset} have been confirmed and staked into {asset}."
    yag.send(to_email, subject, body)

def staking_confirmation_crypto(to_email, username, deposit_amount, asset, duration):
    yag = yagmail.SMTP('wpetss01@gmail.com', 'ahadmfycskhubweu', host='smtp.gmail.com', port=465)
    yag.default_sender = 'BEC Staking <wpetss01@gmail.com>'
    subject = f'Staking has been paid out:  {username}'
    body = f"Your stake of {deposit_amount} worth of {asset} for {duration} has paid out and have been credited to your balance."
    yag.send(to_email, subject, body)






