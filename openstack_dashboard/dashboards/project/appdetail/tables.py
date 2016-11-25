from django.utils.translation import ugettext_lazy as _

from horizon import tables
import json


def get_name(device):
    if device['metadata']:
        name = device['metadata']['name']
        return name
    else:
        return _("Not available")


def get_uid(device):
    if device['metadata']:
        name = device['metadata']['uid']
        return name
    return _("Not available")

def get_status(device):
    if device['status']:
        if hasattr(device['status'], 'phase'):
            return device['status']['phase']
        else:
            return "Running"
    else:
        return _("Not available")
    #service
    #pod
    #rc


def get_cluster_ip(device):
    if device['spec']:
        name = device['spec']['clusterIP']
        return name
    return _("Not available")

class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class AppTable(tables.DataTable):
    name = tables.Column(get_name, \
                         verbose_name=_("NAME"))

    uid = tables.Column(get_uid, \
                           verbose_name=_("UID"))

    #clusterip = tables.Column(get_cluster_ip, verbose_name=_("CLUSTER IP"))

    status = tables.Column(get_status, \
                         verbose_name=_("STATUS"))
    '''
    image_name = tables.Column('image_name', \
                               verbose_name=_("Image Name"))
    '''


    def get_object_id(self, datum):
        return datum['metadata']['uid']

    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        table_actions = (MyFilterAction,)
