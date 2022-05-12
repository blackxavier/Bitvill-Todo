from django.urls import path

from todo.views import (
    ListCreateApiTodo,
    TodoDetailUpdateDestroyApiView,
    AllCompletedTodoView,
    AllArchivedTodoView,
    ArchiveTodoView,
    CompleteTodoView,
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
        AllCompletedTodoView.as_view(),
        name="completed",
    ),
    path(
        "todos/archived/",
        AllArchivedTodoView.as_view(),
        name="archived",
    ),
    path(
        "todos/<int:pk>/archived/",
        ArchiveTodoView.as_view(),
        name="archived",
    ),
    path(
        "todos/<int:pk>/complete/",
        CompleteTodoView.as_view(),
        name="archived",
    ),
]
