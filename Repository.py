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
        CREATE TABLE logistics (
            id              INT     PRIMARY KEY, 
            name            STRING    NOT NULL,
            count_sent      INT     NOT NULL,
            count_received  INT     NOT NULL
        );
        
        CREATE TABLE suppliers (
            id          INT     PRIMARY KEY,
            name        STRING    NOT NULL,
            logistic    INT     NOT NULL,
            FOREIGN KEY (logistic)  REFERENCES logistics(id)
        );
        
        CREATE TABLE clinics (
            id          INT     NOT NULL,
            location    STRING    NOT NULL,
            demand      INT     NOT NULL,
            logistic    INT,
            FOREIGN KEY (logistic)  REFERENCES logistics(id)
        );
        
        CREATE TABLE vaccines (
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

    def find_supplier(self, name):
        return self._suppliers.find(name=name)

# the repository singleton
repo = _Repository()
atexit.register(repo._close)
