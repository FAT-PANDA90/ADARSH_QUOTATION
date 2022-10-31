import json
import msal
import requests

client_id = '604b8ad1-55b0-439b-96a6-51d2e78f1c09'
client_secret = '5477382c-6c29-4e02-9833-d07dba014f2d'
tenant_id = 'f8cdef31-a31e-4b4a-93e4-5f571e91255a'

authority = f"https://login.microsoftonline.com/{tenant_id}"
app = msal.ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=authority)

scopes = ["https://graph.microsoft.com/.default"]

result = None
result = app.acquire_token_silent(scopes, account=None)

if not result:
    print(
        "No suitable token exists in cache. Let's get a new one from Azure Active Directory.")
    result = app.acquire_token_for_client(scopes=scopes)

# if "access_token" in result:
#     print("Access token is " + result["access_token"])