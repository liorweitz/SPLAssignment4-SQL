import sys

from Dto import Clinic, Vaccine, Logistic, Supplier
from Orders import receive, send
from Repository import repo


def initialize(path):
    repo.create_tables()
    with open(path, "r") as file:
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


def main():
    path_to_config_file = sys.argv[1]
    path_to_order_file = sys.argv[2]
    path_to_output_file = sys.argv[3]

    # initialize(path_to_config_file)
    with open(path_to_order_file, "r") as file:
        for line in file:
            line = line.rstrip("\n")
            line = line.split(',')
            if len(line) == 3:
                receive(*line)
            else:
                send(*line)


if __name__ == '__main__':
    main()
