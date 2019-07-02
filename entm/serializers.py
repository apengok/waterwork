
from rest_framework import serializers

from .models import Organizations
from dmam.models import Station
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_recursive.fields import RecursiveField


# class RecursiveField(serializers.Serializer):

#     def to_representation(self, value):
#         print('\r\tRecursiveField::::::\r\t')
#         serializer = self.parent.parent.__class__(value, context=self.context)
#         print('asdfer&*^*::::',serializer)
#         return serializer.data

class SubOrganizationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizations
        fields = ('id','name', )

class OrganizationsSerializer(serializers.ModelSerializer):
    # dma = serializers.StringRelatedField(many=True) 
    # children = serializers.StringRelatedField(many=True,read_only=True,required=False)
    # station = serializers.PrimaryKeyRelatedField(many=True,queryset=Station.objects.all()) 
    # children = RecursiveField(many=True)
    # parent = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # children = SubOrganizationsSerializer(many=True,read_only=True)
    parent = RecursiveField(allow_null=True)
    # children = serializers.ListField(child=RecursiveField())
    
    def to_presentation(self,instance):
        data = self.get_serializer(instance).data
        print('\r\n\t',data)

    class Meta:
        model = Organizations
        fields = ('id','name','parent')
        # depth = 3

    # def get_fields(self):
    #     fields = super(OrganizationsSerializer, self).get_fields()
    #     print('fields:',fields)
    #     fields['children'] = OrganizationsSerializer(many=True)
    #     return fields


# class CountryReportSerializer(serializers.ModelSerializer):
#     section_set = serializers.SerializerMethodField('get_parent_sections')

#     @staticmethod
#     def get_parent_sections(self, obj):
#         parent_sections = Section.objects.get(parent=None, pk=obj.pk)
#         serializer = SectionSerializer(parent_sections)
#         return serializer.data

#     class Meta:
#         model = CountryReport
#         fields = ('id', 'title', 'subtitle', 'section_set')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizations
        fields = '__all__'


class DepartmentViewSet(viewsets.ModelViewSet):
    model = Organizations
    serializer_class = DepartmentSerializer
    queryset = Organizations.objects.all()

    def serialize_tree(self, queryset):
        for obj in queryset:
            data = self.get_serializer(obj).data
            data['children'] = self.serialize_tree(obj.children.all())
            yield data

    def list(self, request):
        queryset = self.get_queryset()#.filter(level=0)
        data = self.serialize_tree(queryset)
        return Response(data)

    def retrieve(self, request, pk=None):
        self.object = self.get_object()
        data = self.serialize_tree([self.object])
        return Response(data)