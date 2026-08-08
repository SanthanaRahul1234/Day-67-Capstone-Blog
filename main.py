from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from db_manager import DbManager
from form_manager import Add_Post
import os


app = Flask(__name__)
# Initialize the CKEditor extension
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI','sqlite:///posts.db')
dbmanager = DbManager(app)

@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    posts = dbmanager.get_all_records()
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/show_post/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = dbmanager.get_record_by_id(post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    form = Add_Post()

    if form.validate_on_submit():
        #create record
        dbmanager.create_record(form.new_title.data, form.new_subtitle.data,form.new_author_name.data, form.new_url.data,  form.new_body.data )
        #return home
        return redirect(url_for('get_all_posts'))
    else:
        return render_template("make-post.html", form=form, is_edit=False)


# TODO: edit_post() to change an existing blog post
@app.route('/edit-post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = dbmanager.get_record_by_id(post_id)
    form = Add_Post()
    # 1. On GET request: Pre-fill the form manually from the database
    if request.method == 'GET':
        dbmanager.populate_form(form, post)

    # 2. On POST request: Validate and save back to the database
    if form.validate_on_submit():
        dbmanager.patch_record(post_id, form.new_title.data, form.new_subtitle.data, form.new_author_name.data, form.new_url.data, form.new_body.data)
        return redirect(url_for('show_post', post_id=post_id))

    return render_template("make-post.html", form=form, is_edit=True)


# TODO: delete_post() to remove a blog post from the database
@app.route('/delete/<post_id>')
def delete_post(post_id):
    dbmanager.delete_records(post_id)
    return redirect(url_for('get_all_posts'))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=False)
