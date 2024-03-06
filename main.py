import peewee
from database_manager import DatabaseManager
from local_settings import DATABASE


database_manager = DatabaseManager(
    database_name=DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)


class Address(peewee.Model):
    '''An address object'''

    city = peewee.CharField(
        max_length=20,
        null=False,
        verbose_name='City'
    )
    country = peewee.CharField(
        max_length=20,
        null=False,
        verbose_name='Country'
    )
    state = peewee.CharField(
        max_length=20,
        null=False,
        verbose_name='State'
    )
    street = peewee.CharField(
        max_length=255,
        null=False,
        verbose_name='Street'
    )
    house_name = peewee.CharField(
        max_length=255,
        null=False,
        verbose_name='House Name'
    )


    class Meta:
        database = database_manager.db



class Human(peewee.Model):
    '''A human object'''
    first_name = peewee.CharField(
        max_length=50,
        null=False,
        verbose_name='First Name'
    )
    last_name = peewee.CharField(
        max_length=50,
        null=False,
        verbose_name='Last Name'
    )
    number = peewee.CharField(
        max_length=20,
        null=False,
        verbose_name='Number'
    )
    address = peewee.ForeignKeyField(
        model=Address,
        null=False,
        verbos_name='Address'
    )

    class Meta:
        database = database_manager.db


class PhoneBook(peewee.Model):
    '''A phonebook object'''
    person = peewee.ForeignKeyField(
        model=Human,
        null=False,
        verbos_name='Person'
        )
    note = peewee.TextField(
        null=True,
        verbose_name='Note'
    )

    class Meta:
        database = database_manager.db
