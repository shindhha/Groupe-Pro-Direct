using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace DOMPLUS.MessageHandlers
{
    public class ApiKeyHandler : DelegatingHandler
    {
        private const string DOMPLUS_ApiKey = "1e31cfff-4a37-4362-8b53-68f87ab06a62";

        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            bool isValidAPIKey = false;
            IEnumerable<string> lsHeaders;

            var checkApiKeyExists = request.Headers.TryGetValues("apikey", out lsHeaders);

            if (checkApiKeyExists)
            {
                if (lsHeaders.FirstOrDefault().Equals(DOMPLUS_ApiKey))
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