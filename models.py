from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50,null=True)

    def __str__(self):
        return str(self.name)


class State(models.Model):
    name = models.CharField(max_length=50,null=True)

    def __str__(self):
        return str(self.name)



class City(models.Model):
    D_id = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    S_id = models.ForeignKey(State,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=50,null=True)

    def __str__(self):
        return str(self.name)
