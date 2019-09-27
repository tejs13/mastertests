# from rest_framework import viewsets
# from rest_framework import status
# from.models import Department
# from .serializers import DepartmentSerializer
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404


#############################################     NOT USED      ######################################################
# class DetailViewSet(viewsets.ViewSet):
#     def list(self,request,model):
#         print(model)
#
#         dataset=Department.objects.all()
#         serializer=DepartmentSerializer(dataset,many=True)
#         return Response(serializer.data)
#
#     def retrieve(self,request,id):
#         dataset=Department.objects.all()
#         dept_name=get_object_or_404(dataset,id=id)
#         serializer=DepartmentSerializer(dept_name)
#         return Response(serializer.data)
#
#     def create(self,request):
#         serializer=DepartmentSerializer(request.data)
#         if serializer.is_valid():
#             Department.objects.create(**serializer.validated_data)
#             return Response(serializer.validated_data,status=status.HTTP_201_created)
#         return Response({'msg':'not created'},status=status.HTTP_400_BAD_REQUEST)
#
#


