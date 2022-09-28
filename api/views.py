import re

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer

from api.serializers import VcfDataSerializer
from api.services import VcfDataService
from api.authentications import SecretKeyAuthentication


# Create your views here.
class VcfDataList(APIView, PageNumberPagination):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer, XMLRenderer]
    page_size = 100
    page_size_query_param = 'page_size'

    def get(self, request, format=None):
        id = self.request.query_params.get('id')
        
        custom_page_size = \
            self.request.query_params.get('page_size')
        
        self.page_size = custom_page_size \
            if custom_page_size else self.page_size
        
        if id and not re.fullmatch(re.compile(r"[A-Za-z0-9]+"), id):
            error_msg = "ID value must be alphanumeric"
            return Response(error_msg, 
                status=status.HTTP_400_BAD_REQUEST
            )

        vcf_data = VcfDataService.get_vcf_data(id)

        results = self.paginate_queryset(
            vcf_data, request, view=self
        )
        serializer = VcfDataSerializer(results, many=True)

        return self.get_paginated_response(serializer.data)


class VcfDataRow(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer, XMLRenderer]
    authentication_classes = [SecretKeyAuthentication]

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = VcfDataSerializer(data=data)

        if serializer.is_valid():
            VcfDataService.create_vcf_data_row(serializer.data)
            return Response(serializer.data, 
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )


    def put(self, request, format=None):
        id = self.request.query_params.get('id')
        data = JSONParser().parse(request)
        serializer = VcfDataSerializer(data=data)

        if id and not re.fullmatch(re.compile(r"[A-Za-z0-9]+"), id):
            error_msg = "ID value must be alphanumeric"
            return Response(error_msg, 
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if serializer.is_valid():
                VcfDataService.update_vcf_data_row(id, serializer.data)
                return Response(serializer.data, 
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        

    def delete(self, request, format=None):
        id = self.request.query_params.get('id')    

        if id and not re.fullmatch(re.compile(r"[A-Za-z0-9]+"), id):
            error_msg = "ID value must be alphanumeric"
            return Response(error_msg, 
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            VcfDataService.delete_vcf_data_row(id)
            return Response('Rows deleted successfully.', 
                status=status.HTTP_204_NO_CONTENT
            )
    