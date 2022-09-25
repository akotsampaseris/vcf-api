import re

from django.http import Http404, HttpResponseBadRequest

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

from api.serializers import VcfDataSerializer
from api.services import VcfDataService


class CustomXMLRenderer(XMLRenderer):
    root_tag_name = 'data'
    item_tag_name = 'row'


# Create your views here.
class VcfDataList(APIView, PageNumberPagination):
    parser_classes = [JSONParser, XMLParser]
    renderer_classes = [JSONRenderer, CustomXMLRenderer]

    def get(self, request, format=None):
        id = self.request.query_params.get('id')    
        
        if not re.fullmatch(re.compile(r"[A-Za-z0-9]+"), id):
            return HttpResponseBadRequest("\
                The id can only contain alphanumeric characters.\
            ")

        vcf_data = VcfDataService.get_vcf_data(id)
        
        if not vcf_data:
           raise Http404 

        results = self.paginate_queryset(vcf_data, request, view=self)
        serializer = VcfDataSerializer(results, many=True)

        return self.get_paginated_response(serializer.data)