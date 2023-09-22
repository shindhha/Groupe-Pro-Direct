using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace EBV_DOMPLUS.MessageHandlers
{
    public class ApiKeyHandler : DelegatingHandler
    {
        //ApiKey Sandbox
        //private const string ApiKey = "7f5831d6-8cf8-4008-b238-9fe81d761e7e";
        //ApiKey Prod
        private const string ApiKey = "d47e96fe-0367-4ec3-b842-43fcc2beddf6";

        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            bool isValidAPIKey = false;
            IEnumerable<string> lsHeaders;

            var checkApiKeyExists = request.Headers.TryGetValues("apikey", out lsHeaders);

            if (checkApiKeyExists)
            {
                if (lsHeaders.FirstOrDefault().Equals(ApiKey))
                {
                    isValidAPIKey = true;
                }
            }
            else
            {
                return request.CreateResponse(HttpStatusCode.Forbidden, "API Key absente !");
            }

            if (!isValidAPIKey)
            {
                return request.CreateResponse(HttpStatusCode.Forbidden, "Mauvaise API Key !");
            }

            var response = await base.SendAsync(request, cancellationToken);

            return response;
        }
    }
}