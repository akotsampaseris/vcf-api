from pkgutil import read_code
from rest_framework import serializers

class VcfDataSerializer(serializers.Serializer):
    ID = serializers.CharField()
    CHROM = serializers.CharField()
    POS = serializers.IntegerField()
    ALT = serializers.CharField()
    REF = serializers.CharField()
