from package.models.user_model import User


def get_all_users(session):
    return session.query(User).all()


def get_user(session, user_id):
    return session.get(User, user_id)


def create_user(session, user_data):
    user = User(**user_data)
    session.add(user)
    session.flush()
    return user


def update_user(session, user_id, user_data):
    user = session.query(User).get(user_id)
    if not user:
        return None
    for key, value in user_data.items():
        setattr(user, key, value)
    session.flush()
    return user


def delete_user(session, user_id):
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    return True
