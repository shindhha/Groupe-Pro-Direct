import Db
import psycopg2
class ProdDb(Db):
    """
    Initialise la connection a la base de donner
    """
    def setUp(self):
        self.db = psycopg2.connect(
            "dbname=production user=pgtantely password=PasyVao2h2011  host= mcserver1.madcom.local")
        self.db.set_client_encoding('WIN1252')
        self.db.set_isolation_level(0)
        self.curseur_ = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor);

    """
    Construit une requête sql permettant de récupérer le nombre de ligne
    existante pour un champ donner dans une table donner avec ou non certains critères
    :param critere 
    :param table Table cibler dans la base de donné
    :param champ champ selectionner dans la table
    """

    def dcount(self, champ, table, critere=""):
        ssql = ""
        if critere == "":
            ssql = "select count(" + champ + ") as theretour from " + table
        else:
            ssql = "select count(" + champ + ") as theretour from " + table + " where " + critere
        self.curseur_.execute(ssql)
        tbret = self.curseur_.fetchall()
        ret = tbret[0]['theretour']
        return ret

    def dmax(self, champ, table, critere=""):
        ssql = ""
        if critere == "":
            ssql = "select max(" + champ + ") as theretour from " + table
        else:
            ssql = "select max(" + champ + ") as theretour from " + table + " where " + critere

        self.curseur_.execute(ssql)
        tbret = self.curseur_.fetchall()
        ret = ""
        if len(tbret) > 0:
            if tbret[0]['theretour'] == None:
                ret = ""
            else:
                ret = tbret[0]['theretour']
        return ret

    def dmin(self, champ, table, critere=""):
        ssql = ""
        if critere == "":
            ssql = "select min(" + champ + ") as theretour from " + table
        else:
            ssql = "select min(" + champ + ") as theretour from " + table + " where " + critere

        self.curseur_.execute(ssql)
        tbret = self.curseur_.fetchall()
        ret = ""
        if len(tbret) > 0:
            if tbret[0]['theretour'] == None:
                ret = ""
            else:
                ret = tbret[0]['theretour']
        return ret

    def dlookup(self, champ, table, critere=""):
        ssql = ""
        if critere == "":
            ssql = "select " + champ + " as theretour from " + table
        else:
            ssql = "select " + champ + " as theretour from " + table + " where " + critere

        self.curseur_.execute(ssql)
        tbret = self.curseur_.fetchall()
        ret = ""
        if len(tbret) > 0:
            ret = tbret[0]['theretour']
        return ret

    def getHours(self):
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur_.execute(ssql)
        tdate = self.curseur_.fetchone()
        ret = str(tdate[1])
        return ret

    def getDateJMA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur_.execute(ssql)
        tdate = self.curseur_.fetchone()
        res = str(tdate[0])
        tb = res.split(ssep)
        ret = str(tb[2]) + ssep + str(tb[1]) + ssep + str(tb[0])
        return ret

    def getDateAMJ(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur_.execute(ssql)
        tdate = self.curseur_.fetchone()
        res = str(tdate[0])
        tb = res.split(ssep)

        ret = str(tb[0]) + ssep + str(tb[1]) + ssep + str(tb[2])
        return ret

    def getDateMJA(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        ssql = "select current_date -1 as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur_.execute(ssql)
        tdate = self.curseur_.fetchone()
        res = str(tdate[0])
        tb = res.split(ssep)

        ret = str(int(tb[1])) + "/" + str(int(tb[2])) + "/" + str(tb[0])
        return ret

    def getDateLetter(self):
        ret = ""
        pos = 0
        ssep = "-"
        tb = []
        tmois = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ssql = "select current_date as date, substr(localtime::varchar,1,8)::time as time"
        self.curseur_.execute(ssql)
        tdate = self.curseur_.fetchone()
        res = str(tdate[0])
        tb = res.split(ssep)

        ret = str(tb[1]) + ssep + str(tb[2]) + ssep + str(tb[0])

        imois = int(tb[1])
        ijour = int(tb[2])

        if ijour < 10:
            ret = tmois[imois] + "  " + str(ijour)
        else:
            ret = tmois[imois] + " " + str(ijour)
        return ret

    def requete_select_mssql(self, mssql):
        self.req_select = mssql
        self.curseur_mssql.execute(self.req_select)

        return self.curseur_mssql.fetchall()