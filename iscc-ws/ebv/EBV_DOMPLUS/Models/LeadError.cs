using System;
using System.Linq;
using System.Net.Mail;
using System.Text.RegularExpressions;

namespace EBV_DOMPLUS.Models
{
    public class LeadError
    {
        private object v;
        public string errCode { get; set; }
        public string errMessage { get; set; }

        public LeadError(Lead DataInject)
        {
            checkIntegrity(DataInject);
        }

        public LeadError(object v)
        {
            this.v = v;
        }

        private LeadError checkIntegrity(Lead DataInject)
        {
            try
            {
                if (string.IsNullOrEmpty(DataInject.nom))
                {
                    errCode = "51";
                    errMessage = "Le champ 'nom' doit être renseigné.";
                    return this;
                }

                if (string.IsNullOrEmpty(DataInject.email))
                {
                    errCode = "52";
                    errMessage = "Le champ 'email' doit être renseigné.";
                    return this;
                }
                else
                {
                    try
                    {
                        var email = new MailAddress(DataInject.email.Trim());
                        if (DataInject.email.Trim() != email.Address)
                        {
                            errCode = "521";
                            errMessage = "Le champ 'email' doit être une adresse email valide. La valeur envoyée est '" + DataInject.email.Trim() + "'.";
                            return this;
                        }
                    }
                    catch (Exception e)
                    {
                        errCode = "522";
                        errMessage = e.Message + " La valeur envoyée est '" + DataInject.email.Trim() + "'.";
                        return this;
                    }
                }

                if (string.IsNullOrEmpty(DataInject.telephone))
                {
                    errCode = "53";
                    errMessage = "Le champ 'telephone' doit être renseigné.";
                    return this;
                }
                else
                {
                    string pattern = @"^\d{10}$";
                    Regex regex = new Regex(pattern);
                    Match match = regex.Match(DataInject.telephone.Trim());
                    if (!match.Success)
                    {
                        errCode = "531";
                        errMessage = "Le champ 'telephone' doit être un numéro de téléphone valide, 10 chiffres sans espace, ni point, ni tiret. La valeur envoyée est '" + DataInject.telephone.Trim() + "'.";
                        return this;
                    }
                }

                if (DataInject.source.Trim().ToLower() == "formulaire")
                {
                    if (string.IsNullOrEmpty(DataInject.dateRappel.Trim()))
                    {
                        errCode = "54";
                        errMessage = "Le champ 'dateRappel' doit être renseigné.";
                        return this;
                    }
                    else
                    {
                        string pattern = @"(\d{2}\/){2}\d{4}";
                        Regex regex = new Regex(pattern);
                        Match match = regex.Match(DataInject.dateRappel);
                        if (!match.Success)
                        {
                            errCode = "541";
                            errMessage = "Le champ 'dateRappel' doit être du format JJ/MM/AAAA. La valeur envoyée est '" + DataInject.dateRappel + "'.";
                            return this;
                        }
                        else
                        {
                            DateTime oDate = Convert.ToDateTime(DataInject.dateRappel);
                            if (oDate.DayOfWeek == DayOfWeek.Saturday || oDate.DayOfWeek == DayOfWeek.Sunday)
                            {
                                errCode = "542";
                                errMessage = "Le champ 'dateRappel' doit être une date de jour ouvré et non weekend. La date de Rappel choisie est un '" + oDate.DayOfWeek.ToString() + "'.";
                                return this;
                            }
                            else
                            {
                                if (Int32.Parse(oDate.ToString("yyyyMMdd")) < Int32.Parse(DateTime.Now.ToString("yyyyMMdd")))
                                {
                                    errCode = "543";
                                    errMessage = "Le champ 'dateRappel' doit être une date supérieure ou égale à aujourd'hui. La date de Rappel choisie est '" + oDate.ToString("dd/MM/yyyy") + "' alors qu'aujourd'hui est '" + DateTime.Now.ToString("dd/MM/yyyy") + "'.";
                                    return this;
                                }
                            }
                        }
                    }

                    if (string.IsNullOrEmpty(DataInject.heureRappel.Trim()))
                    {
                        errCode = "55";
                        errMessage = "Le champ 'heureRappel' doit être renseigné.";
                        return this;
                    }
                    else
                    {
                        string pattern = @"(09|1[0-8]):(0|3)0";
                        Regex regex = new Regex(pattern);
                        Match match = regex.Match(DataInject.heureRappel);
                        if (!match.Success)
                        {
                            errCode = "551";
                            errMessage = "Le champ 'heureRappel' doit être du format HH:MM et dont l'heure doit être comprise entre 9 et 18 et les minutes soit 00 ou 30. La valeur envoyée est '" + DataInject.heureRappel + "'.";
                            return this;
                        }
                    }

                    if (string.IsNullOrEmpty(DataInject.produit.Trim()))
                    {
                        errCode = "56";
                        errMessage = "Le champ 'produit' doit être renseigné.";
                        return this;
                    }
                    else
                    {
                        string[] produitsAttendus = { "Solution Liberté Connectée", "Solution Liberté Standard", "Solution Liberté Illimité", "Solution Sérénité Solo", "Solution Sérénité Duo", "Solution Intimité", "Je ne sais pas encore" };
                        if (produitsAttendus.Contains(DataInject.produit) == false)
                        {
                            errCode = "561";
                            errMessage = "La valeur du champ produit doit être parmi les suivants : '" + string.Join("', '", produitsAttendus) + "'. La valeur entrée est '" + DataInject.produit + "'.";
                            return this;
                        }
                    }
                }
                else
                {
                    if (string.IsNullOrEmpty(DataInject.message.Trim()))
                    {
                        errCode = "58";
                        errMessage = "Le champ 'message' doit être renseigné.";
                        return this;
                    }
                }

                if (string.IsNullOrEmpty(DataInject.optin.Trim()))
                {
                    errCode = "57";
                    errMessage = "Le champ 'optin' doit être renseigné.";
                    return this;
                }
                else
                {
                    string[] optinAttendus = { "0", "1" };
                    if (optinAttendus.Contains(DataInject.optin) == false)
                    {
                        errCode = "571";
                        errMessage = "La valeur du champ optin doit être parmi les suivants : '" + string.Join("', '", optinAttendus) + "'. La valeur entrée est '" + DataInject.optin + "'.";
                        return this;
                    }
                }

                return this;
            }
            catch (NullReferenceException e)
            {
                errCode = "59";
                errMessage = e.Message;
                return this;
            }
            catch (Exception e)
            {
                errCode = "60";
                errMessage = e.Message;
                return this;
            }
        }
    }
}