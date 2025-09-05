from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/webmasters"]
CLIENT_SECRET_FILE = "client_secret.json"  # coloca aquí tu JSON de OAuth
TOKEN_FILE = "token.json"

def get_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return build("searchconsole", "v1", credentials=creds)

def main():
    siteUrl = "sc-domain:plomeroculiacanpro.mx"
    feedpath = "https://plomeroculiacanpro.mx/sitemap.xml"
    
    try:
        service = get_service()
        result = service.sitemaps().submit(siteUrl=siteUrl, feedpath=feedpath).execute()
        print("✅ Sitemap enviado correctamente:", feedpath)
        print("Resultado:", result)
        
        # Verificar el estado del sitemap
        sitemaps = service.sitemaps().list(siteUrl=siteUrl).execute()
        print("\n📋 Sitemaps en la propiedad:")
        for sitemap in sitemaps.get('sitemap', []):
            print(f"- {sitemap.get('path')}: {sitemap.get('lastSubmitted', 'N/A')}")
            
    except Exception as e:
        if "403" in str(e):
            print("❌ Error 403: La propiedad no está verificada en Search Console")
            print("Debes verificar https://plomeroculiacanpro.mx/ en Search Console primero")
        elif "404" in str(e):
            print("❌ Error 404: El sitemap no es accesible")
            print("Verifica que https://plomeroculiacanpro.mx/sitemap.xml esté disponible")
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()