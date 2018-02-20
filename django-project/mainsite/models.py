from django.db import models

class twitterer(models.Model):
    request_only_token = models.CharField(max_length=200, default='')
    oauth_token = models.CharField(max_length=200, default='')
    oauth_token_secret = models.CharField(max_length=200, default='')
    twitter_id = models.CharField(max_length=200, default='')
    logged = models.BooleanField(default=False)
