import Db
import pymssql
class RecordDb(Db):
    def setUp(self):
        self.rec = pymssql.connect(host='5.196.127.163', user='read_write', password='0wY!3M8cQ#Kw',
                                   database='VIVETIC_BACKUP', as_dict=True, timeout=0, login_timeout=600,
                                   charset="cp1252", port=1433)
        self.rec.autocommit(False)
        self.curseur = self.rec.cursor()