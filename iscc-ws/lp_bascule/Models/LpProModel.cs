using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Lpbascule.Models
{
    public class LpPromo
    {
        public string indice_origine { get; set; }
        public string adresse { get; set; }
        public string budget { get; set; }
        public string civilite { get; set; }
        public string cle { get; set; }
        public string codePostal { get; set; }
        public string codePostalRecherche1 { get; set; }
        public string codePostalRecherche2 { get; set; }
        public string codePostalRecherche3 { get; set; }
        public string commentConnu { get; set; }
        public string complementAdresse { get; set; }
        public string conversionRecente { get; set; }
        public string dateCreation { get; set; }
        public string email { get; set; }
        public string hubspotId { get; set; }
        public string informationSource1 { get; set; }
        public string message { get; set; }
        public string nom { get; set; }
        public string nombrePiece { get; set; }
        public string nomProgramme { get; set; }
        public string prenom { get; set; }
        public string telephone { get; set; }
        public string typeAchat { get; set; }
        public string typeBien { get; set; }
        public string ville { get; set; }
        public string villeRecherche1 { get; set; }
        public string villeRecherche2 { get; set; }
        public string villeRecherche3 { get; set; }
        public string optin { get; set; }
        public string daty { get; set; }
        public string Calltype { get; set; }
        public string flagmail_injoignable { get; set; }
        public string details_source_hors_ligne { get; set; }
        public string budget_VAL { get; set; }
        public string civilite_VAL { get; set; }
        public string commentConnu_VAL { get; set; }
        public string nombrePiece_VAL { get; set; }
        public string optin_VAL { get; set; }
        public string typeAchat_VAL { get; set; }
        public string typeBien_VAL { get; set; }
        public string CRITERE_R { get; set; }
        public string CRITERE_R_VAL { get; set; }
        public string VAL_R { get; set; }
        public string COMMENTAIRES { get; set; }
        public string date_deal_change { get; set; }
        public string proprietaireContact { get; set; }
        public string flag_mail_change { get; set; }
        public string flag_resultat_appel_change { get; set; }
        public string flag_proprietairecontact_change { get; set; }
        public string flag_deal_change { get; set; }
        public string flag_contact_change { get; set; }
        public string Flag_fin_appel_deal { get; set; }
        public string createdate_hubspot { get; set; }
        public string proprietaireContact_VAL { get; set; }
        public string ANI { get; set; }
        public string FLAG_INJECTION { get; set; }
        public string DATE_RDV { get; set; }
        public string HEURE_RDV { get; set; }
        public string TYPE_RDV { get; set; }
        public string COMMERCIAL { get; set; }
        public string NOM_COMMERCIAL { get; set; }

        public string[] getClientFields()
        {
            string[] clientFields = new string[] { "indice_origine", "adresse", "budget", "civilite", "cle", "codePostal", "codePostalRecherche1", "codePostalRecherche2", "codePostalRecherche3", "commentConnu", "complementAdresse", "conversionRecente", "dateCreation", "email", "hubspotId", "informationSource1", "message", "nom", "nombrePiece", "nomProgramme", "prenom", "telephone", "typeAchat", "typeBien", "ville", "villeRecherche1", "villeRecherche2", "villeRecherche3", "optin", "daty", "Calltype", "flagmail_injoignable", "details_source_hors_ligne", "budget_VAL", "civilite_VAL", "commentConnu_VAL", "nombrePiece_VAL", "optin_VAL", "typeAchat_VAL", "typeBien_VAL", "CRITERE_R", "CRITERE_R_VAL", "VAL_R", "COMMENTAIRES", "date_deal_change", "proprietaireContact", "flag_mail_change", "flag_resultat_appel_change", "flag_proprietairecontact_change", "flag_deal_change", "flag_contact_change", "Flag_fin_appel_deal", "createdate_hubspot", "proprietaireContact_VAL", "ANI", "FLAG_INJECTION", "DATE_RDV", "HEURE_RDV", "TYPE_RDV", "COMMERCIAL" ,"NOM_COMMERCIAL" };

            return clientFields;
        }

        public string[] getClientPhone()
        {
            string[] phoneFields = new string[] { "telephone" };
            return phoneFields;
        }


        public List<object[]> getDataLpPromo()
        {
            DateTime dateTime = DateTime.UtcNow.Date;
            string daty = dateTime.ToString("yyyyddMM");
            List<object[]> data = new List<object[]>();
            data.Add(new object[] { this.indice_origine, this.adresse, this.budget, this.civilite, this.cle, this.codePostal, this.codePostalRecherche1, this.codePostalRecherche2, this.codePostalRecherche3, this.commentConnu, this.complementAdresse, this.conversionRecente, this.dateCreation, this.email, this.hubspotId, this.informationSource1, this.message, this.nom, this.nombrePiece, this.nomProgramme, this.prenom, this.telephone, this.typeAchat, this.typeBien, this.ville, this.villeRecherche1, this.villeRecherche2, this.villeRecherche3, this.optin, this.daty, this.Calltype, this.flagmail_injoignable, this.details_source_hors_ligne, this.budget_VAL, this.civilite_VAL, this.commentConnu_VAL, this.nombrePiece_VAL, this.optin_VAL, this.typeAchat_VAL, this.typeBien_VAL, this.CRITERE_R, this.CRITERE_R_VAL, this.VAL_R, this.COMMENTAIRES, this.date_deal_change, this.proprietaireContact, this.flag_mail_change, this.flag_resultat_appel_change, this.flag_proprietairecontact_change, this.flag_deal_change, this.flag_contact_change, this.Flag_fin_appel_deal, this.createdate_hubspot, this.proprietaireContact_VAL, this.ANI, this.FLAG_INJECTION, this.DATE_RDV, this.HEURE_RDV, this.TYPE_RDV, this.COMMERCIAL, this.NOM_COMMERCIAL });
            return data;
        }

    }
}
public class retour
{
    public string Error { get; set; }
    public string Message { get; set; }
}