from passlib.context import CryptContext


class PasswordHelper:

    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str):
        return self.context.hash(password)

    def verify_password(self, password: str, hashed_password: str):
        return self.context.verify(password, hashed_password)

    def verify_and_update(self, password: str, hashed_password: str):
        return self.context.verify_and_update(password, hashed_password)