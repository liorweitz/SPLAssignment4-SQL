import sys

from Dto import Clinic, Vaccine, Logistic, Supplier
from Repository import repo


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
    clinic_id = clinic.id
    clinic_demand = clinic.demand
    clinic_logistic_id = clinic.logistic
    logistic = repo.find_logistic(id=clinic_logistic_id)[0]
    repo.update_logistics({"count_sent": logistic.count_sent+int(amount)}, {"id": clinic_logistic_id})
    if int(amount) >= clinic_demand:
        repo.update_clinics({"demand": 0}, {"id": clinic_id})
    else:
        repo.update_clinics({"demand": clinic_demand - int(amount)}, {"id": clinic_id})
    vaccines_to_send = int(amount)
    while vaccines_to_send != 0:
        earliest_date = repo.find_earliest()[0]
        earliest_vaccine = repo.find_vaccine(date=earliest_date)[0]
        earliest_vaccine_amount = earliest_vaccine.quantity
        if vaccines_to_send >= earliest_vaccine_amount:
            vaccines_to_send -= earliest_vaccine_amount
            repo.delete_vaccine(id=earliest_vaccine.id)
        else:
            repo.update_vaccines({"quantity": earliest_vaccine.quantity - vaccines_to_send},
                                 {"id": earliest_vaccine.id})
            vaccines_to_send = 0


def main():
    path_to_config_file = sys.argv[1]
    path_to_order_file = sys.argv[2]
    path_to_output_file = sys.argv[3]
    output = open(path_to_output_file, 'w')

    repo.create_tables()
    with open(path_to_config_file, "r") as file:
        objects_nums = file.readline()
        vaccines_num = int(objects_nums[0])
        suppliers_num = int(objects_nums[2])
        clinics_num = int(objects_nums[4])
        logistics_num = int(objects_nums[6])
        for i in range(vaccines_num):
            line = file.readline()
            line = line.rstrip('\n')
            repo.insert_vaccine(Vaccine(*(line.split(','))))
        for i in range(suppliers_num):
            line = file.readline()
            line = line.rstrip('\n')
            repo.insert_supplier(Supplier(*(line.split(','))))
        for i in range(clinics_num):
            line = file.readline()
            line = line.rstrip('\n')
            repo.insert_clinic(Clinic(*(line.split(','))))
        for i in range(logistics_num):
            line = file.readline()
            line = line.rstrip('\n')
            repo.insert_logistic(Logistic(*(line.split(','))))

    with open(path_to_order_file, "r") as file:
        for line in file:
            line = line.rstrip("\n")
            line = line.split(',')
            if len(line) == 3:
                receive(*line)
            else:
                send(*line)
            total_inventory = str(repo.sum_inventory()[0])
            total_demand = str(repo.sum_demand()[0])
            total_received = str(repo.sum_received()[0])
            total_send = str(repo.sum_sent()[0])
            stmt = total_inventory+","+total_demand+","+total_received+","+total_send+"\n"
            output.write(stmt)
    output.close()





if __name__ == '__main__':
    main()
