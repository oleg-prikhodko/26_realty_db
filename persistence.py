import json

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


def load_ads_from_json(json_filepath="ads.json"):
    with open(json_filepath) as json_file:
        ads_data = json.load(json_file)
        ads = [Ad(**ad_data) for ad_data in ads_data]
        return ads


def save_ads(ads):
    session.add_all(ads)
    session.commit()


def get_ads(settlement=None, price=0, max_ads=15, page=1):
    start = (page - 1) * max_ads
    query = session.query(Ad)
    if settlement is not None:
        query = query.filter_by(settlement=settlement)

    ads = query.filter(Ad.price >= price).order_by(Ad.price)[
        start : start + max_ads
    ]
    return ads


if __name__ == "__main__":
    engine = db.create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    save_ads(load_ads_from_json())
    ads = get_ads("Вологда", 3000000)  # "Вологда"
    for ad in ads:
        print(ad.id, ad.settlement, ad.address, ad.price)
