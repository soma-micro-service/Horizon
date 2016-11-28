# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from django.http import HttpResponse
from django.views.generic import View

from horizon import views
from horizon.utils.lazy_encoder import LazyTranslationEncoder
import pykube
import requests
import json
import urlparse
import time

#pykube api
pykubeapi = pykube.HTTPClient(pykube.KubeConfig.from_file("~/.kube/config"))

class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'project/appprocess/index.html'
    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        # jenkins, pykube, magnum info pass
        print(context)
        return context


class JSONView(View):
    def get(self, request, *args, **kwargs):
        phase = 1  # Checkin, Build, Test, Provisioning, run
        jenkinsUrl = 'http://172.16.100.55:6680/job/app/lastBuild/consoleText'
        print("======================")
        print(jenkinsUrl)
        print("======================")
        jenkins = requests.get(jenkinsUrl).text
        pods = pykube.Pod.objects(pykubeapi).filter(namespace="default").execute().json()['items']
        podAllStatus = True

        if '[Docker] INFO: Creating docker image from' in jenkins:
            phase = 2
            if 'Done pushing image' in jenkins:
                phase = 3
                for pod in pods:
                    if pod['status']['phase'] != 'Running':
                        podAllStatus = False
                if podAllStatus == False:
                    phase = 4
                else:
                    phase = 5

        if 'Finished: FAILURE' in jenkins:
            phase = 6






        data = {
            'jenkins': jenkins,
            'pods': pods,
            'phase': phase
        }

        json_string = json.dumps(data, cls=LazyTranslationEncoder,
                                 ensure_ascii=False)
        return HttpResponse(json_string, content_type='text/json')

