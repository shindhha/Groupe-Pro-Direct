using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace EdouardDenis.Models
{
    public class EdouardDenis
    {
        public string code_postal { get; set; }
        public string adresse { get; set; }
        public string adresse2 { get; set; }
        public string ville { get; set; }
        public string email { get; set; }
        public string email2 { get; set; }
        public string prenom { get; set; }
        public string nom { get; set; }
        public string tel_mobile { get; set; }
        public string tel_fixe { get; set; }
        public string tel_professionnel { get; set; }
        public string salutation { get; set; }
        public string situation_logement { get; set; }
        public string objectif_achat { get; set; }
        public string date_acquisition { get; set; }
        public string code_programme { get; set; }
        public string projet_immo { get; set; }
        public string commentaire { get; set; }
        public string budget_max { get; set; }
        public string horaire_rappel { get; set; }
        public string utm_capaign { get; set; }
        public string canal { get; set; }
        public string utm_act { get; set; }
        public string utm_source { get; set; }
        public string utm_medium { get; set; }
        public string factoryprojectid { get; set; }
        public string imposition { get; set; }
        public string date_naissance { get; set; }
        public string profession { get; set; }
        public string nom_formulaire { get; set; }
        public string type_logement { get; set; }
        public string surface_logement { get; set; }
        public string taille_logement { get; set; }
        public string budget_fourchette { get; set; }
        public string code_lot { get; set; }
        public string dept_rech { get; set; }
        public string ville_rech { get; set; }
        public string primo_accedant { get; set; }
        public string rgpdin { get; set; }
        public string rgpdout { get; set; }
        public string type_bienED { get; set; }
        public string nature_bien { get; set; }
        public string indice_debut { get; set; }
        public string date_rdv { get; set; }
        public string heure_rdv { get; set; }
        public string id_commercial { get; set; }
        public string id_lieu_rdv { get; set; }
        public string bascule { get; set; }
        public string revente { get; set; }
        public string is_sms { get; set; }
        public string flag_mail { get; set; }
        public string drapp { get; set; }
        public string programme_prodirect { get; set; }


        public string raison_trna { get; set; }

        public string camp_debut { get; set; }

        public string first_sale { get; set; }
        public string avoir_projet { get; set; }
        public string budgetm { get; set; }
        public string etage { get; set; }
        public string m2 { get; set; }
        public string principale_investissement { get; set; }
        public string secteur_geo { get; set; }
        public string destination_achat { get; set; }
        public string budget { get; set; }
        public string typo_formulaire { get; set; }

        public string[] getClientFields()
        {
            string[] clientFields = new string[] { "code_postal", "adresse", "adresse2", "ville", "email", "email2", "prenom", "nom", "tel_mobile", "tel_fixe", "tel_professionnel", "salutation", "situation_logement", "objectif_achat", "date_acquisition", "code_programme", "projet_immo", "commentaire", "budget_max", "horaire_rappel", "utm_capaign", "canal", "utm_act", "utm_source", "utm_medium", "factoryprojectid", "imposition", "date_naissance", "profession", "nom_formulaire", "type_logement", "surface_logement", "taille_logement", "budget_fourchette", "code_lot", "dept_rech", "ville_rech", "primo_accedant", "rgpdin", "rgpdout", "type_bienED", "nature_bien", "indice_debut", "date_rdv", "heure_rdv", "id_commercial", "id_lieu_rdv", "bascule", "revente", "is_sms", "flag_mail", "drapp", "programme_prodirect", "raison_trna", "camp_debut", "first_sale", "avoir_projet", "budgetm", "etage", "m2", "principale_investissement", "secteur_geo","destination_achat","budget","typo_formulaire" };
            return clientFields;
        }


        public string[] getClientPhone()
        {
            string[] phoneFields = new string[] { "tel_mobile", "tel_fixe", "tel_professionnel" };
            return phoneFields;
        }
        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>


        public List<object[]> getDataEdouardDenis()
        {
            DateTime dateTime = DateTime.UtcNow.Date;
            string daty = dateTime.ToString("yyyyddMM");
            List<object[]> data = new List<object[]>();
            data.Add(new object[] { this.code_postal, this.adresse, this.adresse2, this.ville, this.email, this.email2, this.prenom, this.nom, this.tel_mobile, this.tel_fixe, this.tel_professionnel, this.salutation, this.situation_logement, this.objectif_achat, this.date_acquisition, this.code_programme, this.projet_immo, this.commentaire, this.budget_max, this.horaire_rappel, this.utm_capaign, this.canal, this.utm_act, this.utm_source, this.utm_medium, this.factoryprojectid, this.imposition, this.date_naissance, this.profession, this.nom_formulaire, this.type_logement, this.surface_logement, this.taille_logement, this.budget_fourchette, this.code_lot, this.dept_rech, this.ville_rech, this.primo_accedant, this.rgpdin, this.rgpdout, this.type_bienED, this.nature_bien, this.indice_debut, this.date_rdv, this.heure_rdv, this.id_commercial, this.id_lieu_rdv, this.bascule, this.revente, this.is_sms, this.flag_mail, this.drapp, this.programme_prodirect, this.raison_trna, this.camp_debut, first_sale, this.avoir_projet, this.budgetm, this.etage, this.m2, this.principale_investissement, this.secteur_geo, this.destination_achat,this.budget,this.typo_formulaire });
            return data;
        }


    }
}