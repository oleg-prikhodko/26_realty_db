import os

from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_parameter

from persistence import DBManager
from settlements import SETTLEMENTS

app = Flask(__name__)


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
        total_ads = db_manager.get_total_ads(**kwargs)
        page = request.args.get(get_page_parameter(), type=int, default=1)
        kwargs["page"] = page
        ads = db_manager.get_ads(**kwargs)

        pagination = Pagination(
            page=page,
            total=total_ads,
            record_name="ads",
            per_page=DBManager.MAX_ADS_PER_PAGE,
            css_framework="bootstrap",
            bs_version=3,
        )

        return render_template(
            "ads_list.html",
            ads=ads,
            settlement_groups=SETTLEMENTS,
            pagination=pagination,
        )


if __name__ == "__main__":
    debug = bool(os.environ.get("FLASK_DEBUG", False))
    app.run(debug=debug)
