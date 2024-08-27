from django.contrib import admin
from .models import UserDatabase, Withdraw, Stake

# Register your models here.
admin.site.register(UserDatabase)

admin.site.register(Withdraw)

admin.site.register(Stake)