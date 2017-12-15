import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

CSRF_ENABLED = True
SECRET_KEY = 'ABC123'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]


# PostgreSQL settings

# http://blog.theodo.fr/2017/03/developping-a-flask-web-app-with-a-postresql-database-making-all-the-possible-errors/
POSTGRES = {
    'host': os.environ['POSTGRES_HOST'],
    'user': os.environ['POSTGRES_USER'],
    'pw': os.environ['POSTGRES_PASSWORD'],
    'db': os.environ['POSTGRES_DB'],
    'port': '5432',
}


SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')