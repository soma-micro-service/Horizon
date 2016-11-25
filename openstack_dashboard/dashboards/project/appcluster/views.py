# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2013 NTT MCL Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import six

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse  # noqa
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View  # noqa

from horizon import exceptions
from horizon import tabs
from horizon import tables, workflows, forms
from horizon.utils.lazy_encoder import LazyTranslationEncoder

from openstack_dashboard import api
from openstack_dashboard.dashboards.project.appcluster.instances \
    import tables as instances_tables
from openstack_dashboard.dashboards.project.appcluster.networks \
    import tables as networks_tables
from openstack_dashboard.dashboards.project.appcluster.ports \
    import tables as ports_tables
from openstack_dashboard.dashboards.project.appcluster.routers \
    import tables as routers_tables
from openstack_dashboard.dashboards.project.appcluster.subnets \
    import tables as subnets_tables
from openstack_dashboard.dashboards.project.appcluster \
    import tabs as topology_tabs
from openstack_dashboard.dashboards.project.appcluster import utils

from openstack_dashboard.dashboards.project.instances import\
    console as i_console
from openstack_dashboard.dashboards.project.instances.tables import \
    STATUS_DISPLAY_CHOICES as instance_choices
from openstack_dashboard.dashboards.project.instances import\
    views as i_views
from openstack_dashboard.dashboards.project.instances.workflows import\
    create_instance as i_workflows
from openstack_dashboard.dashboards.project.networks.subnets import\
    views as s_views
from openstack_dashboard.dashboards.project.networks.subnets import\
    workflows as s_workflows
from openstack_dashboard.dashboards.project.networks.tables import \
    DISPLAY_CHOICES as network_display_choices
from openstack_dashboard.dashboards.project.networks.tables import \
    STATUS_DISPLAY_CHOICES as network_choices
from openstack_dashboard.dashboards.project.networks import\
    views as n_views
from openstack_dashboard.dashboards.project.networks import\
    workflows as n_workflows
from openstack_dashboard.dashboards.project.routers.ports.tables import \
    DISPLAY_CHOICES as ports_choices
from openstack_dashboard.dashboards.project.routers.ports.tables import \
    STATUS_DISPLAY_CHOICES as ports_status_choices
from openstack_dashboard.dashboards.project.routers.ports import\
    views as p_views
from openstack_dashboard.dashboards.project.routers.tables import \
    ADMIN_STATE_DISPLAY_CHOICES as routers_admin_choices
from openstack_dashboard.dashboards.project.routers.tables import \
    STATUS_DISPLAY_CHOICES as routers_status_choices
from openstack_dashboard.dashboards.project.routers import\
    views as r_views

from openstack_dashboard.dashboards.project.appcluster import utils

from openstack_dashboard.dashboards.project.appcluster.workflows.create_cluster import CreateCluster
from openstack_dashboard.dashboards.project.appdetail import views as d_views

import operator
import pykube

# List of known server statuses that wont connect to the console
console_invalid_status = {
    'shutoff', 'suspended', 'resize', 'verify_resize',
    'revert_resize', 'migrating', 'build', 'shelved',
    'shelved_offloaded'}

#pykube api
pykubeapi = pykube.HTTPClient(pykube.KubeConfig.from_file("~/.kube/config"))


class CreateClusterView(workflows.WorkflowView):
    workflow_class = CreateCluster

    def get_initial(self):
        initial = super(CreateClusterView, self).get_initial()
        return initial

class TranslationHelper(object):
    """Helper class to provide the translations of instances, networks,
    routers and ports from other parts of the code to the network topology
    """
    def __init__(self):
        # turn translation tuples into dicts for easy access
        self.instance = dict(instance_choices)
        self.network = dict(network_choices)
        self.network.update(dict(network_display_choices))
        self.router = dict(routers_admin_choices)
        self.router.update(dict(routers_status_choices))
        self.port = dict(ports_choices)
        self.port.update(dict(ports_status_choices))
        # and turn all the keys into Uppercase for simple access
        self.instance = {k.upper(): v for k, v in six.iteritems(self.instance)}
        self.network = {k.upper(): v for k, v in six.iteritems(self.network)}
        self.router = {k.upper(): v for k, v in six.iteritems(self.router)}
        self.port = {k.upper(): v for k, v in six.iteritems(self.port)}


class NTAddInterfaceView(p_views.AddInterfaceView):
    success_url = "horizon:project:appcluster:index"
    failure_url = "horizon:project:appcluster:index"

    def get_success_url(self):
        return reverse("horizon:project:appcluster:index")

    def get_context_data(self, **kwargs):
        context = super(NTAddInterfaceView, self).get_context_data(**kwargs)
        context['form_url'] = 'horizon:project:appcluster:interface'
        return context

class NTCreateRouterView(r_views.CreateView):
    template_name = 'project/appcluster/create_router.html'
    success_url = reverse_lazy("horizon:project:appcluster:index")
    page_title = _("Create a Router")

'''
class LaunchLink(tables.LinkAction):
    name = "launch"
    verbose_name = _("Launch Instance")
    url = "horizon:project:instances:launch"
    classes = ("ajax-modal", "btn-launch")
    icon = "cloud-upload"
    policy_rules = (("compute", "compute:create"),)
    ajax = True
'''

class NTCreateNetwork(n_workflows.CreateNetwork):
    def get_success_url(self):
        return reverse("horizon:project:appcluster:index")

    def get_failure_url(self):
        return reverse("horizon:project:appcluster:index")


class NTCreateNetworkView(n_views.CreateView):
    workflow_class = NTCreateNetwork


class NTLaunchInstance(i_workflows.LaunchInstance):
    success_url = "horizon:project:appcluster:index"


class NTLaunchInstanceView(i_views.LaunchInstanceView):
    workflow_class = NTLaunchInstance


class NTCreateSubnet(s_workflows.CreateSubnet):
    def get_success_url(self):
        return reverse("horizon:project:appcluster:index")

    def get_failure_url(self):
        return reverse("horizon:project:appcluster:index")


class NTCreateSubnetView(s_views.CreateView):
    workflow_class = NTCreateSubnet


class InstanceView(i_views.IndexView):
    table_class = instances_tables.InstancesTable
    template_name = 'project/appcluster/iframe.html'


class RouterView(r_views.IndexView):
    table_class = routers_tables.RoutersTable
    template_name = 'project/appcluster/iframe.html'


class NetworkView(n_views.IndexView):
    table_class = networks_tables.NetworksTable
    template_name = 'project/appcluster/iframe.html'

class AppDetailView(d_views.IndexView):
    #table_class = networks_tables.NetworksTable
    template_name = 'project/appdetail/index.html'


class RouterDetailView(r_views.DetailView):
    table_classes = (ports_tables.PortsTable, )
    template_name = 'project/appcluster/iframe.html'

    def get_interfaces_data(self):
        pass


class NetworkDetailView(n_views.DetailView):
    table_classes = (subnets_tables.SubnetsTable, )
    template_name = 'project/appcluster/iframe.html'


class NetworkTopologyView(tabs.TabView):
    tab_group_class = topology_tabs.TopologyTabs
    template_name = 'project/appcluster/index.html'
    page_title = _("App Cluster Topology")

    def get_context_data(self, **kwargs):
        context = super(NetworkTopologyView, self).get_context_data(**kwargs)
        return utils.get_context(self.request, context)


class JSONView(View):
    trans = TranslationHelper()

    @property
    def is_router_enabled(self):
        network_config = getattr(settings, 'OPENSTACK_NEUTRON_NETWORK', {})
        return network_config.get('enable_router', True)

    def add_resource_url(self, view, resources):
        tenant_id = self.request.user.tenant_id
        for resource in resources:
            if (resource.get('tenant_id')
                    and tenant_id != resource.get('tenant_id')):
                continue
            resource['url'] = reverse(view, None, [str(resource['id'])])

    def _check_router_external_port(self, ports, router_id, network_id):
        for port in ports:
            if (port['network_id'] == network_id
                    and port['device_id'] == router_id):
                return True
        return False

    def _get_servers(self, request):
        # Get nova data
        try:
            servers, more = api.nova.server_list(request)
        except Exception:
            servers = []
        data = []
        console_type = getattr(settings, 'CONSOLE_TYPE', 'AUTO')
        # lowercase of the keys will be used at the end of the console URL.
        for server in servers:
            server_data = {'name': server.name,
                           'status': self.trans.instance[server.status],
                           'original_status': server.status,
                           'task': getattr(server, 'OS-EXT-STS:task_state'),
                           'id': server.id}
            # Avoid doing extra calls for console if the server is in
            # a invalid status for console connection
            if server.status.lower() not in console_invalid_status:
                try:
                    console = i_console.get_console(
                        request, console_type, server)[0].lower()
                    server_data['console'] = console
                except exceptions.NotAvailable:
                    pass

            data.append(server_data)
        self.add_resource_url('horizon:project:instances:detail', data)
        return data

    def _get_networks(self, request):
        # Get neutron data
        # if we didn't specify tenant_id, all networks shown as admin user.
        # so it is need to specify the networks. However there is no need to
        # specify tenant_id for subnet. The subnet which belongs to the public
        # network is needed to draw subnet information on public network.
        try:
            neutron_networks = api.neutron.network_list_for_tenant(
                request,
                request.user.tenant_id)
        except Exception:
            neutron_networks = []
        networks = []
        for network in neutron_networks:
            obj = {'name': network.name_or_id,
                   'id': network.id,
                   'subnets': [{'id': subnet.id,
                                'cidr': subnet.cidr}
                               for subnet in network.subnets],
                   'status': self.trans.network[network.status],
                   'original_status': network.status,
                   'router:external': network['router:external']}
            self.add_resource_url('horizon:project:networks:subnets:detail',
                                  obj['subnets'])
            networks.append(obj)

        # Add public networks to the networks list
        if self.is_router_enabled:
            try:
                neutron_public_networks = api.neutron.network_list(
                    request,
                    **{'router:external': True})
            except Exception:
                neutron_public_networks = []
            my_network_ids = [net['id'] for net in networks]
            for publicnet in neutron_public_networks:
                if publicnet.id in my_network_ids:
                    continue
                try:
                    subnets = []
                    for subnet in publicnet.subnets:
                        snet = {'id': subnet.id,
                                'cidr': subnet.cidr}
                        self.add_resource_url(
                            'horizon:project:networks:subnets:detail', snet)
                        subnets.append(snet)
                except Exception:
                    subnets = []
                networks.append({
                    'name': publicnet.name_or_id,
                    'id': publicnet.id,
                    'subnets': subnets,
                    'status': self.trans.network[publicnet.status],
                    'original_status': publicnet.status,
                    'router:external': publicnet['router:external']})

        self.add_resource_url('horizon:project:networks:detail',
                              networks)

        return sorted(networks,
                      key=lambda x: x.get('router:external'),
                      reverse=True)

    def _get_routers(self, request):
        if not self.is_router_enabled:
            return []
        try:
            neutron_routers = api.neutron.router_list(
                request,
                tenant_id=request.user.tenant_id)
        except Exception:
            neutron_routers = []

        routers = [{'id': router.id,
                    'name': router.name_or_id,
                    'status': self.trans.router[router.status],
                    'original_status': router.status,
                    'external_gateway_info': router.external_gateway_info}
                   for router in neutron_routers]
        self.add_resource_url('horizon:project:routers:detail', routers)
        return routers

    def _get_ports(self, request, networks):
        try:
            neutron_ports = api.neutron.port_list(request)
        except Exception:
            neutron_ports = []

        # we should filter out ports connected to non tenant networks
        # which they have no visibility to
        tenant_network_ids = [network['id'] for network in networks]
        ports = [{'id': port.id,
                  'network_id': port.network_id,
                  'device_id': port.device_id,
                  'fixed_ips': port.fixed_ips,
                  'device_owner': port.device_owner,
                  'status': self.trans.port[port.status],
                  'original_status': port.status}
                 for port in neutron_ports
                 if port.device_owner != 'network:router_ha_interface'
                 and port.network_id in tenant_network_ids]
        self.add_resource_url('horizon:project:networks:ports:detail',
                              ports)
        return ports

    def _prepare_gateway_ports(self, routers, ports):
        # user can't see port on external network. so we are
        # adding fake port based on router information
        for router in routers:
            external_gateway_info = router.get('external_gateway_info')
            if not external_gateway_info:
                continue
            external_network = external_gateway_info.get(
                'network_id')
            if not external_network:
                continue
            if self._check_router_external_port(ports,
                                                router['id'],
                                                external_network):
                continue
            fake_port = {'id': 'gateway%s' % external_network,
                         'network_id': external_network,
                         'device_id': router['id'],
                         'fixed_ips': []}
            ports.append(fake_port)

    def _get_pods(slef, request):
        try:
            res = pykube.Pod.objects(pykubeapi).filter(namespace="default").execute().json()
            print("==============================getPods========================")
            print(res)
            if res:
                return res['items']
        except Exception, e:
            print("==============================getPods Exception========================")
            print(e)
            return []


    def _get_services(slef, request):
        try:
            res = pykube.Service.objects(pykubeapi).filter(namespace="default").execute().json()
            if res:
                return res['items']
        except Exception, e:
            print("==============================getService Exception========================")
            print(e)
            return []

    def _get_replication_controllers(slef, request):
        try:
            res = pykube.ReplicationController.objects(pykubeapi).filter(namespace="default").execute().json()
            if res:
                return res['items']
        except Exception, e:
            print("==============================rccontroller Exception========================")
            print(e)
            return []

    def get(self, request, *args, **kwargs):
        networks = self._get_networks(request)
        data = {'servers': self._get_servers(request),
                'networks': networks,
                'ports': self._get_ports(request, networks),
                'routers': self._get_routers(request),
                'pods': self._get_pods(request),
                'services': self._get_services(request),
                'replicationController': self._get_replication_controllers(request),
                }
        self._prepare_gateway_ports(data['routers'], data['ports'])
        json_string = json.dumps(data, cls=LazyTranslationEncoder,
                                 ensure_ascii=False)
        return HttpResponse(json_string, content_type='text/json')
