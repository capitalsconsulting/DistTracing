from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view, renderer_classes
import json
import pysftp
from django.conf import settings
from background_task import background

Hostname = "bbonesource.blob.core.windows.net"
Username = "bbonesource.sftponesource"
Password = "K12X06IzJucyBqpfi76GgdV3v4fSZQHi"



@api_view(['GET'])
def getSftpFileList(request):
    return JsonResponse({'result': 0})