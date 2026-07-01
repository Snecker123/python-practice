# class Person

"""
1. Model the following
a) A PhoneBook class that has a list of contacts
The PhoneBook should support the following
- ability to add contacts (check for phone number uniqueness)
- ability to remove contacts
- ability to check if a phone number is already in the contacts list
- a display method that shows all contacts in a pretty way

b) 3 different types of contacts, Friend, Colleague, Relative, having the following attributes

Friend:
- name
- phone number
- favorite activity
Colleague:
- name
- phone number
- place of work
Relative
- name
- phone number
- type of relative (ex: mother, brother, etc.)

The contacts should support the following:
- equality comparison
- string representation
"""

class Contact:
    def __init__(self, name: str, phone_number: str):
        self.name = name
        self.phone_number = phone_number


    def __eq__(self, other):
        return self.name == other.name and self.phone_number == other.phone_number




class Friend(Contact):
    def __init__(self, name: str, phone_number: str, favorite_activity=None):
        super().__init__(name, phone_number)
        self.favorite_activity = favorite_activity


    def __str__(self):
        return f"name:\t{self.name}\nphone number:\t{self.phone_number}\nfavorite activity:\t{self.favorite_activity}"


    def print_friend(self):
        print(self)


    def __eq__(self, other):
        return super().__eq__(other)




class Colleague(Contact):
    def __init__(self, name: str, phone_number: str, place_of_work=None):
        super().__init__(name, phone_number)
        self.place_of_work = place_of_work


    def __str__(self):
        return f"name:\t{self.name}\nphone number:\t{self.phone_number}\nfavorite activity:\t{self.place_of_work}"


    def print_colleague(self):
        print(self)


    def __eq__(self, other):
        return super().__eq__(other)




class Relative(Contact):
    def __init__(self, name: str, phone_number: str, relative_type=None):
        super().__init__(name, phone_number)
        self.relative_type = relative_type


    def __str__(self):
        return f"name:\t{self.name}\nphone number:\t{self.phone_number}\nfavorite activity:\t{self.relative_type}"


    def print_relative(self):
        print(self)


    def __eq__(self, other):
        return super().__eq__(other)




class Phonebook:
    def __init__(self, contacts):
        self.contacts = contacts


    def add_contacts(self, contact):
        if not self.is_in_contacts(contact):
            self.contacts.append(contact)


    def is_in_contacts(self, contact) -> bool:
        if contact in self.contacts:
            return True
        return False

    def print_contacts(self):
        for i in self.contacts:
            print(i)

    def remove_contact(self, contact):
        if contact in self.contacts:
            self.contacts.remove(contact)
            print(f"Contactul {contact.name} a fost șters.")
        else:
            print(f"Contactul {contact.name} nu există în agendă.")






prieten1 = Friend("Andronie", "123", "Fotbal")
prieten2 = Friend("Laura", "321", "Bataie")

ruda1 = Relative("Tiberiu", "07 n-am cartela", "varu")

lista = []

agenda = Phonebook(lista)

agenda.add_contacts(prieten1)
agenda.add_contacts(prieten2)

agenda.print_contacts()

agenda.add_contacts(ruda1)

agenda.print_contacts()

agenda.remove_contact(prieten1)
agenda.print_contacts()