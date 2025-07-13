
from flask import jsonify, Request

from app.models.user import User
from app.request_handler.enums import RequestEnums as RE

from app.errors import MethodNotAllowed, SettingNotFound, MissingData, Unauthorized

class RequestHandler: 
    #INIT
    def __init__(self, settings:dict, request:Request, path:str):
        self.settings:dict = settings.get(request.method) #this will automatically validate the method used
        self.req:Request = request
        self.path:str = path
        self.body:dict = None
        self.validated:bool = False
        
        self.get_body_actions:dict = {
                RE.PATH : self.get_path_data
            }
        
        self.get_username_actions:dict = {
                RE.PATH : self.get_username_in_path,
                RE.NONE : self.no_username_needed
            }
    
    def validate(self):
        #validte method
        try:
            if self.settings is None: #means no settings where found in init
                raise MethodNotAllowed(f'{self.req.method} is not a valid method.')
            
            #validate and get data
            body_type:RE = self.settings.get(RE.BODY_TYPE)
            if body_type is None:
                raise SettingNotFound(RE.BODY_TYPE.value)
            
            self.body = self.get_body_actions.get(body_type)()
            if self.body is None:
                raise MissingData('content data')
            
            #get user
            username_location:RE = self.settings.get(RE.USERNAME_LOCATION)
            if username_location is None:
                raise SettingNotFound(RE.USERNAME_LOCATION.value)
            
            username = self.get_username_actions.get(username_location)()
            if username is None:
                raise MissingData('username')
            
            #authentication
            user_exists = User.query.filter_by(username=username).first()
            if not user_exists:
                raise Unauthorized(f'username {username} does not exist. Please register or check if you have spelled it correctly.')
            
            #accept request
            self.validated = True
            
            payload = {
                    'status': RE.STATUS_OK.value, 
                    'message':'Request has been validated successfully',
                    'body': self.body if self.body else '',
                    'username' : username
                }
            
            return jsonify(payload), RE.STATUS_OK.value
            
        except MethodNotAllowed as e:
            return jsonify({'error' : f'MethodNotAllowed: {str(e)}'}), RE.STATUS_BAD_REQUEST.value
        
        except SettingNotFound as e:
            return jsonify({'error':f'SettingNotFound: {str(e)} is missing from settings. Find the developer and punish him.'}), RE.STATUS_BAD_REQUEST.value
        
        except MissingData as e:
            return jsonify({'error' : f'MissingData: could not find {str(e)}. Did you put it the right place?'}),  RE.STATUS_BAD_REQUEST.value
        
        except Unauthorized as e:
            return jsonify({'error' : f'username {str(e)} could not be authorized'}), RE.STATUS_UNAUTHORIZED.value
        
     #HANDLE CONTENT
    def get_path_data(self): 
        data:list[str] = self.path.split('/') if self.path else []
        return [x for x in data if x is not None and str(x).strip() != '']
    
    # @staticmethod
    # def get_json(req:Request): return req.get_json() if req.is_json else None
    # @staticmethod
    # def get_form(req:Request): return req.form.to_dict() if req.form else None
    # @staticmethod
    # def get_query(req:Request): return req.args.to_dict() if req.args else None
    # @staticmethod
    # def get_raw(req:Request): return req.data if req.data else None
    # @staticmethod
    # def get_none(req:Request): return {'data':'no data expected'}
    
    #GET USERNAME
    def get_username_in_path(self):
        """username should always be the first param is this method is used"""
        data:list[str] = self.get_body_actions.get(RE.PATH)()
        return data[0] if len(data) > 0 else None
    
    def no_username_needed(self):
        return RE.UNREGISTERED_USER.value