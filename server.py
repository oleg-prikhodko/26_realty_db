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
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    with DBManager() as db_manager:
        total_pages = db_manager.get_total_pages()
        ads = db_manager.get_ads(page=page)

        return render_template(
            "ads_list.html",
            ads=ads,
            current_page=page,
            pages=make_pages_list(page, total_pages),
            total_pages=total_pages,
        )


if __name__ == "__main__":
    app.run()
