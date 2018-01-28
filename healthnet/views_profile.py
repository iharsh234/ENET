from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from healthnet.forms import PasswordForm, ProfileForm, EmployeeProfileForm, ScoreForm
from healthnet.models import Action, Account, Message, Score
from healthnet import views
from healthnet import appointment
from healthnet import logger
from healthnet import message


def profile_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    if request.user.account.role != Account.ACCOUNT_ADMIN:
        appointment.parse_appointment_cancel(request, template_data)  # Parse appointment cancelling
        template_data['events'] = appointment.parse_appointments(request)  # Build list of appointments
    else:
        template_data['total_logins'] = Action.objects.filter(description__icontains="Account login").count()
        template_data['total_logouts'] = Action.objects.filter(description__icontains="Account logout").count()
        template_data['total_admitted'] = Action.objects.filter(description__icontains="Admitted Patient").count()
        template_data['total_discharged'] = Action.objects.filter(description__icontains="Discharged Patient").count()
        template_data['total_appointments'] = Action.objects.filter(description__icontains="Appointment created").count()
        template_data['total_med_tests'] = Action.objects.filter(description__icontains="Medical Test created").count()
        template_data['total_registered'] = Action.objects.filter(description__icontains="registered").count()
    message.parse_message_archive(request, template_data)
    #template_data['messages'] = Message.objects.filter(target=request.user.account, target_deleted=False)
    template_data['messages'] = Score.objects.filter(owner=request.user.account)

    return render(request, 'healthnet/profile.html', template_data)

###########

def list_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(
        request,
        [Account.ACCOUNT_PATIENT, Account.ACCOUNT_NURSE, Account.ACCOUNT_DOCTOR,Account.ACCOUNT_ADMIN]
    )
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    #appointment.parse_appointment_cancel(request, template_data)  # Parse appointment cancelling
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        template_data['query'] = Score.objects.filter(owner=request.user.account)
    elif request.user.account.role == Account.ACCOUNT_ADMIN:
        from django.db.models import Avg
        #import pdb; pdb.set_trace()
        template_data['query'] = Score.objects.all().values('owner').annotate(score=Avg('score'))
        template_data['query'] = [{'owner':Account.objects.get(pk=id['owner']),'score':int(id['score'])} for id in template_data['query']]
        return render(request, 'healthnet/medtest/list_score_admin.html', template_data)
    else:
        template_data['query'] = Score.objects.all()
    return render(request, 'healthnet/medtest/list_score.html', template_data)

def new_view(request):
    # Authentication check.
    #import pdb; pdb.set_trace()
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(
        request,
        {'form_button': "Send Score"}
    )
    # Proceed with the rest of the view
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score = form.generate()
            score.save()
            #logger.log(Action.ACTION_MESSAGE, 'Message sent', request.user.account)
            request.session['alert_success'] = "Successfully sent your score!"
            return HttpResponseRedirect('/score/list/')
    else:
        # Validation Check. Make sure a message exists for the given pk.
        default = {}
        if 'pk' in request.GET:
            pk = request.GET['pk']
            try:
                account = Account.objects.get(pk=pk)
                default['target'] = pk
            except Exception:
                template_data['alert_danger'] = "We couldn't find the person you're replying to. Please try again.."

        form = ScoreForm(default)
        form.clear_errors()
    template_data['form'] = form
    return render(request, 'healthnet/message/new_score.html', template_data)

###################

def password_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': "Change password"})
    # Proceed with the rest of the view
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username, password=form.cleaned_data['password_current'])
            if user is None:
                form.mark_error('password_current', 'Incorrect password')
            else:
                user = request.user
                user.set_password(form.cleaned_data['password_first'])
                user.save()
                logger.log(Action.ACTION_ACCOUNT, "Account password change", request.user.account)
                form = PasswordForm()  # Clean the form when the page is redisplayed
                template_data['alert_success'] = "Your password has been changed!"
    else:
        form = PasswordForm()
    template_data['form'] = form
    return render(request, 'healthnet/profile/password.html', template_data)


def update_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    # Get the template data from the asession
    template_data = views.parse_session(request, {'form_button': "Update profile"})
    # Proceed with the rest of the view
    profile = request.user.account.profile
    if request.method == 'POST':
        if request.user.account.role != Account.ACCOUNT_PATIENT:
            form = EmployeeProfileForm(request.POST)
        else:
            form = ProfileForm(request.POST)
        if form.is_valid():
            form.assign(profile)
            profile.save()
            logger.log(Action.ACTION_ACCOUNT, "Account updated info", request.user.account)
            template_data['alert_success'] = "Your profile has been updated!"
    else:
        if request.user.account.role != Account.ACCOUNT_PATIENT:
            form = EmployeeProfileForm(profile.get_populated_fields())
        else:
            form = ProfileForm(profile.get_populated_fields())
    template_data['form'] = form
    return render(request, 'healthnet/profile/update.html', template_data)














### CHART OF PROGRESS

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from chartit import DataPool, Chart

# class LineChartView(TemplateView):
#     template_name = 'line.html'
#     #import pdb; pdb.set_trace()
#     def get_ds(self):
#         return DataPool(
#             series=[{'options': {
#                 'source': Score.objects.all()},
#                 'terms': [
#                 'game',
#                 'score',
#                 'updated']}
#             ])
#
#     def get_water_chart(self):
#         return Chart(
#             datasource=self.get_ds(),
#             series_options=[{'options': {
#                 'type': 'line',
#                 'stacking': False},
#                 'terms': {
#                 'updated': [
#                     'game',
#                     'score']
#             }}],
#             chart_options={'title': {
#                 'text': 'User Game Data of Lazy eye HTS'},
#                 'xAxis': {
#                 'title': {
#                     'text': 'Time at play'}}})
#
#     def get_context_data(self, **kwargs):
#         context = super(LineChartView, self).get_context_data(**kwargs)
#         context['weatherchart'] = self.get_water_chart()
#         #import pdb; pdb.set_trace()
#         return context




from datetime import datetime
def chart_view(request):
    authentication_result = views.authentication_check(
        request,
        [Account.ACCOUNT_PATIENT, Account.ACCOUNT_NURSE, Account.ACCOUNT_DOCTOR, Account.ACCOUNT_ADMIN]
    )
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    #template_data = dict()
    # Proceed with the rest of the view
    #appointment.parse_appointment_cancel(request, template_data)  # Parse appointment cancelling
    if request.user.account.role == Account.ACCOUNT_PATIENT:
        score = Score.objects.filter(owner=request.user.account)
    else:
        score = Score.objects.all()
    GAME = ''
    tle = 'User Game Data'
    #from django.core.urlresolvers import resolve
    try:current_url = request.session['owner']#resolve(request.path_info).url_name
    except:current_url=None
    #import pdb; pdb.set_trace()

    if request.method == 'GET' and 'q' in request.GET:
        q = request.GET['q']
        if q is not None:
            score = score.filter(game=q)
            GAME = q
            tle = 'User Game data in game %s' %(q)
    if current_url:
        q = current_url
        score = score.filter(owner=q)

    d = DataPool(
            series=[{'options': {
                'source': score},
                'terms': [
                'score',
                'updated']}
            ])
    #import pdb; pdb.set_trace()
    chat = Chart(
            datasource=d,
            series_options=[{'options': {
                'type': 'line',
                'stacking': False},
                'terms': {
                'updated': [
                    #'game',
                    'score']
            }}],
            chart_options={'title': {
                'text': tle},
                'xAxis': {
                'title': {
                    'text': 'Time at play'}
                    }
                    },
                x_sortf_mapf_mts=(None, lambda i: (i).strftime("%d/%m"), False))

    #import pdb; pdb.set_trace()
    #template_data['weatherchart'] = chat
    return render(request, 'line.html', {'weatherchart':chat})
