from flask import Flask, request, render_template, redirect, url_for
from utils.utils import Utils

app = Flask(__name__)


@app.route('/')
def index():
    """Load data from storage and use it to render an index page."""
    blog_posts = Utils.load_storage_data()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Create new post functionality."""
    if request.method == 'GET':
        return render_template('add.html')
    blog_posts = Utils.load_storage_data()
    new_post_title = request.form.get('title', '<blank>')
    new_post_author = request.form.get('author', '<blank>')
    new_post_content = request.form.get('content', '')
    new_post_id = Utils.get_unique_id()
    blog_posts.append(
        {"id": new_post_id, "author": new_post_author, "likes": 0,
         "title": new_post_title, "content": new_post_content}
    )
    Utils.write_data_to_storage(blog_posts)
    return redirect(url_for('index'))


@app.route('/delete/<int:post_id>', methods=['GET'])
def delete(post_id: int):
    """Rudimentary: if good id, remove the matching dict from storage. No
    indication of failure, just goes back to index either way."""
    blog_posts = Utils.load_storage_data()
    for bp in blog_posts:
        if bp.get('id') == post_id:
            blog_posts.remove(bp)
            Utils.write_data_to_storage(blog_posts)
            break
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id: int):
    """Update blog post (delete old, save data to storage with new). Retains
    unique id. If bad post_id, early exit back to index. If 'GET', display
    update.html; else (means method == 'POST') format POSTed data into dict,
    remove the previously stored dict, then dump with new dict to json."""
    if post_id not in Utils.list_extant_ids():
        return redirect(url_for('index'))
    blog_posts = Utils.load_storage_data()
    post_to_upd = next(bp for bp in blog_posts if bp['id'] == post_id)
    if request.method == 'GET':
        return render_template('update.html').format(
            post_id,
            post_to_upd.get('title', '<untitled>'),
            post_to_upd.get('author', '<unknown>'),
            post_to_upd.get('content', '<unpopulated>')
        )
    new_post_title = request.form.get('title', '<blank>')
    new_post_author = request.form.get('author', '<blank>')
    new_post_content = request.form.get('content', '')
    blog_posts.append(
        {"id": post_id, "author": new_post_author,
         "likes": post_to_upd.get("likes", 0),
         "title": new_post_title, "content": new_post_content}
    )
    blog_posts.remove(post_to_upd)
    Utils.write_data_to_storage(blog_posts)
    return redirect(url_for('index'))


@app.route('/like/<int:post_id>', methods=['GET'])
def like(post_id: int):
    """Increment the number of likes for the post with post_id."""
    if post_id not in Utils.list_extant_ids():
        return redirect(url_for('index'))
    blog_posts = Utils.load_storage_data()
    next(blog_posts[i].update({"likes": bp.get("likes", 0) + 1})
         for i, bp in enumerate(blog_posts) if bp['id'] == post_id)
    Utils.write_data_to_storage(blog_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
