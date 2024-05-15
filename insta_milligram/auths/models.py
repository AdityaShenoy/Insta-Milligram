import django.contrib.auth.models as dcam
import django.db.models as ddm


class BlacklistedToken(ddm.Model):
    user = ddm.OneToOneField(dcam.User, on_delete=ddm.CASCADE)
    iat = ddm.IntegerField()
