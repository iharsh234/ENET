from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings

from healthnet import views
from healthnet import views_admin
from healthnet import views_admission
from healthnet import views_appointment
from healthnet import views_home
from healthnet import views_medtest
from healthnet import views_message
from healthnet import views_prescription
from healthnet import views_profile
from healthnet import views_medicalInfo

from rest_framework import routers
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from healthnet.api import ScoreAPI, UserAPI, GetAuthToken
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'scores', views.ScoreViewSet)
from rest_framework.authtoken import views as vw



urlpatterns = patterns(
    '',
    url(r'^$', views_home.login_view, name='index'),
    url(r'^logout/$', views_home.logout_view, name='logout'),
    url(r'^register/$', views_home.register_view, name='register'),
    url(r'^setup/$', views_home.setup_view, name='setup'),

    url(r'^error/denied/$', views_home.error_denied_view, name='error/denied'),

    url(r'^admin/users/$', views_admin.users_view, name='admin/users'),
    url(r'^admin/users_doctor/$', views_admin.users_view_doctor, name='admin/users_doctor'),
    url(r'^admin/activity/$', views_admin.activity_view, name='admin/activity'),
    url(r'^admin/statistics/$', views_admin.statistic_view, name='admin/statistics'),
    url(r'^admin/createemployee/$', views_admin.createemployee_view, name='admin/createemployee'),
    url(r'^admin/add_hospital/$', views_admin.add_hospital_view, name='admin/add_hospital'),
    url(r'^admin/import/$', views_admin.csv_import_view, name='admin/import'),
    url(r'^admin/export/$', views_admin.csv_export_view, name='admin/export'),

    url(r'^message/list/$', views_message.list_view, name='message/list'),
    url(r'^message/new/$', views_message.new_view, name='message/new'),

    url(r'^appointment/list/$', views_appointment.list_view, name='appointment/list'),
    url(r'^appointment/calendar/$', views_appointment.calendar_view, name='appointment/calendar'),
    url(r'^appointment/update/$', views_appointment.update_view, name='appointment/update'),
    url(r'^appointment/create/$', views_appointment.create_view, name='appointment/create'),

    url(r'^profile/$', views_profile.profile_view, name='profile'),
    url(r'^profile/update/$', views_profile.update_view, name='profile/update'),
    url(r'^profile/password/$', views_profile.password_view, name='profile/password'),

    url(r'^medtest/upload/$', views_medtest.create_view, name='medtest/upload'),
    url(r'^medtest/list/$', views_medtest.list_view, name='medtest/list'),
    url(r'^medtest/display/$', views_medtest.display_view, name='medtest/display'),
    url(r'^medtest/update/$', views_medtest.update_view, name='medtest/update'),

    url(r'^admission/admit/$', views_admission.admit_view, name='admission/admit'),
    url(r'^admission/list/$', views_admission.list_view, name='admission/list'),

    url(r'^prescription/create/$', views_prescription.create_view, name='prescription/create'),
    url(r'^prescription/list/$', views_prescription.list_view, name='prescription/list'),

    url(r'^medicalinfo/list/$', views_medicalInfo.list_view, name='medicalinfo/list'),
    url(r'^medicalinfo/update/$', views_medicalInfo.update_view, name='medicalinfo/update'),
    url(r'^medicalinfo/patient/$', views_medicalInfo.update_view, name='medicalinfo/patient'),

    url(r'^', include(router.urls, namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^api/score', ScoreAPI.as_view()),
    # url(r'^api/user/(?P<pk>\d+)/$', UserAPI.as_view()),
    # url(r'^api/user', UserAPI.as_view()),
    url(r'^getauthtoken', GetAuthToken.as_view()),
    url(r'^api-token-auth/', vw.obtain_auth_token),
    url(r'^score/list/$', views_profile.list_view, name='score/list'),
    url(r'^score/list_admin/$', views_admin.list_view_admin, name='score/list_admin'),
    url(r'^score/new/$', views_profile.new_view, name='score/new'),
    url(r'^score/line/$', views_profile.chart_view),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns = format_suffix_patterns(urlpatterns)
