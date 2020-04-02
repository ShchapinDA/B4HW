"""
модуль регистрации новых пользователей
"""
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

DB_PATH = "sqlite:///Модуль B/B4. Работа с базами данных/Практическое задание/sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    """ Выполняет регистацию пользователей """
    # назание таблицы
    __tablename__ = "user"
    # поля таблицы
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


def connect_db():
    """Устанавливает соединение с БД, создает таблицы при их отсутствии, возвращает объект сессии"""
    # Соединение с БД
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем обьект сессии
    return session()


def request_data():
    """запрашивает у пользователя данные и добавляет их в список user"""
    print("Добрый день! Внесите данные о вас для регистации")
    first_name = input("Введите ваше Имя: ")
    last_name = input("Введите вашу Фамилию: ")
    gender = input("Введите ваш Пол: ")
    email = input("Введите ваш E-mail: ")
    birthdate = datetime.datetime.strptime(input("Введите вашу Дату рождения: "), "%d.%m.%Y").date()
    height = input("Введите ваш Рост: ")

    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user


def main():
    """осуществляем взаимодействие с пользователем """
    # стартуем сссию
    session = connect_db()
    # стартуем запрос данных пользователя
    user = request_data()
    # добавляем пользователя в сессию
    session.add(user)
    # пишем результаты сессии в БД
    session.commit()
    print("Спасибо. Данные сохранены")


if __name__ == "__main__":
    main()
