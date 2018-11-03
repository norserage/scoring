from flask import render_template
from ScoringEngine.web import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        "errors/404.html",
        title="Page Not Found"
    ), 404


@app.errorhandler(413)
def max_upload_exceded(e):
    return render_template(
        "errors/413.html",
        title="Max Upload Exceeded"
    ), 413


@app.errorhandler(500)
def server_error(e):
    return render_template(
        "errors/500.html",
        title="Server Error"
    ), 500
