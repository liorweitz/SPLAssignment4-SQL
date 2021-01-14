import atexit
import sqlite3

from Dao import Dao
from Dto import Vaccine, Supplier, Clinic, Logistic


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect("database.db")
        self._vaccines = Dao(Vaccine, self._conn)
        self._suppliers = Dao(Supplier, self._conn)
        self._clinics = Dao(Clinic, self._conn)
        self._logistics = Dao(Logistic, self._conn)
        self._max_vaccine_id = 0

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE IF NOT EXISTS logistics (
            id              INT     PRIMARY KEY, 
            name            STRING    NOT NULL,
            count_sent      INT     NOT NULL,
            count_received  INT     NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS suppliers (
            id          INT     PRIMARY KEY,
            name        STRING    NOT NULL,
            logistic    INT     NOT NULL,
            FOREIGN KEY (logistic)  REFERENCES logistics(id)
        );
        
        CREATE TABLE IF NOT EXISTS clinics (
            id          INT     PRIMARY KEY,
            location    STRING    NOT NULL,
            demand      INT     NOT NULL,
            logistic    INT,
            FOREIGN KEY (logistic)  REFERENCES logistics(id)
        );
        
        CREATE TABLE IF NOT EXISTS vaccines (
            id          INT     PRIMARY KEY,
            date        DATE    NOT NULL,
            supplier    INT,
            quantity    INT     NOT NULL,
            FOREIGN KEY (supplier) REFERENCES suppliers(id) 
        );
        """)

    def insert_vaccine(self, vaccine):
        self._max_vaccine_id += 1
        self._vaccines.insert(vaccine)

    def insert_supplier(self, supplier):
        self._suppliers.insert(supplier)

    def insert_clinic(self, clinic):
        self._clinics.insert(clinic)

    def insert_logistic(self, logistic):
        self._logistics.insert(logistic)
        
    def find_logistic(self, **keyvals):
        return self._logistics.find(**keyvals)

    def find_supplier(self, **keyvals):
        return self._suppliers.find(**keyvals)

    def find_clinic(self, **keyvals):
        return self._clinics.find(**keyvals)

    def find_vaccine(self, **keyvals):
        return self._vaccines.find(**keyvals)

    def find_earliest(self):
        c = self._conn.cursor()
        c.execute('SELECT MIN(date) FROM vaccines')
        return c.fetchone()

    def update_logistics(self, set_values, condition):
        self._logistics.update(set_values, condition)

    def update_clinics(self, set_values, condition):
        self._clinics.update(set_values, condition)

    def update_vaccines(self, set_values, condition):
        self._vaccines.update(set_values, condition)

    def delete_vaccine(self, **keyvals):
        self._vaccines.delete(**keyvals)

    def sum_inventory(self):
        c = self._conn.cursor()
        c.execute('SELECT SUM(quantity) FROM vaccines')
        return c.fetchone()

    def sum_demand(self):
        c = self._conn.cursor()
        c.execute('SELECT SUM(demand) FROM clinics')
        return c.fetchone()

    def sum_received(self):
        c = self._conn.cursor()
        c.execute('SELECT SUM(count_received) FROM logistics')
        return c.fetchone()

    def sum_sent(self):
        c = self._conn.cursor()
        c.execute('SELECT SUM(count_sent) FROM logistics')
        return c.fetchone()

    def get_max_vaccine_id(self):
        return self._max_vaccine_id

# the repository singleton
repo = _Repository()
atexit.register(repo._close)
