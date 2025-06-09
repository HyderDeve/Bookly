from .models import User
from .structs import UserCreateModel
from .utils import generate_hash_password
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi.responses import JSONResponse


class UserService:
    async def get_user_by_email(self,email:str, session: AsyncSession) -> User:
        """Fetch a user by email from the database."""
        statement = select(User).where(User.email == email)
        
        user = await session.exec(statement)
        
        return user.first()  # Return the first user found or None if not found
    
    async def user_exists(self,email: str, session: AsyncSession):
        """Check if a user exists in the database by email."""
        

        user  = await self.get_user_by_email(email, session)

        return True if user is not None else False  # Return True if user exists, False otherwise

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession) -> User:
        """Create a new user in the database."""
        
        user_data_dict = user_data.model_dump()  # Convert Pydantic model to dictionary

        new_user = User(
            **user_data_dict  # Unpack the dictionary into the User model
        )
        new_user.password = generate_hash_password(user_data_dict['password'])  # Hash the password before saving

        session.add(new_user)  # Add the new user to the session

        await session.commit()

        return new_user


    async def get_user_by_id(self, user_id: str, session: AsyncSession):

        statement = select(User).where(User.id == user_id)

        result = await session.exec(statement)

        user = result.first()

        return user if not None else JSONResponse(
            content={
                'detail': 'User not found'
            }
        )

