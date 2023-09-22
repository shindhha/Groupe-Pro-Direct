using System;
using System.Net.Mail;
using System.Linq;

namespace HS_MIDDLEWARE_LP.Models
{
    public class LeadsError
    {
        public int errCode { get; set; }
        public string errMessage { get; set; }

        public LeadsError(Leads DataInject)
        {
            this.checkIntegrity(DataInject);
        }

        private LeadsError checkIntegrity(Leads DataInject)
        {
            try
            {
                if (string.IsNullOrEmpty(DataInject.civilite.Trim()))
                {
                    errCode = 51;
                    errMessage = "Le champ 'civilite' doit être renseigné.";
                    return this;
                }
                else
                {
                    string[] civilitesAttendus = { "Madame", "Monsieur" };
                    if (civilitesAttendus.Contains(DataInject.civilite) == false)
                    {
                        errCode = 511;
                        errMessage = "La valeur du champ civilite doit être parmi les suivants : '" + string.Join("', '", civilitesAttendus) + "'. La valeur entrée est '" + DataInject.civilite + "'.";
                        return this;
                    }
                }

                if (string.IsNullOrEmpty(DataInject.email.Trim()))
                {
                    this.errCode = 52;
                    this.errMessage = "Le champ email doit être renseigné.";
                    return this;
                }
                else
                {
                    try
                    {
                        var eml = new MailAddress(DataInject.email.Trim());
                        if (eml.Address != DataInject.email.Trim())
                        {
                            this.errCode = 521;
                            this.errMessage = "Le champ 'email' doit être une adresse email valide. La valeur envoyée est '" + DataInject.email.Trim() + "'.";
                            return this;
                        }
                    }
                    catch (Exception e)
                    {
                        this.errCode = 522;
                        this.errMessage = e.Message;
                        return this;
                    }
                }

                if (!string.IsNullOrEmpty(DataInject.commentConnu.Trim()))
                {
                    string[] commentCommusAttendus = { "flyers", "seloger", "leboncoin", "bienici", "immoneuf", "superimmo", "paruvendu", "acheterlouer", "citizia", "other_websites", "agence_lp", "immoneuf_bdx", "immoneuf_tlse", "partenaires", "mairie", "emailing_marketing", "search_engines", "facebook", "instagram", "linkedin", "twitter", "youtube", "pinterest", "sms", "radio", "airport_tlse", "station_bdx", "panneaux_chantier", "presse", "panneaux_affichage", "bouche_oreille", "metro", "bus", "velib", "cinema", "television", "tv_replay", "ne_sait_pas" };
                    if (commentCommusAttendus.Contains(DataInject.commentConnu.ToLower()) == false)
                    {
                        errCode = 53;
                        errMessage = "La valeur du champ commentConnu doit être parmi les suivants : '" + string.Join("', '", commentCommusAttendus) + "'. La valeur entrée est '" + DataInject.commentConnu + "'.";
                        return this;
                    }
                }

                if (string.IsNullOrEmpty(DataInject.optin.Trim()))
                {
                    errCode = 54;
                    errMessage = "Le champ 'optin' doit être renseigné.";
                    return this;
                }
                else
                {
                    string[] optinsAttendus = { "Legitimate interest – prospect/lead", "Legitimate interest – existing customer", "Legitimate interest - other", "Performance of a contract", "Freely given consent from contact", "Not applicable" };
                    if (optinsAttendus.Contains(DataInject.optin) == false)
                    {
                        errCode = 541;
                        errMessage = "La valeur du champ optin doit être parmi les suivants : '" + string.Join("', '", optinsAttendus) + "'. La valeur entrée est '" + DataInject.optin + "'.";
                        return this;
                    }
                }

                return this;
            }
            catch (NullReferenceException e)
            {
                this.errCode = 59;
                this.errMessage = e.Message;
                return this;
            }
            catch (Exception e)
            {
                this.errCode = 60;
                this.errMessage = e.Message;
                return this;
            }
        }
    }
}