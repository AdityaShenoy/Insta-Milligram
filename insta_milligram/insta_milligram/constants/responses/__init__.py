import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore

from .. import messages as m


def create_response(message: str, status_code: int):
    return rr.Response({"message": message}, status_code)


SUCCESS = create_response(m.SUCCESS, rs.HTTP_200_OK)
USER_NOT_FOUND = create_response(
    m.USER_NOT_FOUND,
    rs.HTTP_404_NOT_FOUND,
)
INCORRECT_PASSWORD = create_response(
    m.INCORRECT_PASSWORD,
    rs.HTTP_401_UNAUTHORIZED,
)
USER_ALREADY_EXISTS = create_response(
    m.USER_ALREADY_EXISTS,
    rs.HTTP_400_BAD_REQUEST,
)
USER_ID_MISSING = create_response(
    m.USER_ID_MISSING,
    rs.HTTP_400_BAD_REQUEST,
)
INCORRECT_USER = create_response(
    m.INCORRECT_USER,
    rs.HTTP_401_UNAUTHORIZED,
)
OPERATION_NOT_ALLOWED = create_response(
    m.OPERATION_NOT_ALLOWED,
    rs.HTTP_403_FORBIDDEN,
)
TOKEN_MISSING = create_response(
    m.TOKEN_MISSING,
    rs.HTTP_401_UNAUTHORIZED,
)
INVALID_TOKEN = create_response(
    m.INVALID_TOKEN,
    rs.HTTP_401_UNAUTHORIZED,
)
INCORRECT_TOKEN_PARAMETER = create_response(
    m.INCORRECT_TOKEN_PARAMETER, rs.HTTP_400_BAD_REQUEST
)
INVALID_DATA = create_response(
    m.INVALID_DATA,
    rs.HTTP_400_BAD_REQUEST,
)
