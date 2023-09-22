using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;

namespace EBV_DOMPLUS_sandbox.Models
{
    public class Lead
    {
        public string dateCreation { get; set; }
        public string cle { get; set; }
        public string nom { get; set; }
        public string prenom { get; set; }
        public string email { get; set; }
        public string telephone { get; set; }
        public string dateRappel { get; set; }
        public string heureRappel { get; set; }
        public string produit { get; set; }
        public string optin { get; set; }
        public string source { get; set; }
        public string message { get; set; }

        public string[] getClientFields()
        {
            string[] clientFields;
            string source = this.source;
            if (string.IsNullOrEmpty(this.source))
            {
                source = "FORMULAIRE";
            }
            switch (source.Trim().ToLower())
            {
                case "formulaire":
                    clientFields = new string[] { "dateCreation", "cle", "nom", "prenom", "email", "telephone", "dateRappel", "heureRappel", "produit", "optin", "source" };
                    break;
                default:
                    clientFields = new string[] { "dateCreation", "cle", "nom", "prenom", "email", "telephone", "message", "optin", "source" };
                    break;
            }
            return clientFields;
        }

        public string[] getClientPhone()
        {
            string[] clientPhone = new string[] { "telephone" };
            return clientPhone;
        }

        public List<object[]> getDataEBV()
        {
            List<object[]> data = new List<object[]>();
            string source = this.source.Trim().ToUpper();
            if (string.IsNullOrEmpty(this.source))
            {
                source = "FORMULAIRE";
            }
            this.dateCreation = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            this.cle = DefineCle(this);

            switch (source.Trim().ToLower())
            {
                case "formulaire":
                    data.Add(new object[] { this.dateCreation, this.cle, this.nom, this.prenom, this.email, this.telephone, this.dateRappel, this.heureRappel, this.produit, this.optin, this.source });
                    break;
                default:
                    data.Add(new object[] { this.dateCreation, this.cle, this.nom, this.prenom, this.email, this.telephone, this.message, this.optin, this.source });
                    break;
            }

            return data;
        }

        public string DefineCle(Lead DataLead)
        {
            string cle = DataLead.telephone;
            cle += "#" + DataLead.dateRappel;
            cle += "#" + DataLead.heureRappel;

            if (this.source.Trim().ToLower() == "email")
            {
                cle = DataLead.telephone;
                cle += "#" + DataLead.email;
                cle += "#" + DataLead.nom;
            }

            return EncryptString(cle);
        }

        private string EncryptString(string cle)
        {
            string secret = "babafade277a7900d205757e84ea657b18bd4e48";
            Encoding ascii = Encoding.ASCII;
            HMACSHA256 hmac = new HMACSHA256(ascii.GetBytes(secret));

            return Convert.ToBase64String(hmac.ComputeHash(ascii.GetBytes(cle)));
        }
    }
}