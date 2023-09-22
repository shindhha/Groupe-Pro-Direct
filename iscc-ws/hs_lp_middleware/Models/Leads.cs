using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;

namespace HS_MIDDLEWARE_LP.Models
{
    public class Leads
    {
        public string dateCreation { get; set; }
        public string cle { get; set; }
        public string civilite { get; set; }
        public string email { get; set; }
        public string nom { get; set; }
        public string prenom { get; set; }
        public string telephone { get; set; }
        public string codePostal { get; set; }
        public string adresse { get; set; }
        public string complementAdresse { get; set; }
        public string ville { get; set; }
        public string commentConnu { get; set; }
        public string informationSource1 { get; set; }
        public string conversionRecente { get; set; }
        public string message { get; set; }
        public string hubspotId { get; set; }
        public string optin { get; set; }
        public string proprietaireContact { get; set; }

        public string[] getClientFileds()
        {
            string[] clientFields;

            clientFields = new string[] { "dateCreation", "cle", "civilite", "email", "nom", "prenom", "telephone", "codePostal", "adresse", "complementAdresse", "ville", "commentConnu", "informationSource1", "conversionRecente", "message", "hubspotId", "optin", "proprietaireContact_VAL" };

            return clientFields;
        }

        public string[] getClientPhone()
        {
            string[] clientPhone;

            clientPhone = new string[] { "telephone" };

            return clientPhone;
        }

        public List<object[]> getData()
        {
            List<object[]> data = new List<object[]>();

            this.dateCreation = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            this.cle = this.DefineCle(this);

            if (string.IsNullOrEmpty(this.civilite.Trim()))
            {
                this.civilite = "Monsieur";
            }
            else
            {
                this.civilite = System.Globalization.CultureInfo.CurrentCulture.TextInfo.ToTitleCase(this.civilite);
            }

            if (this.optin == null || string.IsNullOrEmpty(this.optin))
            {
                this.optin = "Not applicable";
            }

            if (string.IsNullOrEmpty(this.telephone.Trim()))
            {
                this.telephone = "9999999999";
            }

            data.Add(new object[] { this.dateCreation, this.cle, this.civilite, this.email, this.nom, this.prenom, this.telephone, this.codePostal, this.adresse, this.complementAdresse, this.ville, this.commentConnu, this.informationSource1, this.conversionRecente, this.message, this.hubspotId, this.optin, this.proprietaireContact });

            return data;
        }

        public string DefineCle(Leads DataLead)
        {
            string cle = DataLead.email;

            return EncryptString(cle);
        }

        public static string EncryptString(string cle)
        {
            string secret = "babafade277a7900d205757e84ea657b18bd4e48";
            Encoding ascii = Encoding.ASCII;
            HMACSHA256 hmac = new HMACSHA256(ascii.GetBytes(secret));

            return Convert.ToBase64String(hmac.ComputeHash(ascii.GetBytes(cle)));
        }
    }
}