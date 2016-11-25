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

class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'project/appprocess/index.html'
    asdasd = "asdsad"
    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        # jenkins, pykube, magnum info pass
        print(context)
        return context


class JSONView(View):
    def get(self, request, *args, **kwargs):
        r = requests.get('http://172.16.100.55:6680/job/hajin/lastBuild/api/json')

        data = {
            'jenkins': r.json(),
            'networks': 'asd',
        }

        json_string = json.dumps(data, cls=LazyTranslationEncoder,
                                 ensure_ascii=False)
        return HttpResponse(json_string, content_type='text/json')

