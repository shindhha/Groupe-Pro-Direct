using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace HS_MIDDLEWARE_LP.Models
{
    public class LeadsReply
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
        public string callCenterProjectId { get; set; }
        public LeadsError error { get; set; }
    }
}