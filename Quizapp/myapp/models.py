from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, null=True)
     
    def __str__(self):
        return self.name



class QuestionModel(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    question = models.CharField(max_length=500, null=True)
    option1 = models.CharField(max_length=200, null=True)
    option2 = models.CharField(max_length=200, null=True)
    option3 = models.CharField(max_length=200, null=True)
    option4 = models.CharField(max_length=200, null=True)
    answer = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.question
