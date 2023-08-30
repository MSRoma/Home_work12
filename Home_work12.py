from collections import UserDict
from datetime import  date
import pickle

class Field:
    def __init__(self, value):
        self.value = value  

class Name(Field):
    pass

class Phone(Field):
    def is_valid(self):
        return True  

    def __set__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid phone")
        self.value = value

    def __get__(self):
        return self.value 

class Birthday(Field):
    def is_valid(self):
        return True 

    def __set__(self, instance, value):
        if not self.is_valid(value):
            raise ValueError("Invalid birthday")
        self.value = value

    def __get__(self):
        return self.value

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name 
        self.phones = phone
        self.birthday = birthday
        # if phone: 
        #     self.phones.append(phone)
      
    def input_error(input_func):  
        def output_func(*args):  
            try:
               result = input_func(*args)
               return result
            except KeyError:
                return "KeyError."
            except ValueError:
                return "ValueError."
            except IndexError:
                return "IndexError."

        return output_func
   
    @input_error
    def add_phone(self, phone: str):
        phone_number = Phone(phone) 
        self.phones.append(phone_number)
    @input_error
    def delete_phone(self, phone: str):
        for ph_obj in self.phones:
            if ph_obj.value == phone:
                self.phones.remove(ph_obj)
    @input_error
    def edit_phone(self, old_phone: str, new_phone: str):
        for ph_obj in self.phones:
            if ph_obj.value == old_phone:
                index = self.phones.index(old_phone)
                self.phones[index] = new_phone
    @input_error
    def days_to_birthday(self):
        date_now = date.today()
        birthday = date(date_now.year, self.birthday.value.month, self.birthday.value.day)
        if date_now < birthday :
            return  date(date_now.year, self.birthday.value.month, self.birthday.value.day) - date_now
        else:
            return  date(date_now.year + 1, self.birthday.value.month, self.birthday.value.day) - date_now

       
class AddressBook(UserDict):
    index = 0
    file_name = "data.bin"
    def add_record(self, rec):
        self.data[rec.name.value] = rec
 
    def __iter__(self):
        self._iter_index = 0
        return self  

    def __next__(self):
        if self.index < len(self.data):
            keys = list(self.data.keys())
            key = keys[self.index]
            self.index += 1
            return  self.data[key]
        else:
            raise StopIteration

    def dump(self):
        try:
            with open(self.file_name, "wb") as fh:
                pickle.dump(self.data, fh)
        except FileNotFoundError:
            return "FileNotFoundError."
            
    def load(self):
        try:
           with open(self.file_name, "rb") as fh:
            self.data = pickle.load(fh)
        except FileNotFoundError:
             return "FileNotFoundError."

    def search(self, search_str):
        results = []
        for key, i in self.data.items():
            a = i.phones.value 
            b = i.name.value
            if a.lower().find(search_str.lower()) != -1 or b.lower().find(search_str.lower()) != -1 :
                    results.append(i)
        return results  
              
if __name__ == "__main__":
    ab = AddressBook() 
   
    # name1 = Name('Bill')
    # phone1 = Phone("123456f790")
    # birthday1 = Birthday(date(2010, 8, 26))
    # rec1= Record(name1, phone1, birthday1)
    # ab.add_record(rec1)

    # name2 = Name('Bob')
    # phone2 = Phone('88')
    # birthday2 = Birthday(date(2008, 6, 11))
    # rec2= Record(name2, phone2, birthday2)
    # ab.add_record(rec2)

    ab.load()
    ab.dump()
    

for i in ab:
    print("______________________________________________________")
    print("Name:",i.name.value)
    print("Phones:",i.phones.value)
    print("Birthday:", i.birthday.value )
    print("Days to Birthday:", i.days_to_birthday())
    print("______________________________________________________")


results = ab.search("8")
if results:
    print("======================================================")
    print("Search results:")
    for record in results:
        print("======================================================")
        print("Name:", record.name.value)
        print("Phones:", record.phones.value)
        print("Birthday:", record.birthday.value)
        print("Days to Birthday:", record.days_to_birthday().days)
        print("======================================================")
else:
    print("No results.")