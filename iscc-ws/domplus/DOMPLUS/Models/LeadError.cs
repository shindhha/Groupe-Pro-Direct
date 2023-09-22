using System;
using System.Linq;
using System.Net.Mail;
using System.Text.RegularExpressions;

namespace DOMPLUS.Models
{
    public class LeadError
    {
        public string errCode { get; set; }
        public string errMessage { get; set; }

        public LeadError(Lead DataInject)
        {
            checkIntegrity(DataInject);
        }

        private LeadError checkIntegrity(Lead DataInject)
        {
            if (string.IsNullOrEmpty(DataInject.nom))
            {
                errCode = "53";
                errMessage = "Le champ 'nom' doit être renseigné.";
                return this;
            }
            if (string.IsNullOrEmpty(DataInject.tel1) && string.IsNullOrEmpty(DataInject.tel2))
            {
                errCode = "57";
                errMessage = "Le champ 'tel1' ou 'tel2' doit être renseigné.";
                return this;
            }
            else
            {
                if (!string.IsNullOrEmpty(DataInject.tel1))
                {
                    string pattern = @"^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$";
                    Regex regex = new Regex(pattern);
                    Match match = regex.Match(DataInject.tel1.Trim());
                    if (!match.Success)
                    {
                        errCode = "571";
                        errMessage = "Le champ 'tel1' doit être un numéro de téléphone valide. La valeur envoyée est '" + DataInject.tel1.Trim() + "'.";
                        return this;
                    }
                }
                if (!string.IsNullOrEmpty(DataInject.tel2))
                {
                    string pattern = @"^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$";
                    Regex regex = new Regex(pattern);
                    Match match = regex.Match(DataInject.tel2.Trim());
                    if (!match.Success)
                    {
                        errCode = "571";
                        errMessage = "Le champ 'tel2' doit être un numéro de téléphone valide. La valeur envoyée est '" + DataInject.tel2.Trim() + "'.";
                        return this;
                    }
                }
            }
            if (string.IsNullOrEmpty(DataInject.email))
            {
            }
            else
            {
                try
                {
                    var email = new MailAddress(DataInject.email.Trim());
                    if (DataInject.email.Trim() != email.Address)
                    {
                        errCode = "581";
                        errMessage = "Le champ 'email' doit être une adresse email valide. La valeur envoyée est '" + DataInject.email.Trim() + "'.";
                        return this;
                    }
                }
                catch (Exception e)
                {
                    errCode = "582";
                    errMessage = e.Message + " La valeur envoyée est '" + DataInject.email.Trim() + "'.";
                    return this;
                }
            }
            if (!string.IsNullOrEmpty(DataInject.dateDispo.ToString()))
            {
                int[] dateDispoAttendu = { 0, 1, 2, 3, 4, 5, 6 };
                if (dateDispoAttendu.Contains(DataInject.dateDispo) == false)
                {
                    errCode = "59";
                    errMessage = "La valeur du champ dateDispo doit être parmi les suivants : 0, 1, 2, 3, 4, 5, 6. La valeur entrée est '" + DataInject.dateDispo + "'.";
                    return this;
                }
            }
            if (!string.IsNullOrEmpty(DataInject.heureDispo.ToString()))
            {
                int[] heureDispoAttendu = { 0, 1, 2, 3, 4 };
                if (heureDispoAttendu.Contains(DataInject.heureDispo) == false)
                {
                    errCode = "60";
                    errMessage = "La valeur du champ heureDispo doit être parmi les suivants : 0, 1, 2, 3, 4. La valeur entrée est '" + DataInject.heureDispo + "'.";
                    return this;
                }
            }
            if (!string.IsNullOrEmpty(DataInject.gender.ToString()))
            {
                int[] genreAttendu = { 0, 1, 2, 3, 4 };
                if (genreAttendu.Contains(DataInject.gender) == false)
                {
                    errCode = "61";
                    errMessage = "La valeur du champ gender doit être parmi les suivants : 0, 1, 2, 3. La valeur entrée est '" + DataInject.gender + "'.";
                    return this;
                }
            }
            if (!string.IsNullOrEmpty(DataInject.produit.ToString()))
            {
                int[] produitAttendu = { 2, 3, 5 };
                if (produitAttendu.Contains(DataInject.produit) == false)
                {
                    errCode = "61";
                    errMessage = "La valeur du champ produit doit être parmi les suivants : 2, 3, 5. La valeur entrée est '" + DataInject.produit + "'.";
                    return this;
                }
            }

            return this;
        }
    }
}