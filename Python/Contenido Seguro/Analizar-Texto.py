from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory, AnalyzeTextOptions

url = "<end point>"
clave = "<key1 or key2>"

cliente = ContentSafetyClient(url, AzureKeyCredential(clave))

texto = "Eres un poco idiota ..."
consulta = AnalyzeTextOptions(text=texto)

try:
    resultado = cliente.analyze_text(consulta)

    for item in resultado.categories_analysis:
        print(f"{item.category}: {item.severity}")

except HttpResponseError as e:
    print(f"Error {e.error.code}: {e.error.message}")