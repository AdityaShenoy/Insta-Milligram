import rest_framework.status as rs  # type: ignore

from ... import helpers as h
from .. import messages as m

SUCCESS = h.create_response(m.SUCCESS, rs.HTTP_200_OK)
USER_NOT_FOUND = h.create_response(
    m.USER_NOT_FOUND,
    rs.HTTP_401_UNAUTHORIZED,
)
INCORRECT_PASSWORD = h.create_response(
    m.INCORRECT_PASSWORD,
    rs.HTTP_401_UNAUTHORIZED,
)
USER_ALREADY_EXISTS = h.create_response(
    m.USER_ALREADY_EXISTS,
    rs.HTTP_400_BAD_REQUEST,
)
INCORRECT_USER = h.create_response(
    m.INCORRECT_USER,
    rs.HTTP_401_UNAUTHORIZED,
)

# INCORRECT_TOKEN_PARAMETER = h.create_response(
#     m.INCORRECT_TOKEN_PARAMETER, rs.HTTP_400_BAD_REQUEST
# )
