from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list_view),
    path('tag/(?p<tag_slug>[-w]+)/', views.post_list_view,name='post_list_by_tag_name'),
    path('/(?p<year>\d{4})/(?p<month>\d{2})/(?p<day>\d{2})/(?p<post>[-\w]+)/', views.post_detail_view,name='post_detail'),
    path('/(?p<id>\d+)/share', views.mail_send_view),
]
