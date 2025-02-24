import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://root:te9GmgGXIUlsC0vyP8Mx55o1VYbFIe0d@dpg-cups6bdsvqrc73f5b4gg-a.oregon-postgres.render.com/cetech_oj50')
    SQLALCHEMY_TRACK_MODIFICATIONS = False