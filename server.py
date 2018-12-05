from flask import Flask, render_template

from persistence import DBManager

app = Flask(__name__)


@app.route("/")
def ads_list():
    with DBManager() as db_manager:
        ads = db_manager.get_ads()
        return render_template("ads_list.html", ads=ads)


if __name__ == "__main__":
    app.run()
