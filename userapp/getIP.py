import time
import requests
import json

def getIP(request):
    with open("/public/Users/siteusr/website/Dmtrack2/log/META.log","a") as w:
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

