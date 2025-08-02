from django.urls import path
from . import views
#from .views import delete_user


app_name = 'messaging'

urlpatterns = [
    # path('delete_user/', delete_user, name='delete_user'),
    path('inbox/', views.inbox, name='inbox'),
   # path('thread/<int:message_id>/', views.view_message_thread, name='view_message_thread'),

]

