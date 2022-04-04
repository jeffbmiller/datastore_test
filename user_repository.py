from typing import List

from user import User

class UserRepository():

    def get_by_uid(self, uid: str) -> User:
        user = User(
            uid=uid,
            email="test@test.com"
            )
        return user
