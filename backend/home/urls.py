from django.urls import path
from . import views
from .views import process_scenario
from .views import save_slider_data
#urls for home app
urlpatterns = [
    path('', views.index, name='index'),
    path('api/process-scenario/', process_scenario, name='process_scenario'), # url for default scenario loads
    path('api/save-slider-data/', save_slider_data, name='save_slider_data'), #url for slider input 
    #path('api/upload_files/', upload_files, name='upload_files'), #url for Scenario Upload
    #path('api/save-scenario/', views.save_scenario, name='save_scenario'),
]
