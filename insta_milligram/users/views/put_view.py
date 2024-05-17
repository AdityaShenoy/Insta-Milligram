import django.contrib.auth.models as dcam
import django.http.request as dhreq

import insta_milligram.constants as ic
import insta_milligram.forms as if_
import insta_milligram.responses.decorators as ird
import users.forms as uf


@ird.check_authenticated()
@ird.check_missing_id()
@ird.check_user_exists()
@ird.check_authorized()
@ird.check_form(uf.UserForm)
def put(request: dhreq.HttpRequest, id: int = -1):
    form_data = if_.get_data(uf.UserForm(request.data))  # type: ignore
    user = dcam.User.objects.get(pk=id)
    for field in form_data:
        user.__setattr__(field, form_data[field])
    user.set_password(form_data["password"])
    user.save()
    return ic.responses.SUCCESS
