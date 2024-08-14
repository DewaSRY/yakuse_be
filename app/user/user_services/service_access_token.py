from app.libs.jwt_lib import jwt_dto, jwt_service


def service_access_token(user_id: str):
    user_ditch = dict([
        ("id", user_id)
    ])
    return jwt_service.create_access_token(user_ditch)
