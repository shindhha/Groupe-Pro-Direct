using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Http;
using System.ServiceModel.Channels;
using System.Web;
using System.Web.Http;
using NLog;
using Newtonsoft.Json;


namespace Lpbascule.Controllers
{
    public class LpPromotionController : ApiController
    {
        private static Logger logger = LogManager.GetCurrentClassLogger();

        public string GetIp()
        {
            return GetClientIp();
        }
        private string GetClientIp(HttpRequestMessage request = null)
        {
            request = request ?? Request;

            if (request.Properties.ContainsKey("MS_HttpContext"))
            {
                return ((HttpContextWrapper)request.Properties["MS_HttpContext"]).Request.UserHostAddress;
            }
            else if (request.Properties.ContainsKey(RemoteEndpointMessageProperty.Name))
            {
                RemoteEndpointMessageProperty prop = (RemoteEndpointMessageProperty)request.Properties[RemoteEndpointMessageProperty.Name];
                return prop.Address;
            }
            else if (HttpContext.Current != null)
            {
                return HttpContext.Current.Request.UserHostAddress;
            }
            else
            {
                return null;
            }

        }


        [HttpPost]
        [Route("api/LpBasculeInject")]
        public HttpResponseMessage LpBasculeInject([FromBody] Models.LpPromo DataLp)
        {
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
            string dateDemarrage = DateTime.Now.ToString("yyyy-MM-dd hh:mm:ss");
            logger.Info("Appel du webservice  par L'IP : " + GetIp());

            Lpbascule.LpPromotionUtility.CallFileUtilities LeadsInject = new Lpbascule.LpPromotionUtility.CallFileUtilities();
            LeadsInject.CookieContainer = new System.Net.CookieContainer();
            string campId = "LP_PROMOTION_CONFIRMATION_RDV";
            Models.LpPromo DataM = new Models.LpPromo();

            try
            {
                JsonConvert.PopulateObject(JsonConvert.SerializeObject(DataLp), DataM);

            }
            catch (Exception e)
            {
                return Request.CreateResponse(HttpStatusCode.ExpectationFailed, e);
            }

            string Tel = System.Text.RegularExpressions.Regex.Replace((DataM.telephone == null) ? "vide" : DataM.telephone.ToString().Replace(" ", string.Empty).Replace("-", string.Empty), @"\D+", String.Empty);


            if (Tel.Length < 9)
            {
                return Request.CreateResponse(HttpStatusCode.ExpectationFailed, "PhoneNumberError ");
            }


            DataM.telephone = "0" + Tel.Substring(Tel.Length - 9);

            bool retourLog = LeadsInject.Login("ws-ovh", "c8e56b2d5bd538c4d4e2ce9c12153f059a252818");

            if (retourLog)
            {
                logger.Info("connection Hermes Status : OK");
                try
                {


                    string[] clientFields = DataM.getClientFields();
                    string[] phoneFields = DataM.getClientPhone();
                    var Data2send = DataM.getDataLpPromo();

                    int num_task = LeadsInject.AddClients(1, campId, clientFields, Data2send.ToArray(), true, phoneFields, "", false, "", 0, 0, DateTime.MinValue);
                    Lpbascule.LpPromotionUtility.TaskProgression taskResult;
                    Lpbascule.LpPromotionUtility.ImportationError[] TaskError;

                    logger.Info("contenu json :\n");
                    logger.Info(JsonConvert.DeserializeObject(JsonConvert.SerializeObject(DataM)));
                    do
                    {
                        System.Threading.Thread.Sleep(500);
                        taskResult = LeadsInject.GetTaskProgression(num_task);
                    } while (taskResult.Result == Lpbascule.LpPromotionUtility.TaskResult.Pending || taskResult.Result == Lpbascule.LpPromotionUtility.TaskResult.InProgress);


                    if (taskResult.Result == LpPromotionUtility.TaskResult.ErrorBadParameter)
                    {

                        TaskError = LeadsInject.GetImportationErrors(num_task);

                        logger.Info("STATUS INJECTION : KO");
                        return Request.CreateResponse(HttpStatusCode.NotAcceptable, JsonConvert.DeserializeObject("{ 'message': 'Error injection','error':'unsupported key'}"));

                    }
                    else if (taskResult.Result == LpPromotionUtility.TaskResult.CompletedWithError)
                    {
                        logger.Info("STATUS INJECTION : KO");
                        return Request.CreateResponse(HttpStatusCode.ExpectationFailed, JsonConvert.DeserializeObject("{ 'message': 'injection error','error':'duplicate row '}"));
                    }

                    logger.Info("STATUS INJECTION : SUCCESS");
                    return Request.CreateResponse(HttpStatusCode.OK, JsonConvert.DeserializeObject("{ 'message': 'injection success','error':''}"));


                }
                catch
                {
                    logger.Info("STATUS INJECTION : ERROR");
                    return Request.CreateResponse(HttpStatusCode.NotAcceptable, JsonConvert.DeserializeObject("{ 'message': 'injection Error','Error':'format donné invalide'}"));
                }
            }
            else
            {
                logger.Info("Problème d'authentification : " + dateDemarrage + " Probablement une coupure vocaclom");
                return Request.CreateResponse(HttpStatusCode.NotImplemented, JsonConvert.DeserializeObject("{ 'message': 'injection error','error': 'Error serveur'}"));
            }



        }


    }
}
