# import requests
# import json

# def get_embed_url_and_token(report_id, username):
#     url = f"https://api.powerbi.com/v1.0/myorg/reports/{report_id}"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": "Bearer <ACCESS_TOKEN>",
#     }
#     params = {
#         "allowedEmbeddingDomains": [
#             "http://127.0.0.1:8000/"
#         ],
#         "username": username,
#     }
#     response = requests.post(url + "/GenerateToken", headers=headers, json=params)
#     if response.status_code != 200:
#         raise Exception(f"Failed to get embed URL and token. Response: {response.text}")
#     data = response.json()
#     return data["embedUrl"], data["token"]

# embed_url, token = get_embed_url_and_token("<REPORT_ID>", "<USERNAME>")

# # powerBI gateway
# # services - powerbi, 


import requests

# Replace these values with your own

def get_access_token(client_id, username, password):
    data = {
        'grant_type': 'password',
        'scope': 'openid',
        'resource': r'https://analysis.windows.net/powerbi/api',
        'client_id': client_id,
        'username': username,
        'password': password
    }
    token = requests.post('https://login.microsoftonline.com/common/oauth2/token', data=data)
    assert token.status_code == 200, "Fail to retrieve token: {}".format(token.text)
    return token.json().get('access_token')


client_id = "6127afdf-0323-4a7c-8f43-bb0d1759dc6f"
client_secret = "67ebe75d-a3b7-420c-9f5e-79c2f63064c0"
username = "Bolisetti190739@exlservice.com"
password = "Hasa2020$"

print(get_access_token(client_id, username, password))

# Get an access token
# url = "https://login.microsoftonline.com/common/oauth2/token"
# data = {
#     "resource": "https://analysis.windows.net/powerbi/api",
#     "client_id": client_id,
#     "client_secret": client_secret,
#     "username": username,
#     "password": password,
#     "grant_type": "password"
# }
# response = requests.post(url, data=data)
# print(response)
# Extract the access token from the response
# access_token = response.json()["access_token"]

# Make a GET request to the Power BI REST API

# url = "https://api.powerbi.com/v1.0/myorg/reports"
# headers = {
#     "Authorization": f"Bearer {access_token}"
# }
# response = requests.get(url, headers=headers)

# # Extract the reports from the response
# reports = response.json()["value"]
# print(reports)

# # def report_view(request):
# #     # Get access token for Power BI API
# #     access_token = get_access_token()

# #     # Get report id from Power BI API
# #     report_id = get_report_id()

# #     # Get embed URL for the report
# #     embed_url = get_embed_url(report_id)

# #     # Pass access token to the iframe
# #     context = {
# #         'embed_url': embed_url,
# #         'access_token': access_token
# #     }
# #     return render(request, 'report.html', context)
