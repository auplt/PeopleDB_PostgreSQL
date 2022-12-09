import psycopg2


class DbConnection:
    def __init__(self, config):
        self.path = config.dbfilepath
        self.prefix = config.dbtableprefix
        self.conn = psycopg2.connect(dbname=config.database, user=config.user, password=config.password,
                                     host=config.host)

    def __del__(self):
        if self.conn:
            self.conn.close()

    def test(self):
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE test(test integer)")
        cur.execute("INSERT INTO test(test) VALUES(1)")
        self.conn.commit()
        cur.execute("SELECT * FROM test")
        result = cur.fetchall()
        cur.execute("DROP TABLE test")
        self.conn.commit()
        return (result[0][0] == 1)
