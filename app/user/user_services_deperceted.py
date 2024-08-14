# from typing import Type, Optional, Callable
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy import BinaryExpression
# from fastapi import HTTPException, UploadFile, status
#
# from app.libs.images_service import create_image_service
#
# from .user_model import UserModel
# from . import user_dtos
#
# from app.libs import password_lib
# from app.utils import optional, find_errr_from_args
# from app.libs.jwt_lib import jwt_dto, jwt_service
#
#
# def get_user(db: Session, user_id: str) -> optional.Optional[UserModel, Exception]:
#     user_model = db.query(UserModel) \
#         .filter(UserModel.id == user_id) \
#         .first()
#     if not user_model:
#         return optional.build(error=HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"))
#
#     return optional.build(data=user_model)
#
#
# def get_user_by_property(
#         db: Session, filter: Callable[[Type[UserModel]], BinaryExpression[bool]]) \
#         -> optional.Optional[UserModel, HTTPException]:
#     user_model: Optional[UserModel] = db.query(UserModel).filter(filter(UserModel)).first()
#     if user_model:
#         return optional.build(data=user_model)
#     else:
#         return optional.build(error=HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="user not found"
#         ))
#
#
# def get_user_by_email(db: Session, user_email: str) -> optional.Optional[UserModel, HTTPException]:
#     def user_filter(user_model: Type[UserModel]):
#         return user_model.email.like(f"{user_email}")
#
#     user_opt = get_user_by_property(db=db, filter=user_filter)
#
#     if user_opt.data:
#         return user_opt
#
#     return optional.build(error=HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="email is not register"
#     ))
#
#
# def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[Type[UserModel]]:
#     return db.query(UserModel) \
#         .offset(skip) \
#         .limit(limit) \
#         .all()
#
#
# # user-register
# def create_user(db: Session, user: user_dtos.UserCreateDto) -> optional.Optional[UserModel, Exception]:
#     try:
#         user_model = UserModel()
#         user_model.email = user.email
#         user_model.fullname = user.fullname
#         user_model.username = user.username
#         user_model.hash_password = password_lib.get_password_hash(password=user.password)
#
#         db.add(user_model)
#         db.commit()
#         return optional.build(data=user_model)
#     except SQLAlchemyError as e:
#         print(find_errr_from_args("users", str(e)))
#         return optional.build(error=HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="{property} already use".format(
#                 property=find_errr_from_args("users", str(e))
#             )
#         ))
#
#
# # user-login
#
# # user-edit
# def user_edit(db: Session, user: user_dtos.UserEditProfileDto, user_id: str) -> optional.Optional[UserModel, Exception]:
#     try:
#         user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
#
#         if user_model:
#             # Data user sudah diisi dari request body melalui parameter 'user'
#             for field, value in user.dict().items():
#                 setattr(user_model, field, value)
#
#             db.commit()
#             db.refresh(user_model)
#
#             return optional.build(data=user_model)
#
#         else:
#             raise optional.build(error=HTTPException(status_code=404, detail="User not found"))
#
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise optional.build(error=HTTPException(status_code=409, detail="Database conflict: " + str(e)))
#
#
# # user-token
# def service_access_token(user_id: str):
#     user_ditch = dict([
#         ("id", user_id)
#     ])
#     return jwt_service.create_access_token(user_ditch)
