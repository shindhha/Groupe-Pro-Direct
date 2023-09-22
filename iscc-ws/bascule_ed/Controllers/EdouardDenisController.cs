using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using NLog;
using Newtonsoft.Json;
using System.Web;
using System.ServiceModel.Channels;
using EdouardDenis.Models;

namespace EdouardDenis.Controllers
{
    public class EdouardDenisController : ApiController
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

        public HttpResponseMessage EdouardInject([FromBody] Models.EdouardDenis DataEdouard)
        {
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
            string dateDemarrage = DateTime.Now.ToString("yyyy-MM-dd hh:mm:ss");
            logger.Info("Appel du webservice  par L'IP : " + GetIp());

            BasculeEdouardDenis.EdouardDenis_edouardUtility.CallFileUtilities LeadsInject = new BasculeEdouardDenis.EdouardDenis_edouardUtility.CallFileUtilities();
            LeadsInject.CookieContainer = new System.Net.CookieContainer();
            string campId = "31_RA_EDOUARD_DENIS";
            Models.EdouardDenis DataM = new Models.EdouardDenis();

            try
            {
                JsonConvert.PopulateObject(JsonConvert.SerializeObject(DataEdouard), DataM);

            }
            catch (Exception e)
            {
                return Request.CreateResponse(HttpStatusCode.ExpectationFailed, e);
            }

            string telMobile = System.Text.RegularExpressions.Regex.Replace((DataM.tel_mobile == null) ? "vide" : DataM.tel_mobile.ToString().Replace(" ", string.Empty).Replace("-", string.Empty), @"\D+", String.Empty);
            string telPerso = System.Text.RegularExpressions.Regex.Replace((DataM.tel_fixe == null) ? "vide" : DataM.tel_fixe.ToString().Replace(" ", String.Empty).Replace("-", String.Empty), @"\D+", String.Empty);


            if (telMobile.Length < 9 && telPerso.Length < 9)
            {
                return Request.CreateResponse(HttpStatusCode.ExpectationFailed, "PhoneNumberError ");
            }





            bool retourLog = LeadsInject.Login("ws-ovh", "c8e56b2d5bd538c4d4e2ce9c12153f059a252818");



            if (retourLog)
            {
                logger.Info("connection Hermes Status : OK");
                try
                {


                    string[] clientFields = DataM.getClientFields();
                    string[] phoneFields = DataM.getClientPhone();
                    var Data2send = DataM.getDataEdouardDenis();

                    int num_task = LeadsInject.AddClients(1, campId, clientFields, Data2send.ToArray(), true, phoneFields, "", false, "", 0, 0, DateTime.MinValue);
                    BasculeEdouardDenis.EdouardDenis_edouardUtility.TaskProgression taskResult;
                    BasculeEdouardDenis.EdouardDenis_edouardUtility.ImportationError[] TaskError;

                    logger.Info("contenu json :\n");
                    logger.Info(JsonConvert.DeserializeObject(JsonConvert.SerializeObject(DataM)));
                    do
                    {
                        System.Threading.Thread.Sleep(500);
                        taskResult = LeadsInject.GetTaskProgression(num_task);
                    } while (taskResult.Result == BasculeEdouardDenis.EdouardDenis_edouardUtility.TaskResult.Pending || taskResult.Result == BasculeEdouardDenis.EdouardDenis_edouardUtility.TaskResult.InProgress);
                    if (taskResult.Result == BasculeEdouardDenis.EdouardDenis_edouardUtility.TaskResult.ErrorBadParameter || taskResult.Result == BasculeEdouardDenis.EdouardDenis_edouardUtility.TaskResult.CompletedWithError)
                    {


                        try
                        {
                            TaskError = LeadsInject.GetImportationErrors(num_task);

                            logger.Info("STATUS INJECTION : KO");
                            return Request.CreateResponse(HttpStatusCode.NotAcceptable, JsonConvert.DeserializeObject("{ 'message': 'Error injection','error':'unsupported key'}"));
                        }
                        catch
                        {
                            logger.Info("STATUS INJECTION : KO");
                            return Request.CreateResponse(HttpStatusCode.ExpectationFailed, JsonConvert.DeserializeObject("{ 'message': 'injection error','error':'Column and keys not compatible'}"));
                        }



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
