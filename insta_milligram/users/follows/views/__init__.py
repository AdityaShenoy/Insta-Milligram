import rest_framework.views as rv  # type: ignore

from .post_view import post
from .get_followings_view import get
from .get_followers_view import get_followers

# from .delete_view import delete


class UserFollowView(rv.APIView):
    def __init__(self):
        super().__init__()
        self.post = post
        self.get = get
        # self.delete = delete


class UserFollowerView(rv.APIView):
    def __init__(self):
        super().__init__()
        self.get = get_followers
