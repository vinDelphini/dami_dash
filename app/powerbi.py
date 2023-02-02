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