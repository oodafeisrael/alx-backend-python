from django.urls import path
from . import views
#from .views import delete_user


app_name = 'messaging'

urlpatterns = [
    # path('delete_user/', delete_user, name='delete_user'),
    # path('inbox/', views.inbox, name='inbox'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('send/', views.send_message, name='send_message'),
    path('reply/<int:message_id>/', views.reply_message, name='reply_message'),
   # path('thread/<int:message_id>/', views.view_message_thread, name='view_message_thread'),

]

