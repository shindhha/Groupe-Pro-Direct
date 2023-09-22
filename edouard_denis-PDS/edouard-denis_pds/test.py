class Table():
    def __init__(self) -> None:
        self.query = ""
        self.select_part = ""
        self.where_part = ""
        self.from_part = ""

    def select(self,list_column):
        for column in list_column:
            if (self.select_part == ""):
                self.select_part += column
            else:
                self.select_part += ", " + column
        return self

    def where(self,column,value,operator=""):
        if (operator == ""):
            operator = " = "
        else: 
            tmp = value
            value = operator
            operator = tmp
        
        if (self.where_part == ""):
            self.where_part = column + " " + operator + " " + value
        else :
            self.where_part = " AND " + column + " " + operator + " " + value 
        return self
        
    def From(self,tables): 
        for table in tables:
            if (self.from_part == ""):
                self.from_part += table
            else:
                self.from_part += ", " + table
        return self
    
    def into(self,table):
        self.from_part = table
    
    def get(self) :
        return "SELECT " + self.select_part + " FROM " + self.from_part + " WHERE " + self.where_part

    def insert(self,datas):
        columns = "("
        values = "("
        for cle in datas.keys():
            columns += cle
            values += datas[cle]
        columns += ")"
        values += ")"
        return "INSERT INTO " + self.from_part + " " + columns +  " VALUES " + values
    


table = Table()
columns = ['indice','indice_debut','LastAgent','CallLocalTime','lib_status','ANI','tel_mobile',
          'tel_fixe','tel_professionnel','date_rdv','heure_rdv','type_rdv','nom_client','prenom_client',
          'nom_commercial','prenom_commercial','id_commercial']

query = table.select(columns).From(["utilisateur"]).where("Age","<","12").get()

insert_query = table.From(["utilisateur"]).insert({"Nom":"Medard"})

print(insert_query)