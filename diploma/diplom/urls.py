from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.Base.as_view()),
    path('acc', views.AccentC.as_view()),
    path('new', views.New_user.as_view(), name = 'new_user'),
    path('sigin', views.Login.as_view(), name = 'sig'),
    path('reg', views.New_user.as_view(), name = 'reg'),
    path('audio', views.Audio.as_view(), name='audio'),
    path('dproc',views.DataCutting.as_view(), name='dcut'),
    path('class', views.DataPredict.as_view(), name='class'),
    path('history', views.History.as_view(), name = 'his'),
    path('logout', views.Logout.as_view(), name='logout')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


