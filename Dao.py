import sqlite3

import dbtools
from Dto import Logistic


class Dao:
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type
        # dto_type is a class, its __name__ field contains a string of the class name
        self._table_name = dto_type.__name__.lower() + 's'

    def insert(self, dto_instance):
        with self._conn:
            ins_dict = vars(dto_instance)
            column_names = ','.join(ins_dict.keys())
            params = list(ins_dict.values())
            qmarks = ','.join(['?'] * len(ins_dict))
            stmt = 'INSERT OR IGNORE INTO {} ({}) VALUES ({})'.format(self._table_name, column_names, qmarks)
            self._conn.execute(stmt, params)

    def find_all(self):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {}'.format(self._table_name))
        return dbtools.orm(c, self._dto_type)

    def find(self, **keyvals):
        column_names = keyvals.keys()
        params = list(keyvals.values())
        stmt = 'SELECT * FROM {} WHERE {}'.format(self._table_name,
                                                  ' AND '.join([col + '=?' for col in column_names]))
        c = self._conn.cursor()
        c.execute(stmt, params)
        # print(c.fetchall())
        return dbtools.orm(c, self._dto_type)

    def delete(self, **keyvals):
        with self._conn:
            column_names = keyvals.keys()
            params = keyvals.values()
            stmt = 'DELETE FROM {} WHERE {}'.format(self._table_name,
                                                    ' AND '.join([col + '=?' for col in column_names]))
            c = self._conn.cursor()
            c.execute(stmt, params)

    def update(self, set_values, cond):
        with self._conn:
            # what field to update, example: count_set = 50
            set_column_names = list(set_values.keys())
            set_params = list(set_values.values())
            # which rows to update, example: WHERE id=3
            cond_column_names = list(cond.keys())
            cond_params = list(cond.values())
            params = set_params + cond_params
            stmt = 'UPDATE {} SET {} WHERE {}'.format(self._table_name,
                                                      ', '.join([set + '=?' for set in set_column_names]),
                                                      ' AND '.join([cond + '=?' for cond in cond_column_names]))
            self._conn.execute(stmt, params)
