import aioredis
from src.config import Config


TOKEN_EXPIRY = 3600  # 1 hour in seconds


token_blocklist = aioredis.StrictRedis(
    host = Config.REDIS_HOST,
    port = Config.REDIS_PORT,
    db = 0
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex = TOKEN_EXPIRY
    )

async def token_in_blocklist(jti:str) -> bool:
    await token_blocklist.get(jti)

    return jti is not None

