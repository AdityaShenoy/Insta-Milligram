import django.contrib.auth.models as dcam
import django.http.request as dhreq

from .. import forms as f
import insta_milligram.constants as ic
import insta_milligram.responses as ir
import insta_milligram.responses.decorators as ird


@ird.check_missing_id()
def put(request: dhreq.HttpRequest, id: int = -1):
    form = f.UserForm(request.data)  # type: ignore
    if not form.is_valid():
        return ir.create_response(
            ic.responses.INVALID_DATA,
            {"errors": form.errors},
        )
    form_data = form.cleaned_data
    try:
        user = dcam.User.objects.get(pk=id)
        for field in form_data:
            user.__setattr__(field, form_data[field])
        user.set_password(form_data["password"])
        user.save()
        return ic.responses.SUCCESS
    except dcam.User.DoesNotExist:
        return ic.responses.USER_NOT_FOUND
