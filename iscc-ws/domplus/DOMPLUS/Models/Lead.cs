using Newtonsoft.Json;
using System;
using System.Collections.Generic;

namespace DOMPLUS.Models
{
    public class Lead
    {
        public int gender { get; set; }
        public string postcode { get; set; }
        public string city { get; set; }
        public int dateDispo { get; set; }
        public int heureDispo { get; set; }
        public string email { get; set; }
        public int mode { get; set; }
        public string nom { get; set; }
        public string prenom { get; set; }
        public int produit { get; set; }
        public Features[] questionReponse { get; set; }
        public string tel1 { get; set; }
        public string tel2 { get; set; }
        protected string daty { get; set; }
        public string uniqId { get; set; }

        public Lead()
        {
            DateTime date = DateTime.Now;
            this.daty = date.ToString("yyyy-MM-dd HH:mm:ss");
        }

        public string[] getClientFields()
        {
            string[] clientFields = new string[] { "CIVILITE", "CODE_POSTAL", "COMMUNE", "DATY", "DISPO_DATE", "DISPO_HEURE", "MAIL", "MODE", "NOM", "PRENOM", "PRODUIT", "QUESTION_REPONSE", "TEL1", "TEL2", "SOURCE" };
            return clientFields;
        }

        public string[] getClientPhone()
        {
            string[] clientPhone = new string[] { "TEL1", "TEL2" };
            return clientPhone;
        }

        public List<object[]> getDataDomplus()
        {
            List<object[]> data = new List<object[]>();

            string questionReponses = JsonConvert.SerializeObject(this.questionReponse);
            string source = "SILVER LEADS";

            Console.WriteLine("DOMPLUS LOG " + this.uniqId);

            data.Add(new object[] { this.getCivilite(), this.postcode, this.city, this.getDaty(), this.getDateDispo(), this.getHeureDispo(), this.email, this.mode, this.nom, this.prenom, this.getProduit(), questionReponses, this.tel1, this.tel2, source });

            return data;
        }

        private string getDateDispo()
        {
            string date_dispo = "";

            switch (this.dateDispo)
            {
                case 0:
                    date_dispo = "Indifférent";
                    break;
                case 1:
                    date_dispo = "Lundi";
                    break;
                case 2:
                    date_dispo = "Mardi";
                    break;
                case 3:
                    date_dispo = "Mercredi";
                    break;
                case 4:
                    date_dispo = "Jeudi";
                    break;
                case 5:
                    date_dispo = "Vendredi";
                    break;
                case 6:
                    date_dispo = "Samedi";
                    break;
            }

            return date_dispo;
        }

        private string getHeureDispo()
        {
            string heure_dispo = "";

            switch (this.heureDispo)
            {
                case 0:
                    heure_dispo = "Indifférent";
                    break;
                case 1:
                    heure_dispo = "Matin";
                    break;
                case 2:
                    heure_dispo = "Midi";
                    break;
                case 3:
                    heure_dispo = "Après-midi";
                    break;
                case 4:
                    heure_dispo = "Soir";
                    break;
            }

            return heure_dispo;
        }

        public string getCivilite()
        {
            string civilite = "";

            switch (this.gender)
            {
                case 1:
                    civilite = "Inconnu";
                    break;
                case 2:
                    civilite = "Monsieur";
                    break;
                case 3:
                    civilite = "Madame";
                    break;
            }

            return civilite;
        }

        public string getProduit()
        {
            string _produit = "";

            switch (this.produit)
            {
                case 2:
                    _produit = "Douche sénior";
                    break;
                case 3:
                    _produit = "Monte escalier";
                    break;
                case 5:
                    _produit = "Téléassistance";
                    break;
            }

            return _produit;
        }

        public string getDaty()
        {
            return this.daty;
        }
    }
}