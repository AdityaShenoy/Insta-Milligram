import rest_framework.views as rv  # type: ignore

from .post_view import post
from .get_view import get
from .put_view import put
from .delete_view import delete


class UserView(rv.APIView):
    def __init__(self):
        super().__init__()
        self.post = post
        self.get = get
        self.put = put
        self.delete = delete
