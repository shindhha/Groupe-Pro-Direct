namespace EBV_DOMPLUS_sandbox.Models
{
    public class LeadReply
    {
        public string dateCreation { get; set; }
        public string cle { get; set; }
        public string nom { get; set; }
        public string prenom { get; set; }
        public string email { get; set; }
        public string telephone { get; set; }
        public string callCenterProjectId { get; set; }
        public LeadError error { get; set; }
        public string dateRappel { get; set; }
        public string heureRappel { get; set; }
        public string produit { get; set; }
        public string message { get; set; }
    }
}