from django.conf.urls import url

urlpatterns = [
    url(r'^get-safepath/','safestRoute.views.calculateSafePath'),
    url(r'^mark-accident/','safestRoute.views.indicateAccident'), 
   	url(r'^is-safe-driving/','safestRoute.views.isBadDriving'),   
]
