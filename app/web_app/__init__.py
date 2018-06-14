from flask import Flask, render_template

from app.filter import filters_to_string
from app.storage import load

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    THREADS_PER_PAGE=4,
    CSRF_ENABLED=True,
    CSRF_SESSION_KEY="secret",
)


@app.route("/")
def hello():
    _, to_send = load()
    return render_template("cars.html", cars=to_send, filters=filters_to_string())
