import rest_framework.response as rr  # type: ignore
import rest_framework.status as rs  # type: ignore

import insta_milligram.constants.messages as icm


def create_response(message: str, status_code: int):
    return rr.Response({"message": message}, status_code)


SUCCESS = create_response(
    icm.SUCCESS,
    rs.HTTP_200_OK,
)
USER_NOT_FOUND = create_response(
    icm.USER_NOT_FOUND,
    rs.HTTP_404_NOT_FOUND,
)
INCORRECT_PASSWORD = create_response(
    icm.INCORRECT_PASSWORD,
    rs.HTTP_401_UNAUTHORIZED,
)
USER_ALREADY_EXISTS = create_response(
    icm.USER_ALREADY_EXISTS,
    rs.HTTP_400_BAD_REQUEST,
)
USER_ID_MISSING = create_response(
    icm.USER_ID_MISSING,
    rs.HTTP_400_BAD_REQUEST,
)
INCORRECT_USER = create_response(
    icm.INCORRECT_USER,
    rs.HTTP_401_UNAUTHORIZED,
)
OPERATION_NOT_ALLOWED = create_response(
    icm.OPERATION_NOT_ALLOWED,
    rs.HTTP_403_FORBIDDEN,
)
TOKEN_MISSING = create_response(
    icm.TOKEN_MISSING,
    rs.HTTP_401_UNAUTHORIZED,
)
INVALID_TOKEN = create_response(
    icm.INVALID_TOKEN,
    rs.HTTP_401_UNAUTHORIZED,
)
INCORRECT_TOKEN_PARAMETER = create_response(
    icm.INCORRECT_TOKEN_PARAMETER, rs.HTTP_400_BAD_REQUEST
)
INVALID_DATA = create_response(
    icm.INVALID_DATA,
    rs.HTTP_400_BAD_REQUEST,
)
LOGIN_BLACKLISTED = create_response(
    icm.LOGIN_BLACKLISTED,
    rs.HTTP_401_UNAUTHORIZED,
)

INVALID_USER_PATCH_DATA = create_response(
    icm.INVALID_USER_PATCH_DATA,
    rs.HTTP_400_BAD_REQUEST,
)
