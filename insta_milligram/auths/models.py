import django.db.models as ddm


class BlacklistedToken(ddm.Model):
    token = ddm.CharField(max_length=500)
