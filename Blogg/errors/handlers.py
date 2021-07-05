from flask import Blueprint, render_template, make_response

errors = Blueprint('errors', __name__)


@errors.errorhandler(400)
def bad_request():
    #make_response sends ('data to render', http code, json/string data)
    return make_response(
        render_template("errors/400.html"),
        400
    )

@errors.app_errorhandler(404)
def error_404(error):
    return make_response(
        render_template('errors/404.html'),
        404
    )

@errors.app_errorhandler(403)
def error_403(error):
    return make_response(
        render_template('errors/403.html'), 
        403
    )

@errors.app_errorhandler(500)
def error_500(error):
    return make_response(
        render_template('errors/500.html'), 
        500
    )