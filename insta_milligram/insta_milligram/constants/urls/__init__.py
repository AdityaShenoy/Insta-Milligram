USERS = "/users"
AUTHS = "/auths"


def user_id(id: int):
    return f"/users/{id}"


def user_id_followings(id: int):
    return f"/users/{id}/followings"


def user_id_followings_page(id: int, page: int):
    return f"/users/{id}/followings?page={page}"


def user_id_followers(id: int):
    return f"/users/{id}/followers"


def user_id_followers_page(id: int, page: int):
    return f"/users/{id}/followers?page={page}"


def user_id_followings_id(id1: int, id2: int):
    return f"/users/{id1}/followings/{id2}"
