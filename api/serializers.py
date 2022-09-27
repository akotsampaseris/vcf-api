from rest_framework import serializers
import re

class VcfDataSerializer(serializers.Serializer):
    ID = serializers.CharField(min_length=3, max_length=55)
    CHROM = serializers.CharField(min_length=4, max_length=5)
    POS = serializers.IntegerField()
    ALT = serializers.ChoiceField(choices=['A','C','G','T','.'])
    REF = serializers.ChoiceField(choices=['A','C','G','T','.'])


    # Validation Rules helper functions    
    @staticmethod
    def is_alphanumeric(value):
        if not re.fullmatch(re.compile(r"[A-Za-z0-9]+"), value):
            error_msg = "Values should be strictly alphanumeric."
            
            raise serializers.ValidationError(error_msg)


    @staticmethod
    def has_prefix(value, prefix=''):
        if not value.lower().startswith(prefix):
            error_msg = "Values should start with '%s'." % (prefix) 

            raise serializers.ValidationError(error_msg)


    @staticmethod
    def ends_with_values(value, permitted_values=None):
        if not re.search(permitted_values, value):
            error_msg = "Values should end with %s." % (permitted_values)

            raise serializers.ValidationError(error_msg)


    # Validation Rules per field
    def validate_ID(self, value):
        # Field attributes
        prefix = 'rs'
        permitted_values = r"^([^0][0-9]*)$"

        # Field rules
        self.is_alphanumeric(value)
        self.has_prefix(value, prefix)
        self.ends_with_values(
            re.sub(prefix, '', value),
            permitted_values
        )
        
        return value


    def validate_CHROM(self, value):
        # Field attributes
        prefix = 'chr'
        permitted_values = r"^([XYMxym]|[1-9]|1[0-9]|2[0-2])$"

        # Field rules
        self.is_alphanumeric(value)
        self.has_prefix(value, prefix)
        self.ends_with_values(
            re.sub(prefix, '', value), 
            permitted_values
        )

        return value