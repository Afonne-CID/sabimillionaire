from flask import render_template, abort
from app.admin import blueprint

@blueprint.route('/admin', methods=['GET'])
def admin():
    ''''''
    abort(403)

@blueprint.route('/admin/', methods=['GET'])
def admin2():
    ''''''
    abort(403)

@blueprint.route('/restricted/admin', methods=['GET', 'POST'])
def restricted():
    ''''''