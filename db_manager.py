from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




class DbManager:
    def __init__(self, app):
        self.app = app
        # CREATE DATABASE
        class Base(DeclarativeBase):
            pass
        self.db = SQLAlchemy(model_class=Base)
        self.db.init_app(app)

        # CONFIGURE TABLE
        class BlogPost(self.db.Model):
            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            title: Mapped[str] = mapped_column(String(250), nullable=False)
            subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
            date: Mapped[str] = mapped_column(String(250), nullable=False, default=datetime.now().strftime("%B %d, %Y"))
            body: Mapped[str] = mapped_column(Text, nullable=False)
            author: Mapped[str] = mapped_column(String(250), nullable=False)
            img_url: Mapped[str] = mapped_column(String(250), nullable=False)

        self.BlogPost = BlogPost

        with app.app_context():
            self.db.create_all()


    def get_all_records(self):
        with self.app.app_context():
            result = self.db.session.execute(self.db.select(self.BlogPost))  # creates and SQL Select statement and executes it against Cafe model
            all_posts = result.scalars().all()  # converts result rows into python list of objects representing the cafes
            return all_posts

    def get_record_by_id(self, id):
        with self.app.app_context():
            query = self.db.select(self.BlogPost).where(
            self.BlogPost.id == id)  # first create a query to select things
            result = self.db.session.execute(query)  # excecute query using database session
            # create a result object to store rows of database
            record = result.scalar()
            return record

    def create_record(self, new_title, new_subtitle,new_author_name, new_url, new_body):
        with self.app.app_context():
            new_blog = self.BlogPost(title=new_title, subtitle=new_subtitle, body=new_body, author=new_author_name, img_url=new_url)
            self.db.session.add(new_blog)
            self.db.session.commit()

    def populate_form(self, form, post):
        form.new_title.data = post.title
        form.new_subtitle.data = post.subtitle
        form.new_author_name.data = post.author
        form.new_url.data = post.img_url
        form.new_body.data = post.body
        self.db.session.commit()

    def patch_record(self, blog_id, new_title, new_subtitle,new_author_name, new_url, new_body):
        with self.app.app_context():
            # 1. Locate the cafe in the database by its primary key (ID)
            blog_to_update = self.db.session.get(self.BlogPost, blog_id)
            # 2. If it exists, update the specific attribute and commit
            if blog_to_update:
                blog_to_update.title = new_title
                blog_to_update.subtitle = new_subtitle
                blog_to_update.author = new_author_name
                blog_to_update.img_url = new_url
                blog_to_update.body = new_body
                self.db.session.commit()

    def delete_records(self, blog_id):
        with self.app.app_context():
            query = self.db.select(self.BlogPost).where(self.BlogPost.id == blog_id)
            blog_to_delete = self.db.session.execute(statement=query).scalar()
            # or book_to_delete = db.get_or_404(Book, book_id)
            self.db.session.delete(blog_to_delete)
            self.db.session.commit()