from db import engine, session
from models import Base
import users


def main():
    Base.metadata.create_all(engine)

    token = users.register()
    session.commit()

    user = users.get_by_token(token)
    print(user)


if __name__ == '__main__':
    main()
