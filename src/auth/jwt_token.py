import jwt

from datetime import datetime, timedelta

from src import exceptions
from src.settings import settings


class JWTSecurity:

    def __init__(
            self,
            secret_key: str = settings.jwt.secret_key,
            algorithm: str = settings.jwt.algorithm,
            access_lifetime: int = settings.jwt.access_token_lifetime
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_lifetime = access_lifetime

    async def create_token(self, user_id: int):
        data = {'sub': str(user_id)}
        return self._generate_jwt(data, self.secret_key, self.access_lifetime, algorithm=self.algorithm)

    async def read_token(self, token):
        try:
            data = jwt.decode(token, self.secret_key, algorithms=self.algorithm)
            user_id = data.get('sub')

            if user_id is None:
                raise exceptions.InvalidExistingToken

        except exceptions.PyJWTError:
            raise

        return user_id

    @staticmethod
    def _generate_jwt(data, secret, lifetime, algorithm):
        payload = data.copy()

        if lifetime:
            expire = datetime.utcnow() + timedelta(minutes=lifetime)
            payload['exp'] = expire
        return jwt.encode(payload, secret, algorithm=algorithm)
