from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect

from healthnet import logger
from healthnet.forms import PrescriptionForm
from healthnet.models import Account, Prescription, Action
from healthnet import views


def create_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(
        request,
        [Account.ACCOUNT_DOCTOR]
    )
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': "Add Prescription"})
    default = {}
    if request.user.account.role == Account.ACCOUNT_DOCTOR:
        default['doctor'] = request.user.account.pk
    if 'date' not in request.POST:
        default['date'] = datetime.now().strftime("%Y-%m-%d")
    request.POST._mutable = True
    request.POST.update(default)
    form = PrescriptionForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            pres = Prescription(
                patient=form.cleaned_data['patient'],
                doctor=form.cleaned_data['doctor'],
                date=form.cleaned_data['date'],
                medication=form.cleaned_data['medication'],
                strength=form.cleaned_data['strength'],
                instruction=form.cleaned_data['instruction'],
                refill=form.cleaned_data['refill'],
            )
            pres.save()
            logger.log(Action.ACTION_PRESCRIPTION, 'Prescription Created', request.user.account)
            form = PrescriptionForm(default)  # Clean the form when the page is redisplayed
            form._errors = {}
            request.session['alert_success'] = "Successfully added the prescription."
            return HttpResponseRedirect('/prescription/list/')
    else:
        form._errors = {}
    if request.user.account.role == Account.ACCOUNT_DOCTOR:
        form.disable_field('doctor')
        form.date = datetime.today()
    template_data['form'] = form
    return render(request, 'healthnet/prescription/create.html', template_data)


def list_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(
        request,
        [Account.ACCOUNT_DOCTOR, Account.ACCOUNT_NURSE, Account.ACCOUNT_PATIENT]
    )
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    if request.method == 'POST':
        if 'delete' in request.POST and 'pk' in request.POST:
            pk = request.POST['pk']
            try:
                prescription = Prescription.objects.get(pk=pk)
                prescription.active = False
                prescription.save()
                logger.log(Action.ACTION_PRESCRIPTION, 'Prescription Cancelled', request.user.account)
                template_data['alert_success'] = "The prescription has been deleted."
            except Exception:
                template_data['alert_danger'] = "Unable to delete the prescription. Please try again later."
    if request.user.account.role == Account.ACCOUNT_DOCTOR:
        prescriptions = Prescription.objects.filter(doctor=request.user.account)
    elif request.user.account.role == Account.ACCOUNT_PATIENT:
        prescriptions = Prescription.objects.filter(patient=request.user.account)
    else:
        prescriptions = Prescription.objects.all()
    template_data['query'] = prescriptions.order_by('date')
    return render(request, 'healthnet/prescription/list.html', template_data)