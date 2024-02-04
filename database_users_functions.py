from sqlalchemy.orm import Session
from sqlalchemy import select
from data_base_users import engine, User, Password, Score
from typing import Optional


session = Session(engine)


def clear_db():
    users = session.query(User).all()
    list_id = [user.id for user in users]

    for user_id in list_id:
        delete_user_by_id(user_id)


def user_exists(email: str) -> bool:
    return (get_user_by_email(email=email) != None)


def get_user_id_by_email(email: str) -> int:
    if not user_exists(email):
        return -1

    return session.scalar(select(User).where(User.email == email)).id


def get_user_by_id(_id: int) -> Optional[User]:
    return session.scalar(select(User).where(User.id == _id))


def get_user_by_email(email: str) -> Optional[User]:
    return session.scalar(select(User).where(User.email == email))


def add_new_user(name: str, email: str, password: str, score: int = 0) -> bool:
    if user_exists(email=email):
        return False

    session.add(User(name=name, email=email,
                     password=Password(password=password),
                     score=Score(score=score)))
    session.commit()

    return True


def get_user_score_by_id(user_id: int):
    user = get_user_by_id(user_id)
    return user.score


def set_user_score_by_id(user_id: int, new_score: int):
    session.query(Score).filter_by(user_id=user_id).update(
        values={"score": new_score})

    session.commit()


def delete_user_by_id(_id: int) -> None:
    session.query(User).filter_by(id=_id).delete()
    session.query(Password).filter_by(user_id=_id).delete()
    session.query(Score).filter_by(user_id=_id).delete()
    session.commit()


def delete_user_by_email(email: str) -> None:
    user_id = get_user_id_by_email(email)
    delete_user_by_id(user_id)
    session.commit()


def show_db(db_name) -> None:
    print(*session.query(db_name).all(), sep='\n')


if __name__ == "__main__":
    # add_new_user("alex", "sasha.flexer@gmail.com", "alex2008", 12)
    # add_new_user("daniel", "daniel.suh@email.ru", "danyaSuh!2009")
    # delete_user_by_email("sasha.flexer@gmail.com")
    # clear_db()
    # user_id = get_user_id_by_email("sasha.flexer@gmail.com")
    # set_user_score_by_id(user_id=user_id, new_score=22)
    show_db(User)
