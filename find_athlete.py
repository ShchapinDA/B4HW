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

class Athelete(Base):
    __tablename__ = "athelete"
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db():
    """
    Устанавливает соединение с БД, создает таблицы при их отсутствии и возвращает объект сессии
    """
    #создаем соединение к БД
    engine = sa.create_engine(DB_PATH)
    #создаем описанные таблицы
    Base.metadata.create_all(engine)
    #создаем фабрику сессию
    session = sessionmaker(engine)
    #возвращаем сессию
    return session()


def find(user_id, session):
    """
    Выводит атлета ближайшего по дате рождения и атлета, ближайшего по росту
    """
    #отображаем данные выбранного пользователя
    user_selected = session.query(User).filter(User.id == user_id).first()
    if user_selected:
        #если пользователь найден выводим информацию о нем
        print("Вы выбрали пользователя:\nИмя Фамилия: {} {}\nПол: {}\nE-mail: {}\nДата рождения: {}\nРост: {}\n".format(user_selected.first_name, user_selected.last_name, user_selected.gender, user_selected.email, user_selected.birthdate ,user_selected.height))
        #определяем намиболее близкое др. Для этого счиаем расстояние справа и слева от нашего значения, и которое меньше, то и берем
        nearest_by_birthdate_right = session.query(Athelete).filter(Athelete.birthdate >= user_selected.birthdate).order_by(Athelete.birthdate.asc(),Athelete.id.asc()).first()
        nearest_by_birthdate_left = session.query(Athelete).filter(Athelete.birthdate < user_selected.birthdate).order_by(Athelete.birthdate.desc(),Athelete.id.asc()).first()
        
        if nearest_by_birthdate_right:
            right=nearest_by_birthdate_right.birthdate   
        else:
            right = "3050-01-01" #костыль, так короче
        if nearest_by_birthdate_left:
            left = nearest_by_birthdate_left.birthdate
        else: 
            left = "1900-01-01" #костыль, так короче
        len_right = datetime.datetime.strptime(right,"%Y-%m-%d").date()-datetime.datetime.strptime(user_selected.birthdate,"%Y-%m-%d").date()
        len_left =  datetime.datetime.strptime(user_selected.birthdate,"%Y-%m-%d").date() - datetime.datetime.strptime(left,"%Y-%m-%d").date()
        if len_right <= len_left:
            print("Наиболее близкая дата рождения у: ", nearest_by_birthdate_right.name, nearest_by_birthdate_right.birthdate)
        else:
            print("Наиболее близкая дата рождения у: ", nearest_by_birthdate_left.name, nearest_by_birthdate_left.birthdate)
        
        #определяем намиболее близкий рост. Для этого счиаем расстояние справа и слева от нашего значения, и которое меньше, то и берем
        nearest_by_height_right = session.query(Athelete).filter(Athelete.height >= user_selected.height).order_by(Athelete.height.asc(),Athelete.id.asc()).first()
        nearest_by_height_left = session.query(Athelete).filter(Athelete.height < user_selected.height).order_by(Athelete.height.desc(),Athelete.id.asc()).first()
        
        if nearest_by_height_right:
            right=nearest_by_height_right.height   
        else:
            right = "4" #костыль, так короче
        if nearest_by_height_left:
            left = nearest_by_height_left.height
        else: 
            left = "0" #костыль, так короче
        len_right = right - user_selected.height
        len_left =  user_selected.height - left
        if len_right <= len_left:
            print("Наиболее близкий рост у: ", nearest_by_height_right.name, nearest_by_height_right.height)
        else:
            print("Наиболее близкий рост у: ", nearest_by_height_left.name, nearest_by_height_left.height)
    else:
        print("Пользователь с таким ИД не найден")

def main():
    """
    осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    #стартуем сессию
    session = connect_db()
    #запрашиваем ид пользователя
    user_id = input("Привет! Укажите ид пользователя: ")
    #вызываем функцию поиска по ид
    find(user_id, session)

if __name__ == "__main__":
    main()