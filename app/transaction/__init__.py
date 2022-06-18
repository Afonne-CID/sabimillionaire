from flask import Blueprint

blueprint = Blueprint(
    'transaction_blueprint',
    __name__,
    url_prefix=''
)
