import peewee
from database_manager import DatabaseManager
from local_settings import DATABASE
import numpy as np
import random


first_names = np.array(
    [
    'Macan', 'Hadi', 'Amir', 'Hassan', 'Hossein', 'Mehran', 'Mehrdad', 'Soroush',
    'Hassan', 'Mina', 'Mehrane', 'Samira', 'Negin', 'Hadis', 'Arman', 'Ahmad', 'Reza',
    'Hamid', 'Mohammad', 'Mohammadreza', 'Ali', 'Mahmod', 'Negar', 'Sarina', 'Armita'
    ]
)

last_names = np.array(
    [
    'Mehri', 'Khani', 'Amiri', 'Hassani', 'Hosseini', 'Mehrani', 'Mehrdadi', 'Soroushi',
    'Hassani', 'Minai', 'Mehranei', 'Samirai', 'Negini', 'Hadisi', 'Armani', 'Ahmadi', 'Rezai',
    'Hamidi', 'Mohammadi', 'Mohammadrezai', 'Asadi', 'Mahmodi', 'Negari', 'Sarinai', 'Armitai'
    ]
)

cities = np.array(
    [
        'Tehran', 'Gorgan', 'Ahvaz', 'Sari', 'Mashhad', 'Joybar', 'Esfahan', 'Shiraz', 'Rasht'
        'Karaj', 'Tabriz', 'Bojnord', 'Gonbad', 'Galogah', 'Sirjan', 'Sanandaj', 'kashan'
    ]
)

provices = np.array(
    [
        'Tehran', 'Esfahan', 'Fars', 'Mazandaran', 'Golestan', 'Khorasan Shomali',
        'Khorasan Razavi', 'Khorasan Jonobi', 'Gilan', 
    ]
)


def create_random_addresses():
    '''Creating random addresses and add to database'''
    for i in range(10):
        Address.create(
            city=random.choice(cities),
            provice=random.choice(provices),
            street=random.randint(0, 10_000),
            house_name=random.randint(0, 10_000),
        )


def create_random_people():
    '''Creating random person and add to database'''
    for i in range(10):
        Human.create(
            first_name=random.choice(first_names),
            last_name=random.choice(last_names),
            number=random.randint(1_000, 1_000_000_000_000),
            address=random.randint(1, 20)
        )


def create_random_phone_book():
    '''Creating random objects of phone book'''
    for i in range(20):
        PhoneBook.create(
            person=random.randint(1, 20),
            note=''
        )


# Connect to database useing database_manager
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
    provice = peewee.CharField(
        max_length=20,
        null=False,
        verbose_name='Provice'
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
        verbose_name='Address'
    )

    class Meta:
        database = database_manager.db


class PhoneBook(peewee.Model):
    '''A phonebook object'''
    person = peewee.ForeignKeyField(
        model=Human,
        null=False,
        verbose_name='Person'
    )
    note = peewee.TextField(
        null=True,
        verbose_name='Note'
    )

    class Meta:
        database = database_manager.db


if __name__ == '__main__':
    try:
        database_manager.create_tables(
            [Human, Address, PhoneBook]
        )
        # Created some random datas to make sure it is working correctly
        # create_random_addresses()
        # create_random_people()
        # create_random_phone_book()

        MENU = '''
1. Add new address.
2. Add new person.
3. Add new person to phonebook.
4. Add existed person to phonebook.
5. Change a persons info.
'''
        print(MENU)

    except ValueError as error:
        print('ValueError:', error)
    finally:
        # Closing database connection.
        if database_manager.db:
            database_manager.db.close()
            print('Database connection is closed')
