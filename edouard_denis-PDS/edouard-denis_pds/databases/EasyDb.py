import pymssql
import Db
class EasyDb(Db) :
    def setUp(self):
        self.db0 = pymssql.connect(host='5.196.127.163', user='read_write', password='0wY!3M8cQ#Kw',
                                   database='PROD_CAMBIUM', timeout=0, login_timeout=600, as_dict=True,
                                   charset="cp1252", port=1433)
        self.db0.autocommit(False)
        self.curseur0 = self.db0.cursor()