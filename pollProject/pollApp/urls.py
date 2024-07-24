from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/results/detail/', views.results_detail, name='results_detail'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('admission_login/', views.admission_login, name='admission_login'),
]