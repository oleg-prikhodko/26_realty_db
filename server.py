import os

from flask import Flask, render_template, request

from persistence import DBManager
from settlements import SETTLEMENTS

app = Flask(__name__)


def make_pages_list(current_page, total_pages):
    if current_page == 1:
        start, end = current_page, current_page + 3
    elif current_page == total_pages:
        start, end = current_page - 2, current_page + 1
    else:
        start, end = current_page - 1, current_page + 2

    pages = [
        page for page in range(start, end) if page >= 1 and page <= total_pages
    ]
    return pages


@app.route("/")
def ads_list():
    kwargs = {
        "oblast_district": request.args.get("oblast_district"),
        "max_price": request.args.get("max_price", type=int),
        "min_price": request.args.get("min_price", type=int),
        "new_buildings_only": request.args.get("new_building", type=bool),
    }
    kwargs = {key: value for key, value in kwargs.items() if value is not None}

    with DBManager() as db_manager:
        total_pages = db_manager.get_total_pages(**kwargs)
        page = request.args.get("page", 1, type=int)
        if page < 1 or page > total_pages:
            page = 1
        kwargs["page"] = page

        ads = db_manager.get_ads(**kwargs)
        return render_template(
            "ads_list.html",
            ads=ads,
            current_page=page,
            pages=make_pages_list(page, total_pages),
            total_pages=total_pages,
            settlement_groups=SETTLEMENTS,
        )


if __name__ == "__main__":
    debug = bool(os.environ.get("FLASK_DEBUG", False))
    app.run(debug=debug)
