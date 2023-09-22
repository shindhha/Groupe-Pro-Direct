class Db():
    def __init__(self, sql=""):
        self.rec = None
        self.curseur = None
        self.setUp()
        self.request = sql

    def setRequest(self, ssql):
        self.request = ssql

    def setNothing(self):
        self.rec.close()
        self.rec = None
        self.curseur = None

    """
        Execute une requête sql donner en argument
    """
    def runSql(self, ssql):
        self.request = ssql
        self.docomand()


    """
        Execute la requête sql en argument et retourne la première ligne retourné
        :param ssql requête sql
    """

    def openrecordsetOne(self, ssql):
        self.request = ssql
        self.curseur.execute(self.request)
        return self.curseur.fetchone()
    """
        Execute la requête sql donner en argument et retourne l'entièreté des lignes
    """
    def openrecordset(self, ssql):
        self.request = ssql
        self.curseur.execute(self.request)
        return self.curseur.fetchall()
    """
        Execute la dernière requête sql stocker
    """
    def execute(self):
        self.curseur.execute(self.request)

    """
        Execute la dernière requête sql stocker
    """
    def docomand(self):
        self.curseur.execute(self.request)

















