# Импортируем необходимые модули
from flask import Flask, render_template, redirect, abort, request
from flask_sqlalchemy import SQLAlchemy
from os.path import dirname, exists, splitext, basename
from os import listdir

# Инициализируем приложение и базу данных
server = Flask(
    __name__, 
    root_path = dirname(__file__), 
    template_folder = f"{dirname(__file__)}/pages", 
    static_folder = f"{dirname(__file__)}/resources", 
    instance_path = f"{dirname(__file__)}/data"
)
server.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///posts.db"# Указываем адрес по которому будет доступна база данных

# Инициализируем базу данных
dataBase = SQLAlchemy(server)

# Определяем структуру записи данных
class Post(dataBase.Model):
    __tablename__ = 'posts'

    id = dataBase.Column(dataBase.Integer, primary_key = True, nullable = False, unique = True, autoincrement = True)
    title = dataBase.Column(dataBase.String(32), nullable = False)
    description = dataBase.Column(dataBase.String(128))
    text = dataBase.Column(dataBase.Text, nullable = False)
    author = dataBase.Column(dataBase.String(16))
    dateTime = dataBase.Column(dataBase.DateTime, nullable = False, server_default = dataBase.text("CURRENT_TIMESTAMP"))

    def __init__(self, title, description, text, author):
        self.title = title
        self.description = description
        self.text = text
        self.author = author

    def __repr__(self):
        return f"<Post {self.id}>"

# Маршрутизируем запросы страниц к серверу
@server.route("/", methods = ["get"])
def index():
    return redirect("/pages/dynamic/main")

@server.route("/pages/dynamic/<string:page>", methods = ["get"])
def page(page):
    if(exists(f"{server.root_path}{request.path}.html")):
        context = {
            "pages": [f"/dynamic/{splitext(basename(path))[0]}" for path in listdir(f"{server.template_folder}/dynamic")]
        }

        match page:
            case "posts":
                with server.app_context():
                    with dataBase.session() as session:
                        context["posts"] = session.query(Post).all()# Получем все записи находящиеся в базе данных и передаем их на страницу

        return render_template(f"/dynamic/{page}.html", context = context)
    
    else:
        return abort(404)

# Добавляем логику запросов на редактирование базы данных
@server.route("/api/posts/publish", methods = ["post"])
def publishPost():
    with server.app_context():
        with dataBase.session() as session:
            session.add(Post(request.form.get("title"), request.form.get("description"), request.form.get("text"), request.form.get("author")))
            session.commit()# Фиксируем изменения в базе данных

            return redirect("/pages/dynamic/posts")

@server.route("/api/posts/delete", methods = ["post"])
def deletePost():
    with server.app_context():
        with dataBase.session() as session:
            session.delete(session.get(Post, {# Находим запись с нужным id и удаляем её
                "id": request.form.get("id")
            }))
            session.commit()# Фиксируем изменения в базе данных

            return redirect("/pages/dynamic/posts")# Перенаправляем пользователя на обновлённую страницу #? передать статус код и изменить на клиенте

# Запускаем приложение
if(__name__ == "__main__"):
    with server.app_context():
        dataBase.create_all()# Создаем место хранения базы данных
        
        server.run()