using System;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.ServiceModel.Channels;
using System.Web;
using System.Web.Http;
using DOMPLUS.domplusUtilities;
using DOMPLUS.Models;
using Newtonsoft.Json;
using NLog;

namespace DOMPLUS.Controllers
{
    public class DomPlusController : ApiController
    {
        private static Logger logger = LogManager.GetCurrentClassLogger();

        public string GetIp()
        {
            return GetClientIp();
        }

        [HttpPost]
        [Route("api/LeadInject")]
        public HttpResponseMessage LeadInject(HttpRequestMessage request, [FromBody] Lead DataLead)
        {
            //Paramètres
            string HermesLogin = "admin";
            string HermesPwd = "02e5d8130f0ce649af579cc4030a1b361bfaedc9";
            string CampaignID = "DOMPLUS";
            try
            {
                DataLead.uniqId = Guid.NewGuid().ToString();
                LeadReply LeadReg = new LeadReply();
                LeadReg.daty = DataLead.getDaty();

                logger.Info(" ");
                logger.Info("Début injection depuis l'adresse IP : " + GetIp() + ">>>");
                logger.Info(JsonConvert.SerializeObject(DataLead));

                LeadReg.error = new LeadError(DataLead);
                LeadReg.nom = DataLead.nom;
                LeadReg.prenom = DataLead.prenom;
                LeadReg.produit = DataLead.getProduit();
                LeadReg.email = DataLead.email;
                LeadReg.tel = DataLead.tel1 + " | " + DataLead.tel2;
                LeadReg.uniqId = DataLead.uniqId;

                if (string.IsNullOrEmpty(LeadReg.error.errCode))
                {
                    ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
                    CallFileUtilities leadInject = new CallFileUtilities();
                    leadInject.CookieContainer = new CookieContainer();
                    bool isLogged = leadInject.Login(HermesLogin, HermesPwd);

                    string resultatInjection = "";
                    string indice = "";

                    if (isLogged)
                    {
                        try
                        {
                            int numTask2 = leadInject.GetCallsInformations(1, CampaignID, "CONCAT(RIGHT(ClientTable.TEL1, 9), RIGHT(ClientTable.TEL2, 9)) = CONCAT(RIGHT('" + DataLead.tel1 + "', 9), RIGHT('" + DataLead.tel2 + "', 9))", 0);
                            TaskProgression taskResult2;
                            do
                            {
                                System.Threading.Thread.Sleep(500);
                                taskResult2 = leadInject.GetTaskProgression(numTask2);
                                logger.Info("Tentative pour tâche " + numTask2 + "...");
                                logger.Info("Tentative pour campId DOMPLUS >> " + taskResult2.Result);
                            } while (taskResult2.Result == TaskResult.Pending || taskResult2.Result == TaskResult.InProgress);
                            CallInfo[] fiches = leadInject.GetCallsInformationsResult(numTask2);

                            if (fiches != null && fiches.Length > 0)
                            {
                                LeadReg.error.errCode = "65";
                                LeadReg.error.errMessage = "Injection KO > Doublon";

                                logger.Info(fiches.Length + " fiche(s) trouvée(s).");
                                logger.Info(JsonConvert.SerializeObject(fiches));

                                logger.Error("Doublon");
                                logger.Warn(JsonConvert.SerializeObject(DataLead));

                                return request.CreateResponse(HttpStatusCode.Ambiguous, LeadReg);
                            }
                            else
                            {
                                logger.Info("0 fiche trouvée.");
                                logger.Info(JsonConvert.SerializeObject(fiches));
                            }

                            int numTask = leadInject.AddClients(1, CampaignID, DataLead.getClientFields(), DataLead.getDataDomplus().ToArray(), true, DataLead.getClientPhone(), "", false, "", 0, 0, DateTime.MinValue);
                            TaskProgression taskResult;
                            ImportationError[] taskError;

                            do
                            {
                                System.Threading.Thread.Sleep(500);
                                taskResult = leadInject.GetTaskProgression(numTask);
                                logger.Info("Tentative pour tâche " + numTask + "...");
                                logger.Info("Tentative pour campId DOMPLUS >> " + taskResult.Result);
                            } while (taskResult.Result == TaskResult.Pending || taskResult.Result == TaskResult.InProgress);

                            taskError = leadInject.GetImportationErrors(numTask);

                            if (taskResult.Result == TaskResult.ErrorBadParameter)
                            {
                                LeadReg.error.errCode = "66";
                                LeadReg.error.errMessage = "Injection KO > " + JsonConvert.SerializeObject(taskError);
                                resultatInjection = LeadReg.error.errMessage;
                                logger.Error(resultatInjection);
                            }
                            else if (taskResult.Result == TaskResult.CompletedWithError)
                            {
                                LeadReg.error.errCode = "67";
                                LeadReg.error.errMessage = "Injection KO 2 > " + JsonConvert.SerializeObject(taskError);
                                resultatInjection = LeadReg.error.errMessage;
                                logger.Error(resultatInjection);
                            }
                            else if (taskResult.Result == TaskResult.ErrorTaskNotFound)
                            {
                                LeadReg.error.errCode = "68";
                                LeadReg.error.errMessage = "Injection KO 3 : Task not found > " + numTask;
                                resultatInjection = LeadReg.error.errMessage;
                                logger.Error(resultatInjection);
                            }

                            logger.Info("Résultat : " + JsonConvert.SerializeObject(taskResult));
                            logger.Info(JsonConvert.SerializeObject(leadInject.GetTaskModifiedIndices(numTask)));

                            int numTask3 = leadInject.GetCallsInformations(1, CampaignID, "CONCAT(RIGHT(ClientTable.TEL1, 9), RIGHT(ClientTable.TEL2, 9)) = CONCAT(RIGHT('" + DataLead.tel1 + "', 9), RIGHT('" + DataLead.tel2 + "', 9))", 0);
                            TaskProgression taskResult3;
                            do
                            {
                                System.Threading.Thread.Sleep(500);
                                taskResult3 = leadInject.GetTaskProgression(numTask3);
                                logger.Info("Tentative pour tâche " + numTask3 + "...");
                                logger.Info("Tentative pour campId DOMPLUS >> " + taskResult3.Result);
                            } while (taskResult3.Result == TaskResult.Pending || taskResult3.Result == TaskResult.InProgress);
                            fiches = leadInject.GetCallsInformationsResult(numTask3);
                            if (fiches.Length > 0)
                            {
                                LeadReg.callCenterProjectId = fiches[0].Indice.ToString();
                                logger.Info(JsonConvert.SerializeObject(fiches[0].Indice));
                                indice = LeadReg.callCenterProjectId;
                                resultatInjection = "Injection OK";
                            }

                            string[] exceptionalErr = { "66", "67", "68", "69" };
                            if (!String.IsNullOrEmpty(LeadReg.error.errCode))
                            {
                                return request.CreateResponse(HttpStatusCode.BadRequest, LeadReg);
                            }
                            else if (exceptionalErr.Contains(LeadReg.error.errCode) == true)
                            {
                                return request.CreateResponse(HttpStatusCode.InternalServerError, LeadReg);
                            }
                            return request.CreateResponse(HttpStatusCode.OK, LeadReg);
                        }
                        catch (Exception ex)
                        {
                            return request.CreateResponse(HttpStatusCode.BadRequest, ex);
                        }
                    }
                    else
                    {
                        LeadReg.error = new LeadError(DataLead);
                        LeadReg.error.errCode = "404";
                        LeadReg.error.errMessage = "Impossible de se connecter";
                        return request.CreateResponse(HttpStatusCode.Unauthorized, LeadReg);
                    }
                }
                else
                {
                    return request.CreateResponse(HttpStatusCode.BadRequest, LeadReg);
                }
            }
            catch (NullReferenceException e)
            {
                return request.CreateResponse(HttpStatusCode.BadRequest, e);
            }
            catch (Exception e)
            {
                return request.CreateResponse(HttpStatusCode.BadRequest, e);
            }
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

            return null;
        }
    }
}
