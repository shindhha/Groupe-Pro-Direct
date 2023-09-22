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

            edouardUtility.CallFileUtilities LeadsInject = new edouardUtility.CallFileUtilities();
            LeadsInject.CookieContainer = new System.Net.CookieContainer();
            string campId = "EDOUARD_DENIS";
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
            string telpro = System.Text.RegularExpressions.Regex.Replace((DataM.tel_professionnel == null) ? "vide" : DataM.tel_professionnel.ToString().Replace(" ", string.Empty).Replace("-", string.Empty), @"\D+", String.Empty);
            string email = DataM.email.ToString();
            string date_acqui = DataM.date_acquisition.ToString();
            date_acqui = date_acqui.Substring(0, 10).Replace("-", "");

            if (DataM.email != null)
            {
                if (telMobile.Length >= 9)
                {
                    string cle = email + "#" + telMobile + "#" + date_acqui;
                    DataM.cle = cle;
                }
            }

            //if (telMobile.Length < 9 && telPerso.Length < 9 && telpro.Length < 9)
            //{
            //    return Request.CreateResponse(HttpStatusCode.ExpectationFailed, "PhoneNumberError ");
            //}

            // clear factory phone number

            if (telMobile.Length >= 9)
            {
                DataM.tel_mobile = "0" + telMobile.Substring(telMobile.Length - 9);
            }
            if (telpro.Length >= 9)
            {
                DataM.tel_professionnel = "0" + telpro.Substring(telpro.Length - 9);
            }
            if (telPerso.Length >= 9)
            {
                DataM.tel_fixe = "0" + telPerso.Substring(telPerso.Length - 9);
            }
            // System.Diagnostics.Debug.WriteLine(DataM.tel_fixe + " " + DataM.tel_professionnel + " " + DataM.tel_mobile);


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
                    edouardUtility.TaskProgression taskResult;
                    edouardUtility.ImportationError[] TaskError;

                    logger.Info("contenu json :\n");
                    logger.Info(JsonConvert.DeserializeObject(JsonConvert.SerializeObject(DataM)));
                    do
                    {
                        System.Threading.Thread.Sleep(500);
                        taskResult = LeadsInject.GetTaskProgression(num_task);
                    } while (taskResult.Result == edouardUtility.TaskResult.Pending || taskResult.Result == edouardUtility.TaskResult.InProgress);
                    if (taskResult.Result == edouardUtility.TaskResult.ErrorBadParameter)
                    {

                        TaskError = LeadsInject.GetImportationErrors(num_task);

                        logger.Info("STATUS INJECTION : KO");
                        return Request.CreateResponse(HttpStatusCode.NotAcceptable, JsonConvert.DeserializeObject("{ 'message': 'Error injection','error':'unsupported key'}"));

                    }
                    else if (taskResult.Result == edouardUtility.TaskResult.CompletedWithError)
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
