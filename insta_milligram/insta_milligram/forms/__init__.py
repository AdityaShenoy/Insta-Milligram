import django.forms as df


def get_data(form: df.Form):
    form.is_valid()
    return form.cleaned_data
