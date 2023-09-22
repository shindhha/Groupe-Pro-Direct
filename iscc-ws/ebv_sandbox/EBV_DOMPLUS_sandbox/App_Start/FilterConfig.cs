using System.Web;
using System.Web.Mvc;

namespace EBV_DOMPLUS_sandbox
{
    public class FilterConfig
    {
        public static void RegisterGlobalFilters(GlobalFilterCollection filters)
        {
            filters.Add(new HandleErrorAttribute());
        }
    }
}
