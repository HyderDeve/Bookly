from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, responses
from fastapi.responses import JSONResponse

from .structs import UserCreateModel, UserResponse, UserLoginModel, UserBooks, EmailRequest, PasswordResetRequest, PasswordConfirmRequest
from .services import UserService
from .utils import create_access_token, decode_token,verify_password, create_url_safe_token, decode_url_safe_token, generate_hash_password
from .dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker, get_current_user

from datetime import timedelta, datetime
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.errors import (UserAlreadyExists, UserNotFound, InvalidCredentials, InvalidToken)
from src.mail import create_message, mail
from src.config import Config
from typing import Any

auth_router = APIRouter()
user_service = UserService()  # Create an instance of UserService for handling user operations
role_checker = RoleChecker(['admin','user'])

REFRESH_TOKEN_EXPIRY = 2



@auth_router.post('/send-mail')
async def send_mail(emails : EmailRequest, background_tasks : BackgroundTasks):
    
    emails = emails.addresses

    html = '<h1>Welcome To The App</h1>'

    message = create_message(
        receipients = emails,
        subject = 'Account Created Successfully',
        body = html
    )

    background_tasks.add_task(mail.send_message, message)

    return JSONResponse(
        content = {'message' : 'Email Sent Successfully'},
        status_code = status.HTTP_201_CREATED
    )
    
@auth_router.post("/signup", status_code=status.HTTP_201_CREATED, responses = {
    201 : {"description": "Created",
        "content": {
            "application/json": {
                "example": {
                     'message' : 'Account Created Successfully! Check your email to verify your account',
                      "user": {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "email": "user@example.com",
                            "username": "johndoe",
                            "first_name": "John",
                            "last_name": "Doe",
                            "role": "user",
                            "is_verified": False,
                            "created_at": "2025-08-08T12:00:00",
                            "updated_at": "2025-08-08T12:00:00"
                        }
                }
            }
        }},
    500 : {"description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Customized Message"
                }
            }
        }},
    403 : {
        "description": "Not authorized",
        "content": {
            "application/json": {
                "example": {
                    "message": "Not Authorized"
                }
            }
        }}
})
async def create_user(user_data: UserCreateModel, background_tasks : BackgroundTasks,session: AsyncSession = Depends(get_session)):
    
    email = user_data.email 

    user_exists = await user_service.user_exists(email, session)  # Check if the user already exists in the database

    if user_exists:
        raise UserAlreadyExists()
    
    new_user = await user_service.create_user(user_data,session)

    token = create_url_safe_token({"email" : email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f6f9fc; padding: 40px 0;">
      <tr>
        <td align="center">
          <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; padding: 40px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <tr>
              <td align="center" style="padding-bottom: 20px;">
                <img src="https://static.vecteezy.com/system/resources/previews/020/336/484/non_2x/tesla-logo-tesla-icon-transparent-png-free-vector.jpg" alt="Train Grains Logo" width="150" style="display: block;" />
              </td>
            </tr>
            <tr>
              <td style="font-size: 20px; color: #333333; font-weight: bold; text-align: center;">
                Verify Your Email
              </td>
            </tr>
            <tr>
              <td style="font-size: 16px; color: #555555; line-height: 1.6; padding: 20px 0; text-align: center;">
                Hi there,<br />
                Thank you for signing up. Please confirm your email address to activate your account.
              </td>
            </tr>
            <tr>
              <td align="center" style="padding: 20px;">
                <a href="{link}" style="background-color: #007BFF; color: #ffffff; padding: 14px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                  Confirm Email
                </a>
              </td>
            </tr>
            <tr>
              <td style="font-size: 14px; color: #999999; text-align: center; padding-top: 30px;">
                If you did not sign up for this account, you can safely ignore this email.
              </td>
            </tr>
            <tr>
              <td style="font-size: 12px; color: #cccccc; text-align: center; padding-top: 20px;">
                © {datetime.now().year} Train Grains, All rights reserved.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
    """
    message = create_message(
        receipients = [email],
        subject = 'Verify Your Account',
        body = html_message
    )

    background_tasks.add_task(mail.send_message, message)

    return {
            'message' : 'Account Created Successfully! Check your email to verify your account',
            'user' : new_user
        }


@auth_router.get('/verify/{token}',responses={
        200: {
            "description": "Account verified successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Account verified successfully"
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "invalid_token": {
                            "summary": "Invalid Token Error",
                            "value": {
                                "message": "Invalid token format",
                                "error_code": "INVALID_TOKEN",
                                "timestamp": "2025-08-07T12:00:00"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def verify_account(token: str, session: AsyncSession = Depends(get_session)):
    try:
        token_data = decode_url_safe_token(token)

        user_email = token_data.get('email')

        if user_email is None:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": "Invalid token format",
                    "error_code": "Invalid Token",
                    "timestamp": datetime.now().isoformat()
                }
            )

        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()
        
        await user_service.update_user(user, {'is_verified': True}, session)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": str(e),
                "error_code": "Verification Error",
                "timestamp": datetime.now().isoformat()
            }
        )

@auth_router.post("/login", status_code = status.HTTP_201_CREATED, responses = {
    201: {'description' : 'Created', 'content':{'application/json' : {'example' : 
      {
        'message' : 'Login Successful',
                    "access_token": 'access_token',
                    "refresh_token": 'refresh_token',
                    "user" : {
                        "email": 'user.email',
                        "user_id": 'str(user.id)'
                    }
      }}}},
      500:{'description' : 'Internal Server Error', 'content':{'application/json' : {'example' : 
      {
        'message' : "Email Doesn't Exists"}}}},
      403:{'description' : 'Forbidden Access', 'content':{'application/json' : {'example' : 
      {
        'message' : "Login Failed, Forbidden Access"}}}}
    }
  )
async def login_user(login_data:UserLoginModel, session: AsyncSession = Depends(get_session)):
    
    email = login_data.email
    password = login_data.password

    try:
    
      user = await user_service.get_user_by_email(email,session)
    
    except Exception as e:
        JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {'message' : str(e)}
        )

    if user is not None:
        password_valid = verify_password(password, user.password)

        if password_valid:
            access_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_id': str(user.id),
                    'role': user.role
                }
            )

            refresh_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_id': str(user.id)
                },
                refresh = True,
                expiry = timedelta(days = REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user" : {
                        "email": user.email,
                        "user_id": str(user.id)
                    }
                }
            )
    
    raise InvalidCredentials()


@auth_router.get("/refresh-token",responses = {200:{'description' : 'Access Token Refreshed', 'content' : {'application/json' : {'example':{"message": "Access token refreshed successfully.", "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImVtYWlsIjo..."}}}},500:{'description' : 'Internal Server Error', 'content' : {'application/json' : {'example':{"message": "Server Not Responding."}}}},403:{'description' : 'Forbidden Access', 'content' : {'application/json' : {'example':{"message": "Token is expired or invalid."}}}}})
async def access_token(token_details:dict = Depends(RefreshTokenBearer())):

    """
    Endpoint to refresh the access token using a valid refresh token.
    
    """

    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
        user_data = token_details['user']
        )
        return JSONResponse(content={
                "message": "Access token refreshed successfully.",
                "access_token": new_access_token
            })
    
    raise InvalidToken()



# GET /auth/me
@auth_router.get('/me',response_model=UserBooks,responses = {500:{'description' : 'Internal Server Error', 'content' : {'application/json' : {'example' : {'message' : 'Customized Error Message'}}}},403:{'description' : 'Forbidden Access', 'content' : {'application/json' : {'example' : {'message' : 'Insufficient Permissions'}}}}})
async def get_current_user(
    user = Depends(get_current_user),
    _ : bool = Depends(role_checker)):

    return user


@auth_router.post('/password-reset' , status_code = status.HTTP_201_CREATED, responses = {
    201 : {
              "description": "Password Reset Link Sent Successfully",
            "content": {
                "application/json": {
                    "example":{'message' : "Please Check Email To Reset Password"}
                  }
                }
              },
    500 : {
            "description": "Internal Server Error",
              "content": {
                "application/json": {
                    "example":{'message' : "Customized Error Message"}
                  }
                }
              }
          })
async def password_reset_request(email_data : PasswordResetRequest, background_tasks : BackgroundTasks):
    
    email = email_data.email

    try:
        
        token = create_url_safe_token({"email" : email})

    except Exception as e:
        
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {'message' : str(e)}
        )

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f6f9fc; padding: 40px 0;">
      <tr>
        <td align="center">
          <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; padding: 40px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <tr>
              <td align="center" style="padding-bottom: 20px;">
                <img src="https://static.vecteezy.com/system/resources/previews/020/336/484/non_2x/tesla-logo-tesla-icon-transparent-png-free-vector.jpg" alt="Train Grains Logo" width="150" style="display: block;" />
              </td>
            </tr>
            <tr>
              <td style="font-size: 20px; color: #333333; font-weight: bold; text-align: center;">
                Reset Your Password
              </td>
            </tr>
            <tr>
              <td style="font-size: 16px; color: #555555; line-height: 1.6; padding: 20px 0; text-align: center;">
                Hi there,<br />
                Thank you for signing up. Please confirm your email address to activate your account.
              </td>
            </tr>
            <tr>
              <td align="center" style="padding: 20px;">
                <a href="{link}" style="background-color: #007BFF; color: #ffffff; padding: 14px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                  Confirm Email
                </a>
              </td>
            </tr>
            <tr>
              <td style="font-size: 14px; color: #999999; text-align: center; padding-top: 30px;">
                If you did not sign up for this account, you can safely ignore this email.
              </td>
            </tr>
            <tr>
              <td style="font-size: 12px; color: #cccccc; text-align: center; padding-top: 20px;">
                © {datetime.now().year} Train Grains, All rights reserved.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
    """
    
    message = create_message(
        receipients = [email],
        subject = 'Reset Your Password',
        body = html_message
    )

    try:
        
        background_tasks.add_task(mail.send_message, message)

    except Exception as e:
        
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {'message' : str(e)}
        )


    return JSONResponse(
        content = {
            'message' : 'Please Check Your Email To Reset Your Password',
          },
          status_code = status.HTTP_201_CREATED
    )



@auth_router.post('/password-reset-confirm/{token}',status_code = status.HTTP_201_CREATED, responses = {201:{'description': 'Created','content':{'application/json': {'example' : {'message':'Password Reset Successfully'}}}},400:{'description': 'Bad Request','content':{'application/json': {'example' : {'message':'Passwords do not match'}}}},500:{'description': 'Internal Server Error','content':{'application/json': {'example' : {'message':'Error While Decoding Token'}}}}} )
async def reset_password(token : str, password : PasswordConfirmRequest, session : AsyncSession = Depends(get_session)):
    
    new_password  = password.new_password
    confirm_password = password.confirm_password

    if new_password != confirm_password:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                'message' : 'Passwords do not match'
            }
        )

    try:

      token_data = decode_url_safe_token(token)

      user_email = token_data.get('email')
    
    except Exception as e:
        
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {
                'message' : str(e)
            }
        )

    if user_email is not None:
        
        user = await user_service.get_user_by_email(user_email,session)

        if not user:
            raise UserNotFound()
        
        password_hash  = generate_hash_password(new_password)

        await user_service.update_user(user, {'password' : password_hash}, session)

        return JSONResponse(
            content = {
                'message' : 'Password Reset successfully'
            },
            status_code = status.HTTP_201_CREATED 
        )
    
    return JSONResponse(
        content = {'message' : 'Error Resetting Password'},
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    )