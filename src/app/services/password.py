from sqlalchemy import or_, func

from src.app.models import PasswordModel


class PasswordService:
    @staticmethod
    def is_password_exists(pass_id, session):
        """
        Method check is password exists in the database
        :param pass_id:
        :param session:
        :return: boolean or Exception SQLAlchemy error if dont have connect to db
        """
        password = session.query(PasswordModel).filter(PasswordModel.pass_id == pass_id).first()
        return bool(password)

    @staticmethod
    def get_password_list(current_user, session):
        passwords = session.query(PasswordModel).filter(PasswordModel.user_id == current_user.id).all()
        passwords_serialized = []
        for password in passwords:
            passwords_serialized.append(password.serialize)
        return passwords_serialized

    @staticmethod
    def get_password_by_id(current_user_id, pass_id, session):
        password = session.query(PasswordModel)\
            .filter(PasswordModel.user_id == current_user_id)\
            .filter(PasswordModel.pass_id == pass_id)\
            .first()
        return password

    @staticmethod
    def add_password(data, current_user, session):
        session.add(PasswordModel(current_user.id, data))
        session.commit()
        return data['title']

    @staticmethod
    def update_password(password, data, session):
        for key in data.keys():
            if key != 'password':
                password.__setattr__(key, data[key])
            else:
                password.crypt_password(data[key])
        session.add(password)
        session.commit()
        return password

    @staticmethod
    def delete_password(pass_id, current_user, session):
        session.query(PasswordModel) \
            .filter(PasswordModel.user_id == current_user.id) \
            .filter(PasswordModel.pass_id == pass_id) \
            .delete()
        session.commit()
        return pass_id

    @staticmethod
    def search_password_by_condition(user_id, condition, session):
        condition.lower()
        # Soft search with wildcard percent sign
        filtered_passwords = session.query(PasswordModel).filter(PasswordModel.user_id == user_id).filter(or_(
            func.lower(PasswordModel.comment).like(f'%{condition}%'),
            func.lower(PasswordModel.title).like(f'%{condition}%'),
            func.lower(PasswordModel.url).like(f'%{condition}%')
        ))
        passwords_by_condition = []
        for password in filtered_passwords:
            passwords_by_condition.append(password.serialize)
        if passwords_by_condition:
            return passwords_by_condition
        else:
            return False

    @staticmethod
    def filter_password_by_id(pass_id, session):
        password = session.query(PasswordModel).filter(PasswordModel.pass_id == pass_id).first()
        return password