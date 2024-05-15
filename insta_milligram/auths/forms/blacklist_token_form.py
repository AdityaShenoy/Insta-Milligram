import django.forms as df


class BlacklistTokenForm(df.Form):
    token = df.CharField()
