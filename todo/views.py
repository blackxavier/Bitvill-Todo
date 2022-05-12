from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from todo.models import Todo
from todo.serializers import (
    ReadTodoSerializer,
    ReadDetailTodoSerializer,
    PostWriteTodoSerializer,
)
from todo.pagination import CustomPaginator


class ListCreateApiTodo(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        todos = Todo.objects.filter(user=user)
        paginator = CustomPaginator()
        response = paginator.generate_response(todos, ReadTodoSerializer, request)

        data = {"data": response.data, "status": f"{status.HTTP_200_OK} OK"}
        return Response(data)

    def post(self, request, *args, **kwargs):
        serializer = PostWriteTodoSerializer(data=request.data)
        if serializer.is_valid():
            todo = serializer.save(user=request.user)
            response = {
                "data": {
                    "id": todo.id,
                    "item": todo.item,
                    "start_date": todo.start_date,
                    "end_date": todo.end_date,
                    "is_completed": todo.is_completed,
                    "is_archived": todo.is_archived,
                },
                "status": f"{status.HTTP_201_CREATED} CREATED",
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailUpdateDestroyApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=kwargs["id"])
        serializer = ReadDetailTodoSerializer(todo)
        data = {
            "data": serializer.data,
            "status": f"{status.HTTP_200_OK} OK",
        }
        return Response(data)

    def put(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=kwargs["id"])
        serializer = PostWriteTodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            todo = serializer.save()
            data = {
                "status": f"{status.HTTP_200_OK} OK",
            }

            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=kwargs["id"])
        serializer = PostWriteTodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            todo = serializer.save()
            data = {
                "status": f"{status.HTTP_200_OK} OK",
            }

            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=kwargs["id"])
        todo.delete()
        return Response("Todo deleted", status=status.HTTP_204_NO_CONTENT)


from rest_framework import filters


class TodoCompletedView(ListAPIView):
    serializer_class = ReadTodoSerializer
    queryset = Todo.completed.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["item"]
    ordering_fields = ["username", "email"]


class TodoArchivedView(ListAPIView):
    serializer_class = ReadTodoSerializer
    queryset = Todo.archived.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["item"]
    ordering_fields = ["username", "email"]
