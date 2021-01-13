from Dto import Supplier, Vaccine
from Repository import repo
import os


def receive(name, amount, date):
    supplier = repo.find_supplier(name=name)[0]
    supplier_id = supplier.id
    supplier_logistic_id = supplier.logistic
    vaccine_id = repo.get_max_vaccine_id() + 1
    repo.insert_vaccine(Vaccine(vaccine_id, date, supplier_id, amount))
    logistic = repo.find_logistic(id=supplier_logistic_id)[0]
    logistic_count_received = logistic.count_received
    repo.update_logistics({"count_received": (logistic_count_received + int(amount))},
                          {"id": int(supplier_logistic_id)})


def send(location, amount):
    clinic = repo.find_clinic(location=location)[0]
    clinic_demand = clinic[2]
    clinic_logistic = clinic[3]
    if amount >= clinic_demand:
        repo.update_clinics()
