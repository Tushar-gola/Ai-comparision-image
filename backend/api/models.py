from django.db import models
import random
import string
def genrateCode():
    length=6
    while True:
        code = ''.join(random.choice(string.ascii_uppercase,k=length))
        if Images.objects.filter(code=code).count() == 0:
            break
    return code
            
class Images(models.Model):
    code=models.CharField(max_length=6,default="")
    name=models.CharField(max_length=255,default="")
    user_id=models.IntegerField()
    image=models.CharField(max_length=100,default="")
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
    