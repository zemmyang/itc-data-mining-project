from sqlalchemy import create_engine, MetaData, Table, Column, String, ForeignKey
from sqlalchemy.schema import DropSchema
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATE
from sqlalchemy_utils import database_exists, create_database
import json
import os
from BBBScraper import internal_config as ICFG


def get_sql_credentials():
    with open(ICFG.BBBORG_JSON_FILE) as f:
        json_file = json.load(f)
    return json_file


def clear_schema():
    cred = get_sql_credentials()
    DropSchema(cred["sql_db"])


def create_sql_engine():
    cred = get_sql_credentials()
    engine = \
        create_engine(f'mysql+pymysql://{cred["sql_user"]}:{cred["sql_password"]}@{cred["sql_host"]}/{cred["sql_db"]}',
                      echo=True)

    return engine


def check_schema(engine):
    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        engine.connect()


def create_categories_table(engine):
    meta = MetaData()

    Table(
        'categories', meta,
        Column('category_id', INTEGER(4, zerofill=True), primary_key=True),
        Column('category_name', String(100)),
    )

    meta.create_all(engine, checkfirst=True)


def create_all_tables(engine):
    meta = MetaData()

    Table(
        'business_profile', meta,
        Column('business_id', String(28), primary_key=True),
        Column('business_name', String(100)),
        Column('alerts', String(100)),
        Column('location', String(400)),
        Column('website', String(50)),
        Column('phone_number', String(20)),
        Column('bbb_file_opened', String(15)),
        Column('type_of_entity', String(45)),
        Column('bbb_rating', String(5)),
    )

    Table(
        'categories', meta,
        Column('category_id', INTEGER(8, zerofill=True), primary_key=True),
        Column('category_name', String(100)),
    )

    Table(
        'complaints', meta,
        Column('complaints_id', INTEGER(8, zerofill=True), primary_key=True),
        Column('adverting_sales', INTEGER, nullable=True),
        Column('billing_collections', INTEGER, nullable=True),
        Column('guarantee_warranty', INTEGER, nullable=True),
        Column('problem_product_service', INTEGER, nullable=True),
        Column('business_profile_business_id', VARCHAR(28), ForeignKey('business_profile.business_id')),
    )

    Table(
        'reviews', meta,
        Column('reviews_id', INTEGER(8, zerofill=True), primary_key=True),
        Column('name', VARCHAR(45), nullable=True),
        Column('review_text', String, nullable=True),
        Column('date', DATE, nullable=True),
        Column('star_rating', INTEGER, nullable=True),
    )

    Table(
        'business_profile_has_categories', meta,
        Column('business_profile_business_id', VARCHAR(28), primary_key=True),
        Column('business_profile_business_id', VARCHAR(28), ForeignKey('business_profile.business_id')),
        Column('categories_category_id', VARCHAR(28), ForeignKey('categories.category_id')),
    )

    Table(
        'reviews_has_business_profile', meta,
        Column('reviews_idreviews', INTEGER, primary_key=True),
        Column('reviews_idreviews', VARCHAR(28), ForeignKey('reviews.reviews_id')),
        Column('business_profile_business_id', VARCHAR(28), ForeignKey('business_profile.business_id')),
    )

    meta.create_all(engine, checkfirst=True)

