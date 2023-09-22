using System.Collections.Generic;

namespace DOMPLUS.Models
{
    public class LeadReply
    {
        public string daty { get; set; }
        public string nom { get; set; }
        public string prenom { get; set; }
        public string email { get; set; }
        public string tel { get; set; }
        public string produit { get; set; }
        public string uniqId { get; set; }
        public string callCenterProjectId { get; set; }
        public LeadError error { get; set; }
    }
}