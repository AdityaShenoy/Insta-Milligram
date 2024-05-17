import rest_framework.views as rv  # type: ignore

from .post_view import post
from .delete_view import delete


class AuthView(rv.APIView):
    def __init__(self):
        super().__init__()
        self.post = post
        self.delete = delete
