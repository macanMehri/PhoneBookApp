import peewee
from database_manager import DatabaseManager
from local_settings import DATABASE
import numpy as np
import random
import logging


logging.basicConfig(filename='Logs.log')


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
                logging.error(error)
            except peewee.IntegrityError as error:
                print('IntegrityError:', error)
                logging.error(error)
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
    print(new_address)
    return new_address


def update_phonebook_info(phonebook_id):
    '''Update phonebook information'''
    while True:
        print('1. Person info.\n'
              '2. Note.\n'
              '0. Exit changing.'
        )
        order = int(input('What do you want to change? '))
        match order:
            case 0:
                break
            case 1:
                person_id = PhoneBook.select(PhoneBook.person.id).where(PhoneBook.id==phonebook_id)
                update_persons_info(person_id=person_id)
            case 2:
                new_note = input('Please enter new note: ')
                phonebook = PhoneBook.update(note=new_note).where(PhoneBook.id==phonebook_id)
                phonebook.execute()


def update_address_info(address_id):
    '''Update an address information'''
    while True:
        print('1. Provice.\n'
              '2. City.\n'
              '3. Street.\n'
              '4. House name.\n'
              '0. Exit changing.'
        )
        order = int(input('What do you want to change? '))
        match order:
            case 0:
                break
            case 1:
                new_provice = input('Please enter new provice: ')
                address = Address.update(provice=new_provice).where(Address.id==address_id)
                address.execute()
            case 2:
                new_city = input('Please enter new city: ')
                address = Address.update(city=new_city).where(Address.id==address_id)
                address.execute()
            case 3:
                new_street = input('Please enter new street: ')
                address = Address.update(street=new_street).where(Address.id==address_id)
                address.execute()
            case 4:
                new_house_name = input('Please enter new house name: ')
                address = Address.update(house_name=new_house_name).where(Address.id==address_id)
                address.execute()


def update_persons_info(person_id):
    '''Update a persons information'''

    while True:
        print('1. First name.\n'
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
                            logging.error(error)
                        except peewee.IntegrityError as error:
                            print('IntegrityError:', error)
                            logging.error(error)
                        else:
                            break
                else:
                    new_address = add_new_address()
                person = Human.update(address=new_address).where(Human.id==person_id)
                person.execute()


def delete_person(person_id):
    '''Delete a person from database'''
    try:
        person = Human.delete().where(Human.id == person_id)
        person.execute()
    except peewee.IntegrityError as error:
        print('You cannot delete this person.')
        print('IntegrityError:', error)
        logging.error(error)


def delete_phonebook(phonebook_id):
    '''Delete an object from phonebook table'''
    phonebook = PhoneBook.delete().where(PhoneBook.id==phonebook_id)
    phonebook.execute()


def delete_address(address_id):
    '''Delete an object from address table'''
    try:
        address = Address.delete().where(Address.id==address_id)
        address.execute()
    except peewee.IntegrityError as error:
        print('You cannot delete this address.')
        print('IntegrityError:', error)
        logging.error(error)


def show_all_humans() -> None:
    '''Show all objects from human table'''
    people = Human.select()
    for person in people:
        print(person)
        print('-'*20)


def show_all_data() -> None:
    '''Show all datas from phonebook table'''
    datas = PhoneBook.select()
    for data in datas:
        print(data)
        print('-'*20)


def show_all_addresses() -> None:
    '''Show all objects from address table'''
    addresses = Address.select()
    for address in addresses:
        print(address)
        print('-'*20)


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
    def __str__(self) -> str:
        return (
            f'Address ID: {self.id}\n'
            f'{self.provice}-{self.city}-Street:{self.street}-Name:{self.house_name}'
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

    @property
    def full_name(self) -> str:
        '''Create fullname using firsname and lastname'''
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return (
            f'Person ID: {self.id}\n'
            f'Name: {self.full_name}\n'
            f'Number: {self.number}\n'
            f'Address:\n{self.address}'
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

    def __str__(self) -> str:
        return f'ID: {self.id}\n{self.person}\nNote: {self.note}'

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
6. Delete a person from human table.
7. Delete from phonebook.
8. Change phonebook info.
9. Change address info.
10. Delete an address from address table.
11. Create random addresses.
12. Create random people.
13. Add random people to phonebook.
14. Show all people.
15. Show all addresses.
16. Show all datas from phonebook.
'''
        while True:
            print(MENU)
            while True:
                order = int(input('Please enter your order: '))
                if 0 <= order < 20:
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
                case 6:
                    person_id = int(input('Please enter an id: '))
                    delete_person(person_id=person_id)
                case 7:
                    phonebook_id = int(input('Please enter an id: '))
                    delete_phonebook(phonebook_id=phonebook_id)
                case 8:
                    phonebook_id = int(input('Please enter an id: '))
                    update_phonebook_info(phonebook_id=phonebook_id)
                case 9:
                    address_id = int(input('Please enter an id: '))
                    update_address_info(address_id=address_id)
                case 10:
                    address_id = int(input('Please enter an id: '))
                    delete_address(address_id=address_id)
                case 11:
                    create_random_addresses()
                    print('Random addresses created.')
                case 12:
                    create_random_people()
                    print('Random people created.')
                case 13:
                    create_random_phone_book()
                    print('Random people added to phonebook.')
                case 14:
                    show_all_humans()
                case 15:
                    show_all_addresses()
                case 16:
                    show_all_data()

    except ValueError as error:
        print('ValueError:', error)
        logging.error(error)
    except Exception as error:
        print('ValueError:', error)
        logging.error(error)
    finally:
        # Closing database connection.
        if database_manager.db:
            database_manager.db.close()
            print('Database connection is closed')
