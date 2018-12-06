import os

from flask import Flask, render_template, request

from persistence import DBManager

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
    oblast_district = request.args.get("oblast_district")
    # TODO convert args to appropriate types
    max_price = request.args.get("max_price")
    try:
        min_price = int(request.args.get("min_price", 0))
        new_building = bool(request.args.get("new_building", False))
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1
        new_building = False
        min_price = 0

    with DBManager() as db_manager:
        total_pages = db_manager.get_total_pages(
            oblast_district=oblast_district,
            new_buildings_only=new_building,
            min_price=min_price,
        )
        ads = db_manager.get_ads(
            oblast_district=oblast_district,
            new_buildings_only=new_building,
            min_price=min_price,
        )
        return render_template(
            "ads_list.html",
            ads=ads,
            current_page=page,
            pages=make_pages_list(page, total_pages),
            total_pages=total_pages,
        )


if __name__ == "__main__":
    debug = bool(os.environ.get("FLASK_DEBUG", False))
    app.run(debug=debug)
