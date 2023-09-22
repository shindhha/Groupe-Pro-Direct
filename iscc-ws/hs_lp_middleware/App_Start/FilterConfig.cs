using System.Web;
using System.Web.Mvc;

namespace HS_MIDDLEWARE_LP
{
    public class FilterConfig
    {
        public static void RegisterGlobalFilters(GlobalFilterCollection filters)
        {
            filters.Add(new HandleErrorAttribute());
        }
    }
}
