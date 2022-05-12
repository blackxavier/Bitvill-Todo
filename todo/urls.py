from django.urls import path

from todo.views import (
    ListCreateApiTodo,
    TodoDetailUpdateDestroyApiView,
    TodoCompletedView,
    TodoArchivedView,
)


app_name = "todo"


urlpatterns = [
    path("todos/", ListCreateApiTodo.as_view(), name="list-create-todo"),
    path(
        "todos/<int:id>/",
        TodoDetailUpdateDestroyApiView.as_view(),
        name="retrieve-update-delete",
    ),
    path(
        "todos/completed/",
        TodoCompletedView.as_view(),
        name="completed",
    ),
    path(
        "todos/archived/",
        TodoArchivedView.as_view(),
        name="archived",
    ),
]
