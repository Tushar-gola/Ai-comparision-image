from rest_framework import serializers
from .models import Images

class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Images
        feilds = ('id','code','name','user_id','image','createdAt','updatedAt')