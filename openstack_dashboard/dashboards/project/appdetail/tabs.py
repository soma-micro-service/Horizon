from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.project.appdetail import tables

import operator
import pykube
import json

#pykube api
pykubeapi = pykube.HTTPClient(pykube.KubeConfig.from_file("~/.kube/config"))


class PodTab(tabs.TableTab):
    name = _("Pod")
    slug = "pod_tab"
    table_classes = (tables.AppTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_instances_data(self):
        try:
            marker = self.request.GET.get(
                        tables.AppTable._meta.pagination_param, None)

            instances, self._has_more = api.nova.server_list(
                self.request,
                search_opts={'marker': marker, 'paginate': True})

            pods = self._get_pods()
            print("===============pods=================")
            print(pods)
            print("================================")
            return pods
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []

    def _get_pods(self):
        try:
            res = pykube.Pod.objects(pykubeapi).filter(namespace="default").execute().json()
            if res:
                return res['items']
        except Exception:
            print("ecept")
            return []

class ServiceTab(tabs.TableTab):
    name = _("Service")
    slug = "service_tab"
    table_classes = (tables.AppTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_instances_data(self):
        try:
            marker = self.request.GET.get(
                        tables.AppTable._meta.pagination_param, None)

            instances, self._has_more = api.nova.server_list(
                self.request,
                search_opts={'marker': marker, 'paginate': True})

            services = self._get_services()
            print("=============services===================")
            print(services)
            print("================================")
            print("=============instance===================")
            print(instances)
            print("================================")

            return services
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []

    def _get_services(self):
        try:
            res = pykube.Service.objects(pykubeapi).filter(namespace="default").execute().json()
            if res:
                #print(json.dumps(res['items'], sort_keys=True, indent=4, separators=(',', ': ')))
                return res['items']
        except Exception:
            print("Error")
            return []

class RCControllerTab(tabs.TableTab):
    name = _("Replication Controller")
    slug = "rccontroller_tab"
    table_classes = (tables.AppTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_instances_data(self):
        try:
            marker = self.request.GET.get(
                        tables.AppTable._meta.pagination_param, None)

            instances, self._has_more = api.nova.server_list(
                self.request,
                search_opts={'marker': marker, 'paginate': True})
            rccontroller = self._get_replication_controllers()
            print("================rccontrollers================")
            print(rccontroller)
            print("================================")
            return rccontroller
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []

    def _get_replication_controllers(self):
        try:
            res = pykube.ReplicationController.objects(pykubeapi).filter(namespace="default").execute().json()
            if res:
                return json.dump(res['items'])
        except Exception:
            print("Error")
            return []

class AppDetailTabs(tabs.TabGroup):
    slug = "appdetail_tabs"
    tabs = (PodTab, ServiceTab, RCControllerTab)
    sticky = True
