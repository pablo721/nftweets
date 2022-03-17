from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32)


class Tag(models.Model):
    text = models.CharField(max_length=32)


class TwitterAcc(models.Model):
    username = models.CharField(max_length=64)
    user_id = models.BigIntegerField()
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    bio = models.CharField(max_length=200, blank=True)
    followers = models.ManyToManyField('self')


class Tweet(models.Model):
    author = models.ForeignKey('mood.TwitterAcc', on_delete=models.CASCADE)
    tags = models.ManyToManyField('mood.Tag')
    text = models.CharField(max_length=500)


class CryptoAsset(models.Model):
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=16, blank=True, null=True)
    url = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    tags = models.ManyToManyField('mood.Tag')


class Cryptocurrency(CryptoAsset):
    price = models.FloatField()
    quote_curr = models.CharField(max_length=16)


class CryptoNetwork(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=64)
    native_asset = models.OneToOneField('mood.Cryptocurrency', on_delete=models.CASCADE)
    consensus_mechanism = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=512, blank=True)


class NFT(CryptoAsset):
    floor_price = models.FloatField()
    quote_curr = models.CharField(max_length=16)
    collection = models.ForeignKey('mood.NFTCollection', on_delete=models.CASCADE)


class NFTCollection(models.Model):
    name = models.CharField(max_length=128)




class Event(models.Model):
    name = models.CharField(max_length=128)
    announce_date = models.DateField()
    start_date = models.DateField()
    description = models.CharField(max_length=512)
    url = models.CharField(max_length=128)


class Alert(models.Model):
    underlying_asset = models.ForeignKey('mood.CryptoAsset', on_delete=models.CASCADE)
    message = models.CharField(max_length=256)
    signature = models.CharField(max_length=128, default='NFT Analyzer')

