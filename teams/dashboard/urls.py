from django.urls import path

from .views import index, board, board_create, column_create, task_create, task_modify, tasks, task_delete

urlpatterns = [
    path('',  index, name='board_index'),
    path('<int:id>', board, name='board'),
    path('create', board_create, name='board_create'),
    path('<int:id>/create', column_create, name='column_create'),
    path('<int:id>/<int:column_id>', tasks, name='tasks'),
    path('<int:id>/<int:column_id>/create', task_create, name='task_create'),
    path('<int:id>/<int:column_id>/<int:task_id>/modify', task_modify, name='task_modify'),
    path('<int:id>/<int:column_id>/<int:task_id>/delete', task_delete, name='task_delete'),
]