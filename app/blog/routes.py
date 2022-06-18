from flask import render_template
from app.blog import blueprint

@blueprint.route('/retrieve-blogs', methods=['GET', 'POST'])
def blogs():
    ''''''
    return render_template('home/home.html')