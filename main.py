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


def add_new_person():
    '''Create a person with user inputs'''
    while True:
        first_name = input('Please enter your name: ').capitalize()
        if not first_name.isnumeric() and len(first_name) > 3:
            break
        print('This name is not allowed! Please try again.')
    while True:
        last_name = input('Please enter your last name: ').capitalize()
        if not last_name.isnumeric() and len(last_name) > 3:
            break
        print('This last name is not allowed! Please try again.')
    while True:
        number = input('Please enter your number: ')
        if number.isnumeric() and len(number) > 3:
            break
        print('This number is not allowed! Please try again.')
    while True:
        order = input(
            'Do you want to use an existed address?(Y/N): '
        )
        if order == 'Y' or order == 'N':
            break
        print('I cannot understand! Please try again.')
    if order == 'Y':
        while True:
            try:
                address_id = int(input('Please enter an address id: '))
            except ValueError as error:
                print('ValueError:', error)
            except peewee.IntegrityError as error:
                print('IntegrityError:', error)
            else:
                break
    else:
        address_id = add_new_address()

    new_person = Human.create(
        first_name=first_name,
        last_name=last_name,
        number=number,
        address=address_id
    )
    return new_person


def add_new_to_phone_book(person_id=None):
    '''Create and add new person to phone book'''
    if not person_id:
        person_id = add_new_person()
    note = input('If you want to add note, type here: ')
    PhoneBook.create(
        person=person_id,
        note=note
    )



def add_new_address():
    '''Create an address with user inputs'''  
    while True:
        provice = input('Please enter your provice: ').capitalize()
        if not provice.isnumeric() and len(provice) > 3:
            break
        print('This provice name is not allowed! Please try again.').capitalize()
    while True:
        city = input('Please enter your city: ').capitalize()
        if not city.isnumeric() and len(city) > 3:
            break
        print('This city name is not allowed! Please try again.')
    street = input('Please enter your street: ').capitalize()
    house_name = input('Please enter your house name: ').capitalize()

    new_address = Address.create(
        city=city,
        provice=provice,
        street=street,
        house_name=house_name
    )
    return new_address


def update_persons_info(person_id):
    '''Update a persons information'''

    while True:
        print('1. First name\n'
              '2. Last name.\n'
              '3. Number.\n'
              '4. Address.\n'
              '0. Exit changing.'
        )
        order = int(input('What do you want to change? '))
        match order:
            case 0:
                break
            case 1:
                while True:
                    new_name = input('Please enter new name: ').capitalize()
                    if not new_name.isnumeric() and len(new_name) > 3:
                        break
                    print('This name is not allowed! Please try again.')
                person = Human.update(first_name=new_name).where(Human.id==person_id)
                person.execute()
            case 2:
                while True:
                    new_last_name = input('Please enter new last name: ').capitalize()
                    if not new_last_name.isnumeric() and len(new_last_name) > 3:
                        break
                    print('This last name is not allowed! Please try again.')
                person = Human.update(last_name=new_last_name).where(Human.id==person_id)
                person.execute()
            case 3:
                while True:
                    new_number = input('Please enter new number: ')
                    if new_number.isnumeric() and len(new_number) > 3:
                        break
                    print('This number is not allowed! Please try again.')
                person = Human.update(number=new_number).where(Human.id==person_id)
                person.execute()
            case 4:
                while True:
                    order = input(
                        'Do you want to use an existed address?(Y/N): '
                    )
                    if order == 'Y' or order == 'N':
                        break
                    print('I cannot understand! Please try again.')
                if order == 'Y':
                    while True:
                        try:
                            new_address = int(input('Please enter an address id: '))
                        except ValueError as error:
                            print('ValueError:', error)
                        except peewee.IntegrityError as error:
                            print('IntegrityError:', error)
                        else:
                            break
                else:
                    new_address = add_new_address()
                person = Human.update(address=new_address).where(Human.id==person_id)
                person.execute()





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
        # Create tables
        database_manager.create_tables(
            [Human, Address, PhoneBook]
        )

        MENU = '''
0. Exit.
1. Add new address.
2. Add new person.
3. Add new person to phonebook.
4. Add existed person to phonebook.
5. Change a persons info.
6. Delete a person from phonebook.
7. Create random addresses.
8. Create random people.
9. Add random people to phonebook.
'''
        while True:
            print(MENU)
            while True:
                order = int(input('Please enter your order: '))
                if 0 <= order < 7:
                    break
                print('You enter wrong number! Please try again.')
            match order:
                case 0:
                    break
                case 1:
                    add_new_address()
                case 2:
                    add_new_person()
                case 3:
                    add_new_to_phone_book()
                case 4:
                    person_id = int(input('Please enter an id: '))
                    add_new_to_phone_book(person_id=person_id)
                case 5:
                    person_id = int(input('Please enter an id: '))
                    update_persons_info(person_id=person_id)
                case 7:
                    create_random_addresses()
                    print('Random addresses created.')
                case 8:
                    create_random_people()
                    print('Random people created.')
                case 9:
                    create_random_phone_book()
                    print('Random people added to phonebook.')

    except ValueError as error:
        print('ValueError:', error)
    finally:
        # Closing database connection.
        if database_manager.db:
            database_manager.db.close()
            print('Database connection is closed')
