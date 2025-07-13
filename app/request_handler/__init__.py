
# from flask import jsonify, Request
# from app.request_handler.status_code import StatusCode
# from app.request_handler.request_type import RequestType
# from app.request_handler.enums import RequestParams as RP

# class MethodNotAllowed(Exception):pass
# class MissingData(Exception):pass
# class SettingNotFound(Exception):pass
# class Unauthorized(Exception):pass

# class RequestHandler:
#      #HANDLE CONTENT
#     @staticmethod
#     def get_json(req:Request): return req.get_json() if req.is_json else None
#     @staticmethod
#     def get_form(req:Request): return req.form.to_dict() if req.form else None
#     @staticmethod
#     def get_query(req:Request): return req.args.to_dict() if req.args else None
#     @staticmethod
#     def get_raw(req:Request): return req.data if req.data else None
#     @staticmethod
#     def get_none(req:Request): return {'data':'no data expected'}
    
#     get_data_actions = {
#                     RP.JSON : get_json,
#                     RP.FORM : get_form,
#                     RP.QUERY : get_query,
#                     RP.RAW : get_raw,
#                     RP.NONE : get_none
#                     }
    
#     #HANDLE AUTHENTICATION
    
#     def __init__(self, settings:dict, request:Request):
#         self.settings:dict = settings.get(request.method) #this will automatically validate the method used
#         self.req = request
    
#     def request_is_valid(self):
#         #validte method
#         try: 
#             if self.settings is None: #means no settings where found in init
#                 raise MethodNotAllowed(f'{self.req.method} is not a valid method.')
            
#             #validate and get data
#             data_type:RP = self.settings.get(RP.CONTENT_TYPE)
#             if data_type is None:
#                 raise SettingNotFound(RP.CONTENT_TYPE.value)
            
#             data:dict = self.get_data_actions.get(data_type)(self.req)
#             if data is None:
#                 raise MissingData(data_type.value)
            
#             #check user
#             username_location:RP = self.settings.get(RP.USERNAME_LOCATION)
#             if username_location is None:
#                 raise SettingNotFound(RP.USERNAME_LOCATION.value)
            
#             return "MADE IT SO FAAAAAR!"
            
#             # auth_type:RP = self.settings.get(RP.AUTH_TYPE)
#             # if auth_type is None:
#             #     raise SettingNotFound("auth_type")
            
#             # if self.auth_actions.get(auth_type)(self.req):
#             #     raise Unauthorized("Missing or invalud authentication. Check username and where you put your auth")
            
            
#         except MethodNotAllowed as e:
#             return str(e), RP.STATUS_BAD_REQUEST
#         except SettingNotFound as e:
#             return f'{str(e)} is missing from settings. Find the developer and punish him.', RP.STATUS_BAD_REQUEST
#         except MissingData as e:
#             return f'No data found in {str(e)}. Did you put it the right place?', RP.STATUS_BAD_REQUEST
   
   
    
    
    
    
#     # def handle_request(target_method, level:Level, next_level:Level,
#     #                     get_secret_key:callable, get_data:callable, 
#     #                     level_response:callable, db:QuestDB, req):
#     #     #set default response
#     #     failed_request_level_response = level.get_failed_request_info()
#     #     response = {'request_status':StatusCode.BAD_REQUEST.value,
#     #             'level_info': failed_request_level_response}
        
#     #     #build request report
#     #     if not req.method == target_method:
#     #         response.update({'request_status': StatusCode.UNAUTHORIZED.value, 'error': 'You must work on the METHODology.'})
#     #         return jsonify(response), 404 #big failure
#     #     response.update({'method_status': 'accepted'})
        
#     #     # Retrieve X-secret-key from request headers
#     #     secret_key = get_secret_key(req)
#     #     user_validated = secret_key and db.get_team(secret_key) is not None
#     #     if not user_validated:
#     #         response.update({'request_status': StatusCode.UNAUTHORIZED.value, 'error': 'Missing the secret key ingredient X'})
#     #         return jsonify(response), 404 #big failure
#     #     response.update({'secret-key': 'accepted'})
#     #     response.update({'request_status':StatusCode.ACCEPTED.value}) #upgrades status to indicate method and username is handled correct

#     #     request_data = get_data(req)
        
#     #     #build level response
#     #     answer = request_data.get('answers','')
#     #     print("HERE!")
#     #     level_info = level_response(level=level, answer=answer, next_level=next_level, username=secret_key)
#     #     print(f"FROM LEVEL: {level_info}")
#     #     response.update({'level_info':level_info})
        
#     #     #check if level completed
#     #     answer_accepted = level_info.get('answer_accepted','')
#     #     if answer_accepted:
#     #         response.update({'request_accepted':True})
#     #         response.update({'request_status':StatusCode.OK.value})
        
#     #     return jsonify(response)