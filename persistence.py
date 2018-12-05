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
        ads = [
            Ad(
                id=ad_data.get("id"),
                settlement=ad_data.get("settlement"),
                under_construction=ad_data.get("under_construction"),
                description=ad_data.get("description"),
                price=ad_data.get("price"),
                oblast_district=ad_data.get("oblast_district"),
                living_area=ad_data.get("living_area"),
                has_balcony=ad_data.get("has_balcony"),
                address=ad_data.get("address"),
                construction_year=ad_data.get("construction_year"),
                rooms_number=ad_data.get("rooms_number"),
                premise_area=ad_data.get("premise_area"),
            )
            for ad_data in ads_data
        ]
        return ads


def save_ads(ads):
    session.add_all(ads)
    session.commit()


def get_ads(settlement=None, price=0, max_ads=15, page=1):
    start = (page - 1) * max_ads
    query = session.query(Ad)
    if settlement is not None:
        query = query.filter_by(settlement=settlement)

    for ad in query.filter(Ad.price >= price)[start : start + max_ads]:
        print(ad.id, ad.settlement, ad.address, ad.price)


if __name__ == "__main__":
    engine = db.create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    save_ads(load_ads_from_json())
    get_ads("Вологда", 5000000)  # "Вологда"
