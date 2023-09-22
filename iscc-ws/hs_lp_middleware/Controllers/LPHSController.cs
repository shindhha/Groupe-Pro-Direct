using System;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Mail;
using System.ServiceModel.Channels;
using System.Web;
using System.Web.Http;
using HS_MIDDLEWARE_LP.Models;
using Newtonsoft.Json;
using NLog;
using HS_MIDDLEWARE_LP.LPUtility;

namespace HS_MIDDLEWARE_LP.Controllers
{
    public class LPHSController : ApiController
    {
        private static Logger logger = LogManager.GetCurrentClassLogger();

        public string GetIp()
        {
            return GetClientIp();
        }

        [HttpPost]
        [Route("api/LeadInject")]
        public HttpResponseMessage LeadInject(HttpRequestMessage request, [FromBody] Leads DataLead)
        {
            string HermesLogin = "ws-ovh";
            string HermesPwd = "c8e56b2d5bd538c4d4e2ce9c12153f059a252818";
            string CampaignID = "LP_PROMOTION_HUBSPOT";

            try
            {
                LeadsReply leadReg = new LeadsReply();

                logger.Info(" ");
                logger.Info("Début injection depuis l'adresse IP : " + GetIp() + " >>>");
                logger.Info(JsonConvert.SerializeObject(DataLead));

                DataLead.getData();

                leadReg.dateCreation = DataLead.dateCreation;
                leadReg.cle = DataLead.cle;
                leadReg.civilite = DataLead.civilite;
                leadReg.email = DataLead.email;
                leadReg.nom = DataLead.nom;
                leadReg.prenom = DataLead.prenom;
                leadReg.telephone = DataLead.telephone;
                leadReg.codePostal = DataLead.codePostal;
                leadReg.adresse = DataLead.adresse;
                leadReg.complementAdresse = DataLead.complementAdresse;
                leadReg.ville = DataLead.ville;
                leadReg.commentConnu = DataLead.commentConnu;
                leadReg.informationSource1 = DataLead.informationSource1;
                leadReg.conversionRecente = DataLead.conversionRecente;
                leadReg.message = DataLead.message;
                leadReg.hubspotId = DataLead.hubspotId;
                leadReg.optin = DataLead.optin;
                leadReg.proprietaireContact = DataLead.proprietaireContact;
                leadReg.error = new LeadsError(DataLead);

                logger.Info(" >>> Data reçue et observée: <<< ");
                logger.Info(JsonConvert.SerializeObject(leadReg));

                if (string.IsNullOrEmpty(leadReg.error.errMessage))
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
                            string criteria = "ClientTable.CLE = '" + DataLead.cle + "'";
                            int numTask2 = leadInject.GetCallsInformations(1, CampaignID, criteria, 0);

                            TaskProgression taskResult2;
                            do
                            {
                                System.Threading.Thread.Sleep(500);
                                taskResult2 = leadInject.GetTaskProgression(numTask2);
                                logger.Info("Tentative pour tâche " + numTask2 + "...");
                                logger.Info("Tentative pour campId LP >> " + taskResult2.Result);
                            } while (taskResult2.Result == TaskResult.Pending || taskResult2.Result == TaskResult.InProgress);
                            CallInfo[] fiches = leadInject.GetCallsInformationsResult(numTask2);

                            if (fiches != null && fiches.Length > 0)
                            {
                                leadReg.error.errCode = 65;
                                leadReg.error.errMessage = "Injection KO > Doublon";

                                logger.Info(fiches.Length + " fiche(s) trouvée(s).");
                                logger.Info(JsonConvert.SerializeObject(fiches));

                                logger.Error("Doublon");
                                logger.Warn(JsonConvert.SerializeObject(DataLead));

                                Email("<h1>Doublon</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(leadReg) + "</pre><br>Cordialement,<br><br>API LP");

                                return request.CreateResponse(HttpStatusCode.Ambiguous, leadReg);
                            }
                            else
                            {
                                logger.Info("0 fiche trouvée.");
                                logger.Info(JsonConvert.SerializeObject(fiches));
                            }

                            int numTask = leadInject.AddClients(1, CampaignID, DataLead.getClientFileds(), DataLead.getData().ToArray(), true, DataLead.getClientPhone(), "", false, "", 0, 0, DateTime.MinValue);
                            TaskProgression taskResult;
                            ImportationError[] taskError;

                            do
                            {
                                System.Threading.Thread.Sleep(500);
                                taskResult = leadInject.GetTaskProgression(numTask);
                                logger.Info("Tentative pour tâche " + numTask + "...");
                                logger.Info("Tentative pour campId " + CampaignID + " >> " + taskResult.Result);
                            } while (taskResult.Result == TaskResult.Pending || taskResult.Result == TaskResult.InProgress);

                            taskError = leadInject.GetImportationErrors(numTask);

                            if (taskResult.Result == TaskResult.ErrorBadParameter)
                            {
                                leadReg.error.errCode = 66;
                                leadReg.error.errMessage = "Injection KO > " + JsonConvert.SerializeObject(taskError);
                                resultatInjection = leadReg.error.errMessage;
                                logger.Error(resultatInjection);
                            }
                            else if (taskResult.Result == TaskResult.CompletedWithError)
                            {
                                leadReg.error.errCode = 67;
                                leadReg.error.errMessage = "Injection KO 2 > " + JsonConvert.SerializeObject(taskError);
                                resultatInjection = leadReg.error.errMessage;
                                logger.Error(resultatInjection);
                            }
                            else if (taskResult.Result == TaskResult.ErrorTaskNotFound)
                            {
                                leadReg.error.errCode = 68;
                                leadReg.error.errMessage = "Injection KO 3 : Task not found > " + numTask;
                                resultatInjection = leadReg.error.errMessage;
                                logger.Error(resultatInjection);
                            }

                            logger.Info("Résultat : " + JsonConvert.SerializeObject(taskResult));
                            logger.Info(JsonConvert.SerializeObject(leadInject.GetTaskModifiedIndices(numTask)));

                            int numTask3 = leadInject.GetCallsInformations(1, CampaignID, criteria, 0);
                            TaskProgression taskResult3;
                            do
                            {
                                System.Threading.Thread.Sleep(500);
                                taskResult3 = leadInject.GetTaskProgression(numTask3);
                                logger.Info("Tentative pour tâche " + numTask3 + "...");
                                logger.Info("Tentative pour campId " + CampaignID + " >> " + taskResult3.Result);
                            } while (taskResult3.Result == TaskResult.Pending || taskResult3.Result == TaskResult.InProgress);
                            fiches = leadInject.GetCallsInformationsResult(numTask3);
                            if (fiches.Length > 0)
                            {
                                leadReg.callCenterProjectId = fiches[0].Indice.ToString();
                                logger.Info(JsonConvert.SerializeObject(fiches[0].Indice));
                                indice = leadReg.callCenterProjectId;
                                resultatInjection = "Injection OK";
                            }

                            int[] exceptionalErr = { 66, 67, 68, 69 };
                            if (!String.IsNullOrEmpty(leadReg.error.errMessage))
                            {
                                Email("<h1>" + resultatInjection + "</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(leadReg) + "</pre><br>Cordialement,<br><br>API LP");
                                return request.CreateResponse(HttpStatusCode.BadRequest, leadReg);
                            }
                            else if (exceptionalErr.Contains(leadReg.error.errCode) == true)
                            {
                                Email("<h1>" + resultatInjection + "</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(leadReg) + "</pre><br>Cordialement,<br><br>API LP");
                                return request.CreateResponse(HttpStatusCode.InternalServerError, leadReg);
                            }
                            Email("<h1>" + resultatInjection + " ( " + indice + " )</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(leadReg) + "</pre><br>Cordialement,<br><br>API LP");
                            return request.CreateResponse(HttpStatusCode.OK, leadReg);
                        }
                        catch (Exception ex)
                        {
                            Email("<h1>Erreur d'injection</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(leadReg) + "</pre><br>Cordialement,<br><br>API LP");
                            return request.CreateResponse(HttpStatusCode.BadRequest, ex);
                        }
                    }
                    else
                    {
                        leadReg.error = new LeadsError(DataLead);
                        leadReg.error.errCode = 41;
                        leadReg.error.errMessage = "Impossible de se connecter";

                        Email("<h1>Injection en erreur1</h1><h2>Lead injecté:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(leadReg) + "</pre><br>Cordialement,<br><br>API LP");
                        return request.CreateResponse(HttpStatusCode.Unauthorized, leadReg);
                    }
                }
                else
                {
                    Email("<h1>Injection en erreur2</h1><h2>Lead à injecter:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(leadReg) + "</pre><br>Cordialement,<br><br>API LP");
                    return request.CreateResponse(HttpStatusCode.BadRequest, leadReg);
                }
            }
            catch (NullReferenceException e)
            {
                Email("<h1>Injection en erreur3</h1><h2>Lead à injecter:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(e) + "</pre><br>Cordialement,<br><br>API EBV");
                return request.CreateResponse(HttpStatusCode.BadRequest, e);
            }
            catch (Exception e)
            {
                Email("<h1>Injection en erreur4</h1><h2>Lead à injecter:</h2><pre>" + JsonConvert.SerializeObject(DataLead) + "</pre><h2>Retour API:</h2><pre>" + JsonConvert.SerializeObject(e) + "</pre><br>Cordialement,<br><br>API EBV");
                return request.CreateResponse(HttpStatusCode.BadRequest, e);
            }
        }

        [HttpPost]
        [Route("api/GetCode")]
        public HttpResponseMessage GetCode(HttpRequestMessage request, [FromBody] Code DataCode)
        {
            CodeReply codeReg = new CodeReply();
            DataCode.getCode();
            codeReg.cle = DataCode.email;
            return request.CreateResponse(HttpStatusCode.OK, codeReg);
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
                //message.To.Add(new MailAddress("thierry.randriantiana@vivetic.mg"));
                message.CC.Add(new MailAddress("thierry.randriantiana@vivetic-group.com"));
                message.To.Add(new MailAddress("iscc@vivetic.mg"));
                message.Subject = "Injection des leads LP depuis HubSpot PROD";
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