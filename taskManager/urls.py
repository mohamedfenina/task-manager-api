# urls.py
from django.urls import path
from .views import register_account, login, create_task, create_account, get_accounts_by_admin, \
    update_account_status, update_account_details, get_tasks_by_admin, get_tasks_by_user, done_tasks

urlpatterns = [
    path('api/register', register_account, name='register_account'),
    path('api/createAccount', create_account, name='create_account'),
    path('api/login', login, name='login'),
    path('api/get_task_byAdmin', get_tasks_by_admin, name='task_list_admin'),
    path('api/get_tasks_by_user', get_tasks_by_user, name='task_list_user'),
    path('api/done_tasks', done_tasks, name='done_tasks'),
    path('api/createtask', create_task, name='create_task'),
    path('api/accounts', get_accounts_by_admin, name='get_accounts_by_admin'),
    path('api/update_status', update_account_status, name='update_account_status'),
    path('api/update_details', update_account_details, name='update_account_details'),

]
