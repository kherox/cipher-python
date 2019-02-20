import sys , os 
class AuthorizationMiddleware(object):
    def __init__(self,app):
        self.app =  app
        self.allow_hosts = ["127.0.0.1"]
    
    def __call__(self,environ ,start_response):
        if (environ['SERVER_NAME'] in self.allow_hosts):
            return self.app(environ , start_response)
        else:
            os.system("KILL %d" % os.getpid())
            sys.exit(1)

