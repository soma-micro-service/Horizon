import traceback
import time
from time import mktime
from datetime import datetime
from requests.auth import HTTPBasicAuth

from django.template.defaultfilters import register
from django.utils.translation import ugettext_lazy as _
import requests

from horizon import exceptions
import yaml
import os
import xml.etree.ElementTree as ET
from os.path import expanduser

requests.packages.urllib3.disable_warnings()

create_cluster_url = "https://localhost:8443/rest"
json_headers = {'Accept': 'application/json'}


class Provider:
    """
    Provider data
    """

    def __init__(self, id, name, description, hostname, port, timeout, secured):
        self.id = id
        self.name = name
        self.description = description
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self.secured = secured


def getProviders(self):
    try:
        r = requests.get(create_cluster_url + "/providers", verify=False, auth=HTTPBasicAuth('admin', 'integra'),
                         headers=json_headers)

        providers = []
        for provider in r.json()['providers']:
            providers.append(
                Provider(provider[u'id'], provider[u'name'], provider[u'description'], provider[u'hostname'],
                         provider[u'port'], provider[u'timeout'], provider[u'secured']))

        return providers

    except:
        exceptions.handle(self.request,
                          _('Unable to get providers'))
        return []

# request - horizon environment settings
# context - user inputs from form
def create_appCluster(self, request, context):
    try:
        name = context.get('name')
        git = context.get('git')
        servicename = context.get('servicename')
        languagePack = context.get('languagePack')
        port = context.get('port')
        test = context.get('test')
        devmode = context.get('devmode')

        print(languagePack)
        print("====================")
        # parse xml file
        doc = ET.parse('config.xml')
        # get root node
        root = doc.getroot()
        scm_tag = root.find("scm")
        builders_tag = root.find("builders")
        jenkins_tag = builders_tag.findall("org.jenkinsci.plugins.dockerbuildstep.DockerBuilder")[2]

        #example) https://github.com/soma-micro-service/simple_django.git
        for url in scm_tag.iter("url"):
            url.text = str(git)
            #print("=========")

        #example) cp ~/Dockerfiles/python/Dockerfile $WORKSPACE/
        #example) cp ~/Dockerfiles/node/Dockerfile $WORKSPACE/
        for command in builders_tag.iter("command"):
            if str(languagePack) == "django":
                command.text = "cp ~/Dockerfiles/django/Dockerfile $WORKSPACE/"
            else:
                command.text = "cp ~/Dockerfiles/node/Dockerfile $WORKSPACE/"

        #example) simple-django-app
        for containerIds in jenkins_tag.iter("containerIds"):
            containerIds.text = str(name)
            #print(containerIds.text)

        home = expanduser("~")
        doc.write(str(home) + "/ansible-vm1/files/config.xml", encoding="utf-8")

        '''
        fh = open('example.yaml', 'r')
        yam = yaml.load(fh)
        print('')
        print(yam)
        '''
    except:
        print "Exception inside util.Create cluster"
        print traceback.format_exc()
        exceptions.handle(self.request,
                          _('Unable to create a cluster cluster'))
        return []
# request - horizon environment settings
# context - user inputs from form
def addProvider(self, request, context):
    try:

        name = context.get('name')
        description = context.get('description')
        hostname = context.get('hostname')
        port = context.get('port')
        timeout = context.get('timeout')
        secured = context.get('secured')

        payload = {'name': name, 'description': description, 'hostname': hostname, 'port': port, 'timeout': timeout,
                   'secured': secured}
        requests.post(integra_url + "/providers", json=payload, verify=False, auth=HTTPBasicAuth('admin', 'integra'),
                      headers=json_headers)

    except:
        print "Exception inside utils.addProvider"
        print traceback.format_exc()
        exceptions.handle(self.request,
                          _('Unable to add provider'))
        return []


# id is required for table
def deleteProvider(self, id):
    try:

        requests.delete(integra_url + "/providers/" + id, verify=False, auth=HTTPBasicAuth('admin', 'integra'),
                        headers=json_headers)

    except:
        print "Exception inside utils.deleteProvider"
        print traceback.format_exc()
        exceptions.handle(self.request,
                          _('Unable to delete provider'))
        return False


def getProviders(self):
    try:

        r = requests.get(integra_url + "/providers", verify=False, auth=HTTPBasicAuth('admin', 'integra'),
                         headers=json_headers)

        providers = []
        for provider in r.json()['providers']:
            providers.append(ProviderAction(provider[u'id'], provider[u'name'], provider[u'description']))

        return providers

    except:
        exceptions.handle(self.request,
                          _('Unable to retrieve list of posts.'))
        return []


def getProviderActions(self):
    try:

        r = requests.get(integra_url + "/provider_actions/" + id, verify=False, auth=HTTPBasicAuth('admin', 'integra'),
                         headers=json_headers)

        providerActions = []
        for providerAction in r.json()['providerActions']:
            providerActions.append(
                ProviderAction(providerAction[u'id'], providerAction[u'name'], providerAction[u'description']))

        return providerActions

    except:
        exceptions.handle(self.request,
                          _('Unable to retrieve list of posts.'))
        return []
