import traceback

from horizon import workflows, forms, exceptions
from django.utils.translation import ugettext_lazy as _

from openstack_dashboard.dashboards.project.appcluster import util


class SetCreateClusterDetailsAction(workflows.Action):
    name = forms.CharField(
        label=_("App Cluster Name"),
        required=True,
        max_length=80,
        help_text=_("Name"))

    git = forms.CharField(
        label=_("Github Url"),
        required=True,
        max_length=120,
        help_text=_("Github Url"))

    servicename = forms.CharField(
        label=_("Service Name"),
        required=True,
        max_length=120,
        help_text=_("Service Name"))

    languagePack = forms.ThemableChoiceField(
        label=_("LanguagePack"),
        required=True)

    languagePack.choices = ([
                    ('node','Node.js'),
                    ('django','Django')
                ])

    port = forms.IntegerField(
        label=_("Port"),
        required=True,
        min_value=1,
        max_value=65535,
        help_text=_("Port"))

    test = forms.BooleanField(
        label=_("Test"),
        required=False,
        help_text=_("Test"))

    devmode = forms.BooleanField(
        label=_("Dev Mode"),
        required=False,
        help_text=_("Dev Mode"))

    class Meta:
        name = _("Details")

    def __init__(self, request, context, *args, **kwargs):
        self.request = request
        self.context = context
        super(SetCreateClusterDetailsAction, self).__init__(
            request, context, *args, **kwargs)

class SetCreateClusterDetails(workflows.Step):
    action_class = SetCreateClusterDetailsAction
    contributes = ("name", "git", "servicename", "languagePack", "port", "test", "devmode")

    def contribute(self, data, context):
        if data:
            context['name'] = data.get("name", "")
            context['git'] = data.get("git", "")
            context['servicename'] = data.get("servicename", "")
            context['languagePack'] = data.get("languagePack", "")
            context['port'] = data.get("port", "")
            context['test'] = data.get("test", "")
            context['devmode'] = data.get("devmode", "")
        return context


class CreateCluster(workflows.Workflow):
    slug = "add"
    name = _("Create App Cluster")
    finalize_button_name = _("Add")
    success_message = _('Created app cluster "%s".')
    failure_message = _('Unable to create App cluster "%s".')
    success_url = "horizon:project:appprocess:index"
    failure_url = "horizon:project:appcluster:index"
    default_steps = (SetCreateClusterDetails,)

    def format_status_message(self, message):
        return message % self.context.get('name', 'unknown provider')

    def handle(self, request, context):
        try:
            print("=========================================")
            print(request)
            util.create_appCluster(self, request, context)
            #util.addProvider(self, request, context)
            return True
        except Exception:
            print traceback.format_exc()
            exceptions.handle(request, _("Unable to add provider"))
            return False
