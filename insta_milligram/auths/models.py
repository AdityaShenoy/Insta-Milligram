import django.db.models as ddm


class BlacklistedTokens(ddm.Model):
    token = ddm.CharField(max_length=500)
