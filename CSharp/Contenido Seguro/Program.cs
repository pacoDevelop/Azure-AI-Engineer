using Azure.AI.ContentSafety;
using Azure;

namespace Contenido_Seguro 
{
    class Program
    {
        static void Main(string[] args)
        {
            string url = "<end point>";
            string clave = "<key1 or key2>";

            var cliente = new ContentSafetyClient(new Uri(url), new AzureKeyCredential(clave));

            string texto = "Eres un poco idiota ...";
            var consulta = new AnalyzeTextOptions(texto);

            try
            {
                var respuesta = cliente.AnalyzeText(consulta);

                foreach (var item in respuesta.Value.CategoriesAnalysis)
                {
                    Console.WriteLine($"{item.Category}: {item.Severity}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }
    }
}