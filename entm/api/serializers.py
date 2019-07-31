# -*- coding: utf-8 -*-
from rest_framework import serializers
from entm.models import Organizations
import traceback
from entm.utils import unique_cid_generator,unique_uuid_generator,unique_rid_generator

class OrganizationsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    
    class Meta:
        model = Organizations
        fields = ('id','name','parent','attribute','organlevel','register_date','owner_name','phone_number','firm_address',
            'coorType','longitude','latitude','zoomIn','islocation','location','province','city','district','adcode','districtlevel',
            'cid','pId','is_org','uuid')

    def validate_name(self,value):
        qs = Organizations.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Organizations with this name already exists")
        return value

    
    def create(self, validated_data):  
        print(validated_data)
        organ_obj = Organizations(
                name=validated_data.get('name'), 
                parent=validated_data.get('parent'))
        organ_obj.cid = unique_cid_generator(organ_obj,"api")
        organ_obj.save()
        return organ_obj

    # def update(self,instance,validated_data):
    #     print('\r\nupdate--')
    #     print(validated_data)
    #     instance.save()
    #     return instance

    # def validate(self,attrs):
    #     traceback.print_exc()
    #     print("when run to here?")
    #     attrs["pId"] = "scada"
    #     return attrs