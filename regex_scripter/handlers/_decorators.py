from database.db import session, User
from logger import logger


def get_user(get_chat=False):
    def decorator(func):
        def wrapper(update, context):
            logger.info('---------')
            logger.info(f'FUNC {func.__name__}')
            l = 'Getting user'
            if get_chat:
                l += ' and chat'
            logger.info(l)

            user = session.query(User).filter_by(user_id=update.message.from_user.id).first()
            is_changed = False
            if not user:
                user = User(user_id=update.message.from_user.id,
                            first_name=update.message.from_user.first_name,
                            last_name=update.message.from_user.last_name,
                            username=update.message.from_user.username)
                session.add(user)
                logger.info(f'New user {user}')
                is_changed = True
            else:
                logger.info(f'Existing user {user}')
                if user.first_name != update.message.from_user.first_name:
                    user.first_name = update.message.from_user.first_name
                    is_changed = True
                if user.last_name != update.message.from_user.last_name:
                    user.last_name = update.message.from_user.last_name
                    is_changed = True
                if user.last_name != update.message.from_user.last_name:
                    user.username = update.message.from_user.username
                    is_changed = True
            if not get_chat:
                if is_changed:
                    session.commit()
                return func(update, context, user)


            if is_changed:
                session.commit()
            return func(update, context, user)

        return wrapper

    return decorator

