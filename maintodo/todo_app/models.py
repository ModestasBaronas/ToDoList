from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return '{} {}'.format(self.title, self.created)


class ToDoTask(models.Model):
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE,related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'todo_list'
