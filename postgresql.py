from peewee import *


pg_db = PostgresqlDatabase('DataOx', user='postgres', password='0000', host='localhost', port=5432)


class DataModel(Model):
    class Meta:
        database = pg_db
    name = CharField(max_length=200, null=False)
    price = DecimalField(default=None)
    image = CharField(max_length=200, null=False)
    description = TextField()
    date = DateField(null=False)
    city = CharField(max_length=100, null=False)
    beds = CharField(max_length=100, null=False)
    currency = CharField(max_length=3, default='$', null=False)


def write_in_sql(name, price, image, description, city, beds, date):
    try:
        pg_db.connect()
        pg_db.create_tables([DataModel])
        pg_db.close()
    except:
        pass
    if price == None:
        with pg_db:
            DataModel(name=name, currency='-', image=image, description=description,
                      city=city, beds=beds, date=date).save()
    else:
        with pg_db:
            DataModel(name=name, price=price, image=image, description=description,
                      city=city, beds=beds, date=date).save()
