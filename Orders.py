from Dto import Supplier
from Repository import repo


def receive(name, amount, date):
    supplier = repo.find_supplier(name)



def send(location, amount):
    print("send")
