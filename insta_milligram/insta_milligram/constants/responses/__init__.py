import rest_framework.status as rs  # type: ignore

from ... import helpers as h
from .. import messages as m

SUCCESS = h.create_response(m.SUCCESS, rs.HTTP_200_OK)
USER_NOT_FOUND = h.create_response(
    m.USER_NOT_FOUND,
    rs.HTTP_404_NOT_FOUND,
)
INCORRECT_PASSWORD = h.create_response(
    m.INCORRECT_PASSWORD,
    rs.HTTP_401_UNAUTHORIZED,
)
USER_ALREADY_EXISTS = h.create_response(
    m.USER_ALREADY_EXISTS,
    rs.HTTP_400_BAD_REQUEST,
)
USER_ID_MISSING = h.create_response(
    m.USER_ID_MISSING,
    rs.HTTP_400_BAD_REQUEST,
)
INCORRECT_USER = h.create_response(
    m.INCORRECT_USER,
    rs.HTTP_401_UNAUTHORIZED,
)
OPERATION_NOT_ALLOWED = h.create_response(
    m.OPERATION_NOT_ALLOWED,
    rs.HTTP_403_FORBIDDEN,
)
TOKEN_MISSING = h.create_response(
    m.TOKEN_MISSING,
    rs.HTTP_401_UNAUTHORIZED,
)
INVALID_TOKEN = h.create_response(
    m.INVALID_TOKEN,
    rs.HTTP_401_UNAUTHORIZED,
)


# INCORRECT_TOKEN_PARAMETER = h.create_response(
#     m.INCORRECT_TOKEN_PARAMETER, rs.HTTP_400_BAD_REQUEST
# )
