from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=96)
    timestamp = models.DateField(default=timezone.now, editable=False)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.id}: {self.email}, {self.username}"

class Bet(models.Model):

    HRYVNA = 'UAH'
    DOLLAR = 'USD'
    EURO = 'EURO'
    ZLOTY = 'PLN'
    POUND_STERLING = 'GBP'

    CURRENCIES = [
        (HRYVNA, 'Гривень'), 
        (DOLLAR, 'Доларів'), 
        (EURO, 'Євро'), 
        (ZLOTY, 'Злотих'), 
        (POUND_STERLING,'Фунтів стерлінгів')
    ]

    id = models.AutoField(primary_key=True)
    timestamp = models.DateField(default=timezone.now, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bets")
    bet = models.FloatField(default=0.0)
    currency = models.CharField(max_length=64, choices=CURRENCIES)

    class Meta:
        verbose_name = _("Bet")
        verbose_name_plural = _("Bets")

    def __str__(self):
        return f"{self.id}: {self.bet}, {self.username}"

class Auction(models.Model):

    __empty__ = 'NO'
    FASHION = 'FA'
    GAMES = 'GA'
    ELECTRONICS = 'EL'
    HOUSE = 'HO'
    RELAX = 'RE'

    PRODUCT_CATEGORY = [
        (__empty__, 'Без категорії'), 
        (FASHION, 'Мода'), 
        (GAMES, 'Іграшки'), 
        (ELECTRONICS, 'Електроніка'), 
        (HOUSE, 'Дім'), 
        (RELAX,'Відпочинок')
    ]

    id = models.AutoField(primary_key=True)
    timestamp = models.DateField(default=timezone.now, editable=False)
    status = models.BooleanField(default=True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=4096)
    image_url = models.URLField(max_length=128)
    category = models.CharField(max_length=64, choices=PRODUCT_CATEGORY)
    bet = models.ManyToManyField(Bet, blank=True, related_name="auctions")
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")

    class Meta:
        verbose_name = _("Auction")
        verbose_name_plural = _("Auctions")

    def __str__(self):
        return f"{self.id}: {self.title} ({self.category}) {self.status}"

class Wishes(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateField(default=timezone.now, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishes")
    auction = models.ManyToManyField(Auction, blank=True, related_name="wishes")

    class Meta:
        verbose_name = _("Wishes")
        verbose_name_plural = _("Wishlist")

    def __str__(self):
        return f"{self.id}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateField(default=timezone.now, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=4096)
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"{self.id}: {self.comment}, {self.username}"