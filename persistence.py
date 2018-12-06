import json
from contextlib import AbstractContextManager
from datetime import date
from math import ceil, inf

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Ad(Base):
    __tablename__ = "ads"

    id = db.Column(db.Integer, primary_key=True)
    settlement = db.Column(db.String)
    under_construction = db.Column(db.Boolean)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    oblast_district = db.Column(db.String)
    living_area = db.Column(db.Float)
    has_balcony = db.Column(db.Boolean)
    address = db.Column(db.String)
    construction_year = db.Column(db.Integer)
    rooms_number = db.Column(db.Integer)
    premise_area = db.Column(db.Float)
    active = db.Column(db.Boolean)

    def __str__(self):
        return "Ad: {}, {}, {}, {}, {}".format(
            self.id,
            self.settlement,
            self.price,
            self.under_construction,
            self.construction_year,
        )


def load_ads_from_json(json_filepath="ads.json"):
    with open(json_filepath) as json_file:
        ads_data = json.load(json_file)
        ads = [Ad(**ad_data) for ad_data in ads_data]
        return ads


class DBManager(AbstractContextManager):
    def __enter__(self):
        self.engine = db.create_engine("sqlite:///ads.db", echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is not None:
            self.session.rollback()
        self.session.close()
        self.Session.close_all()
        self.engine.dispose()

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
        self,
        oblast_district,
        min_price,
        max_price,
        new_buildings_only,
    ):
        query = self.session.query(Ad)

        if new_buildings_only:
            year_difference = 2
            two_years_ago = date.today().year - year_difference
            query = query.filter(
                db.or_(
                    Ad.under_construction.is_(True),
                    Ad.construction_year >= two_years_ago,
                )
            )

        if oblast_district is not None:
            query = query.filter_by(oblast_district=oblast_district)

        query = query.filter(Ad.price >= min_price, Ad.price <= max_price)
        return query

    def get_ads(
        self,
        oblast_district=None,
        min_price=0,
        max_price=inf,
        new_buildings_only=False,
        max_ads=15,
        page=1,
    ):
        start = (page - 1) * max_ads
        query = self.construct_query(
            oblast_district,
            min_price,
            max_price,
            new_buildings_only,
        )
        ads = query.order_by(Ad.price)[start : start + max_ads]
        return ads

    def get_total_pages(
        self,
        oblast_district=None,
        min_price=0,
        max_price=inf,
        new_buildings_only=False,
        max_ads=15,
    ):
        query = self.construct_query(
            oblast_district,
            min_price,
            max_price,
            new_buildings_only,
        )
        total_ads = query.count()
        total_pages = ceil(total_ads / max_ads)
        return total_pages


if __name__ == "__main__":
    with DBManager() as db_manager:
        db_manager.save_ads(load_ads_from_json())
