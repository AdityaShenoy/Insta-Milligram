import django.forms as df


class RefreshTokenForm(df.Form):
    refresh = df.CharField()
