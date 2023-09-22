import Db
import pymssql
class RecordDbNow(Db):
    def setUp(self):
        self.rec1 = pymssql.connect(host='5.196.127.163', user='read_write', password='0wY!3M8cQ#Kw',
                                    database='HN_Ondata', as_dict=True, timeout=0, login_timeout=600, charset="cp1252",
                                    port=1433)
        self.rec1.autocommit(False)
        self.curseur1 = self.rec1.cursor()
