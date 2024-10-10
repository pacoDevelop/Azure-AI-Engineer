using Microsoft.Graph;
using Microsoft.Graph.Auth;
using Microsoft.Identity.Client;
using Newtonsoft.Json;

namespace Demos.EntraID.ConsoleApp1
{
    public class OData
    {
        [JsonProperty("odata.metadata")]
        public string Metadata { get; set; }
        public Object Value { get; set; }
    }

    internal class Program
    {
        static IConfidentialClientApplication app;

        static void Main(string[] args)
        {
            Console.Clear();

            //////////////////////////////////////////////////////////////////////////////////////////////
            /// Generar el objeto aplicación
            //////////////////////////////////////////////////////////////////////////////////////////////

            app = ConfidentialClientApplicationBuilder
                .Create("<Id Application>")
                .WithClientSecret("<Secret Application>")
                .WithAuthority("https://login.microsoftonline.com/<Id Tenant>")
                .Build();


            //////////////////////////////////////////////////////////////////////////////////////////////
            /// Generar el token
            //////////////////////////////////////////////////////////////////////////////////////////////

            string[] scopes = new string[] { "https://graph.microsoft.com/.default" };
            AuthenticationResult token = app.AcquireTokenForClient(scopes).ExecuteAsync().Result;

            Console.WriteLine(token.AccessToken);
            Console.ReadKey();


            //////////////////////////////////////////////////////////////////////////////////////////////
            /// Listado de usuario mediante un cliente HTTP
            //////////////////////////////////////////////////////////////////////////////////////////////

            Console.Clear();

            var http = new HttpClient();
            string url = "https://graph.microsoft.com/v1.0/users";

            http.DefaultRequestHeaders.Authorization =
                new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token.AccessToken);

            var response = http.GetAsync(url).Result;
            if (response.StatusCode == System.Net.HttpStatusCode.OK)
            {
                string dataJSON = response.Content.ReadAsStringAsync().Result;
                OData data = JsonConvert.DeserializeObject<OData>(dataJSON);
                List<User> usuarios = JsonConvert.DeserializeObject<List<User>>(data.Value.ToString());

                foreach (var usuario in usuarios)
                    Console.WriteLine($" -> {usuario.DisplayName} - {usuario.UserPrincipalName}");
            }
            else Console.WriteLine($"Error {response.StatusCode}");

            Console.ReadKey();


            //////////////////////////////////////////////////////////////////////////////////////////////
            /// Listado de usuario mediante objetos .NET
            //////////////////////////////////////////////////////////////////////////////////////////////

            Console.WriteLine("");

            ClientCredentialProvider authProvider = new ClientCredentialProvider(app);
            GraphServiceClient graphClient = new GraphServiceClient(authProvider);

            var result = graphClient.Users.Request().GetAsync().Result;

            foreach (var user in result)
                Console.WriteLine($" -> {user.DisplayName} {user.UserPrincipalName}");

            Console.ReadKey();
        }
    }
}
