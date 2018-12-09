import argparse
import json
import sys
from contextlib import AbstractContextManager
from datetime import date
from math import ceil, inf

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import FlushError

Base = declarative_base()
engine = db.create_engine("sqlite:///ads.db", echo=False)
Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class Ad(Base):
    __tablename__ = "ads"

    id = db.Column(db.Integer, primary_key=True)
    settlement = db.Column(db.String)
    under_construction = db.Column(db.Boolean, index=True)
    description = db.Column(db.String)
    price = db.Column(db.Integer, index=True)
    oblast_district = db.Column(db.String, index=True)
    living_area = db.Column(db.Float)
    has_balcony = db.Column(db.Boolean)
    address = db.Column(db.String)
    construction_year = db.Column(db.Integer, index=True)
    rooms_number = db.Column(db.Integer)
    premise_area = db.Column(db.Float)
    active = db.Column(db.Boolean, index=True)

    def __str__(self):
        return "Ad: {}, {}, {}, {}, {}".format(
            self.id,
            self.settlement,
            self.price,
            self.under_construction,
            self.construction_year,
        )


def load_ads_from_json(json_filepath):
    with open(json_filepath) as json_file:
        ads_data = json.load(json_file)
        ads = [Ad(**ad_data) for ad_data in ads_data]
        return ads


class DBManager(AbstractContextManager):

    MIN_PRICE = 0
    MAX_PRICE = inf
    MAX_ADS_PER_PAGE = 15

    def __enter__(self):
        self.session = Session()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is not None:
            self.session.rollback()
        Session.remove()

    def save_ads(self, ads):
        for ad in ads:
            ad.active = True

        old_ads = self.session.query(Ad).all()
        for old_ad in old_ads:
            old_ad.active = False

        self.session.add_all(old_ads)
        self.session.add_all(ads)
        self.session.commit()

    def construct_query(
        self, oblast_district, min_price, max_price, new_buildings_only
    ):
        query = self.session.query(Ad)

        if new_buildings_only:
            year_difference = 2
            two_years_ago = date.today().year - year_difference
            new_building_condition = db.or_(
                Ad.under_construction.is_(True),
                Ad.construction_year >= two_years_ago,
            )
            query = query.filter(new_building_condition)

        if oblast_district is not None:
            query = query.filter_by(oblast_district=oblast_district)

        query = query.filter(Ad.price >= min_price, Ad.price <= max_price)
        query = query.filter(Ad.active.is_(True))
        return query

    def get_ads(
        self,
        oblast_district=None,
        min_price=MIN_PRICE,
        max_price=MAX_PRICE,
        new_buildings_only=False,
        max_ads=MAX_ADS_PER_PAGE,
        page=1,
    ):
        start = (page - 1) * max_ads
        query = self.construct_query(
            oblast_district, min_price, max_price, new_buildings_only
        )
        ads = query.order_by(Ad.price)[start : start + max_ads]
        return ads

    def get_total_pages(
        self,
        oblast_district=None,
        min_price=MIN_PRICE,
        max_price=MAX_PRICE,
        new_buildings_only=False,
        max_ads=MAX_ADS_PER_PAGE,
    ):
        query = self.construct_query(
            oblast_district, min_price, max_price, new_buildings_only
        )
        total_ads = query.count()
        total_pages = ceil(total_ads / max_ads)
        return total_pages


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filepath",
        help="Json file from which advertisments will be loaded",
        default="ads.json",
    )
    args = parser.parse_args()
    json_filepath = args.filepath
    Base.metadata.create_all(engine)
    with DBManager() as db_manager:
        try:
            db_manager.save_ads(load_ads_from_json(json_filepath))
        except FlushError as err:
            sys.exit(err)
