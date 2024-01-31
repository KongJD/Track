import logging
import json
import time
import requests

from django.utils.deprecation import MiddlewareMixin

def getIP(request):
    with open("/public/Users/liangq/website/Test_upload/UploadPrj/log/META.log","a") as w:
        w.write(str(request.META)+'\n')
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR").split(',')[0]
        return ip
    else:
        try:
            ip = request.META.get("REMOTE_ADDR").split(',')[0]
            return ip
        except:
            return "ip:null"



class ApiLoggingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.apiLogger = logging.getLogger('api')
    def __call__(self, request):
        try:
            body = json.loads(request.body)
        except Exception:
            body = dict()
        body.update(dict(request.POST))
        response = self.get_response(request)
        ip=getIP(request)
        if request.method != 'GET':
            self.apiLogger.info("{} {} {} {} {} {}".format(
                request.user, request.method, request.path, body,
                response.status_code, response.reason_phrase))
        else:
            self.apiLogger.info("{} {} {} {}".format(request.user,ip,request.method,request.path))

        return response
