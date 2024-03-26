# import base64
#
# import requests
# from cognitojwt import jwt_sync
#
#
# settings = Settings()
# ddb = initialize_dynamodb()
# user_table = ddb.Table("user")
# cognito = initialize_cognito()
#
#
# async def get_refresh_token(token: str):
#     cognito_client_id = cognito.cognito_client_id
#     cognito_client_password = cognito.cognito_client_password
#     cognito_domain = cognito.cognito_domain
#
#     base_encode = cognito_client_id + ":" + cognito_client_password
#     encoded_bytes = base64.b64encode(base_encode.encode("utf-8"))
#     encoded_string = encoded_bytes.decode("utf-8")
#
#     token_endpoint = cognito_domain + "/oauth2/token"
#     payload = {
#         "grant_type": "refresh_token",
#         "client_id": cognito_client_id,
#         "refresh_token": token,
#     }
#
#     # 헤더 설정
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Authorization": "Basic " + encoded_string,
#     }
#
#     response = requests.post(token_endpoint, headers=headers, data=payload)
#     json_data = response.json()
#     access_token = json_data.get("access_token")
#     token_dto = TokenDto(access_token=access_token, refresh_token=token)
#     return token_dto
#
#
# async def get_access_token(code: str):
#     cognito_client_id = cognito.cognito_client_id
#     cognito_client_password = cognito.cognito_client_password
#     redirect_uri = cognito.redirect_uri
#     cognito_domain = cognito.cognito_domain
#     cognito_userpool_region = cognito.cognito_userpool_region
#     cognito_userpool_id = cognito.cognito_userpool_id
#
#     base_encode = cognito_client_id + ":" + cognito_client_password
#     encoded_bytes = base64.b64encode(base_encode.encode("utf-8"))
#     encoded_string = encoded_bytes.decode("utf-8")
#
#     token_endpoint = cognito_domain + "/oauth2/token"
#     payload = {
#         "grant_type": "authorization_code",
#         "client_id": cognito_client_id,
#         "code": code,
#         "redirect_uri": redirect_uri,
#     }
#
#     # 헤더 설정
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Authorization": "Basic " + encoded_string,
#     }
#
#     response = requests.post(token_endpoint, headers=headers, data=payload)
#     json_data = response.json()
#     access_token = json_data.get("access_token")
#     refresh_token = json_data.get("refresh_token")
#     id_token = json_data.get("id_token")
#     result = jwt_sync.decode(
#         id_token, cognito_userpool_region, cognito_userpool_id, cognito_client_id
#     )
#     email = result.get("email")
#     cognito_id = result.get("sub")
#
#     user = await user_service.get_user(cognito_id)
#     if not user:
#         create_user_dto = UserDto(
#             email=email, id=cognito_id, created_at=get_current_time()
#         )
#         user_table.put_item(Item=create_user_dto.dict())
#
#     token_dto = TokenDto(access_token=access_token, refresh_token=refresh_token)
#     return token_dto
