import django.forms as df


class UserFollowForm(df.Form):
    user = df.IntegerField()
