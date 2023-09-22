using System.Collections.Generic;


namespace HS_MIDDLEWARE_LP.Models
{
    public class Code
    {
        public string email { get; set; }

        public List<object[]> getCode()
        {
            List<object[]> data = new List<object[]>();

            this.email = Leads.EncryptString(this.email);

            data.Add(new object[] { this.email });

            return data;
        }
    }
}