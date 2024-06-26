import django.core.validators as dcv
import django.forms as df


class UserForm(df.Form):
    username = df.CharField(
        max_length=50,
        validators=[dcv.RegexValidator(r"[\w.]+")],
    )
    password = df.CharField(min_length=8, max_length=50)
    email = df.EmailField(max_length=50)
    first_name = df.CharField(max_length=50)
    last_name = df.CharField(max_length=50)
