using EBV_DOMPLUS_sandbox.Models;
using Newtonsoft.Json;
using NLog;
using System;
using System.Net;
using System.Net.Http;
using System.ServiceModel.Channels;
using System.Web;
using System.Web.Http;
using EBV_DOMPLUS_sandbox.ebvUtility;
using System.Linq;
using System.Net.Mail;

namespace EBV_DOMPLUS_sandbox.Controllers
{
    public class EBVController : ApiController
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
            string CampaignID = "95A4A7A5075443B4";
            //string CampaignID = "EBV";
            try
            {
                LeadReply LeadReg = new LeadReply();

                logger.Info(" ");
                logger.Info("Début injection depuis l'adresse IP : " + GetIp() + ">>>");
                logger.Info(JsonConvert.SerializeObject(DataLead));

                DataLead.getDataEBV();

                LeadReg.error = new LeadError(DataLead);
                LeadReg.dateCreation = DataLead.dateCreation;
                LeadReg.cle = DataLead.cle;
                LeadReg.nom = DataLead.nom;
                LeadReg.prenom = DataLead.prenom;
                LeadReg.email = DataLead.email;
                LeadReg.telephone = DataLead.telephone;
                LeadReg.dateRappel = DataLead.dateRappel;
                LeadReg.heureRappel = DataLead.heureRappel;
                LeadReg.produit = DataLead.produit;
                LeadReg.message = DataLead.message;

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
                            string creiteria = "ClientTable.CLE = '" + DataLead.DefineCle(DataLead) + "' AND ClientTable.SOURCE = '" + DataLead.source.Trim().ToUpper() + "'";
                            
                            int numTask2 = leadInject.GetCallsInformations(1, CampaignID, creiteria, 0);

                            TaskProgression taskResult2;
                            do
                            {
                                System.Threading.Thread.Sleep(500);
                                taskResult2 = leadInject.GetTaskProgression(numTask2);
                                logger.Info("Tentative pour tâche " + numTask2 + "...");
                                logger.Info("Tentative pour campId EBV >> " + taskResult2.Result);
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

                                Email("<h1>Doublon</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(LeadReg) + "</pre><br>Cordialement,<br><br>API EBV");

                                return request.CreateResponse(HttpStatusCode.Ambiguous, LeadReg);
                            }
                            else
                            {
                                logger.Info("0 fiche trouvée.");
                                logger.Info(JsonConvert.SerializeObject(fiches));
                            }

                            //Pour la source formulaire uniquement
                            //Tous les rappels de même jour différents de l'heure de rappel indiqué du même numéro de téléphone vont être exclus si possible
                            if (DataLead.source.Trim().ToLower() == "formulaire")
                            {
                                string criteriaExclusion = "ClientTable.TELEPHONE = '" + DataLead.telephone + "' AND ClientTable.DATERAPPEL = '" + DataLead.dateRappel + "' AND ClientTable.HEURERAPPEL != '" + DataLead.heureRappel + "'";
                                string reasonExclusion = "FICHE EXCLUE DEPUIS LE WS LE " + DateTime.Now.ToString("dd/MM/yyyy") + " A " + DateTime.Now.ToString("HH:mm:ss");
                                int numTaskExclusion = leadInject.ExcludeCalls(1, CampaignID, criteriaExclusion, reasonExclusion);
                                TaskProgression taskResultExlu;
                                do
                                {
                                    System.Threading.Thread.Sleep(500);
                                    taskResultExlu = leadInject.GetTaskProgression(numTaskExclusion);
                                }
                                while (taskResultExlu.Result == TaskResult.Pending || taskResultExlu.Result == TaskResult.InProgress);
                            }

                            int numTask = leadInject.AddClients(1, CampaignID, DataLead.getClientFields(), DataLead.getDataEBV().ToArray(), true, DataLead.getClientPhone(), "", false, "", 0, 0, DateTime.MinValue);
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

                            int numTask3 = leadInject.GetCallsInformations(1, CampaignID, creiteria, 0);
                            TaskProgression taskResult3;
                            do
                            {
                                System.Threading.Thread.Sleep(500);
                                taskResult3 = leadInject.GetTaskProgression(numTask3);
                                logger.Info("Tentative pour tâche " + numTask3 + "...");
                                logger.Info("Tentative pour campId EBV >> " + taskResult3.Result);
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
                                Email("<h1>" + resultatInjection + "</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(LeadReg) + "</pre><br>Cordialement,<br><br>API EBV");
                                return request.CreateResponse(HttpStatusCode.BadRequest, LeadReg);
                            }
                            else if (exceptionalErr.Contains(LeadReg.error.errCode) == true)
                            {
                                Email("<h1>" + resultatInjection + "</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(LeadReg) + "</pre><br>Cordialement,<br><br>API EBV");
                                return request.CreateResponse(HttpStatusCode.InternalServerError, LeadReg);
                            }
                            Email("<h1>" + resultatInjection + " ( " + indice + " )</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(LeadReg) + "</pre><br>Cordialement,<br><br>API EBV");
                            return request.CreateResponse(HttpStatusCode.OK, LeadReg);
                        }
                        catch (Exception ex)
                        {
                            Email("<h1>Erreur d'injection</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(LeadReg) + "</pre><br>Cordialement,<br><br>API EBV");
                            return request.CreateResponse(HttpStatusCode.BadRequest, ex);
                        }
                    }
                    else
                    {
                        LeadReg.error = new LeadError(DataLead);
                        LeadReg.error.errCode = "41";
                        LeadReg.error.errMessage = "Impossible de se connecter";

                        Email("<h1>Injection en erreur</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(LeadReg) + "</pre><br>Cordialement,<br><br>API GEOXIA");
                        return request.CreateResponse(HttpStatusCode.Unauthorized, LeadReg);
                    }
                }
                else
                {
                    Email("<h1>Injection en erreur</h1><h2>Lead à injecter:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(LeadReg) + "</pre><br>Cordialement,<br><br>API EBV");
                    return request.CreateResponse(HttpStatusCode.BadRequest, LeadReg);
                }
            }
            catch (NullReferenceException e)
            {
                Email("<h1>Injection en erreur</h1><h2>Lead à injecter:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(e) + "</pre><br>Cordialement,<br><br>API EBV");
                return request.CreateResponse(HttpStatusCode.BadRequest, e);
            }
            catch (Exception e)
            {
                Email("<h1>Injection en erreur</h1><h2>Lead à injecter:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(e) + "</pre><br>Cordialement,<br><br>API EBV");
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

        private static void Email(string body)
        {
            logger.Info("Email ...");
            try
            {
                MailMessage message = new MailMessage();
                SmtpClient smtp = new SmtpClient();
                message.From = new MailAddress("noreply@vivetic.com");
                message.To.Add(new MailAddress("thierry.randriantiana@vivetic.mg"));
                //message.CC.Add(new MailAddress("thierry.randriantiana@vivetic-group.com"));
                //message.To.Add(new MailAddress("iscc@vivetic.mg"));
                message.Subject = "Injection des leads EBV";
                message.IsBodyHtml = true;
                message.Body = body;
                smtp.Port = 587;
                smtp.Host = "mail.vivetic.com";
                smtp.UseDefaultCredentials = false;
                smtp.Credentials = new NetworkCredential("noreply@vivetic.com", "N0reply2015");
                smtp.DeliveryMethod = SmtpDeliveryMethod.Network;
                logger.Info("Tentative d'envoi de mail ...");
                smtp.Send(message);
                logger.Info("Mail envoyé.");
            }
            catch (Exception)
            {
                logger.Error("Envoi échoué.");
            }
        }
    }
}
