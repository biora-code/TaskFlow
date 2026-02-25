from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = ['status', 'due_date']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']
    def get_queryset(self):
        return Task.objects.filter(
        user=self.request.user,
        parent__isnull=True
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(detail=True, methods=['post'], url_path='generate-subtasks')
    def generate_subtasks(self, request, pk=None):
        task = self.get_object()

        if not settings.OPENROUTER_API_KEY:
            return Response(
            {"error": "AI service not configured."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        prompt = f"""
        Break down the following task into 5 clear actionable subtasks.
        Return the result as a JSON array of strings.

        Task Title: {task.title}
        Task Description: {task.description}
        """

        try:
            response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "TaskFlow",
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

            data = response.json()
            content = data["choices"][0]["message"]["content"]

            return Response({
                "suggestions": content
            })

        except Exception as e:
            return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

