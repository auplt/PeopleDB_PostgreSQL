from dbtable import *


class DocsTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "docs"

    def columns(self):
        return {"id": ["SERIAL"],
                "person_id": ["integer", f"REFERENCES {self.dbconn.prefix}people(id)"],
                "type": ["varchar(32)", "NOT NULL"],
                "serial": ["varchar(32)", "NOT NULL"],
                "number": ["varchar(32)", "NOT NULL"],
                "date": ["date", "NOT NULL"]}

    def primary_key(self):
        return ['id']

    def all_by_person_id(self, pid):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE person_id =%(id)s"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"id": str(pid)})
        return cur.fetchall()

    def check_docs(self, pid, cd):
        cur = self.dbconn.conn.cursor()
        cur.execute(f'SELECT id FROM {self.table_name()} WHERE person_id = %(id)s', {'id': int(pid)})
        result = cur.fetchall()
        for i in result:
            if str(cd) == str(i[0]):
                return True
        return False

    def delete_docs_by_person(self, pid):
        cur = self.dbconn.conn.cursor()
        cur.execute(f'DELETE FROM {self.table_name()} WHERE person_id=%(id)s', {'id': int(pid)})
        self.dbconn.conn.commit()
        return

    def delete_docs(self, cd):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE id=" + self.primary_key()[0]
        sql += " AND id=%(tell)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"tell": str(cd)})
        self.dbconn.conn.commit()
        return

    def find_by_id(self, num):
        cur = self.dbconn.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name()} WHERE id=%(id)s", {'id': int(num)})
        return cur.fetchone()

    def find_by_position(self, num, pid):
        sql = "SELECT * FROM " + self.table_name() + " WHERE person_id=%(pid)s "
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())  # join string split by ', ', '[aa, bb, ss] ex.: aa, bb, ss
        sql += " LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1, "pid": pid})
        return cur.fetchone()

    def update_docs(self, pid, vals):
        vals = tuple(vals)
        cur = self.dbconn.conn.cursor()
        sql = "UPDATE " + self.table_name() + " SET type=%(type)s, serial=%(serial)s, number=%(number)s, date=%(date)s WHERE id=%(id)s"
        cur.execute(sql, {'type': str(vals[0]), 'serial': str(vals[1]), 'number': str(vals[2]), 'date': str(vals[3]),
                          'id': int(pid)})
        self.dbconn.conn.commit()
        return
