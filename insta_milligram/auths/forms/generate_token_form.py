import django.core.validators as dcv
import django.forms as df


class GenerateTokenForm(df.Form):
    username = df.CharField(
        max_length=50,
        validators=[dcv.RegexValidator(r"[\w.]+")],
    )
    password = df.CharField(min_length=8, max_length=50)
