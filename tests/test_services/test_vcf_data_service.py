import os
from dotenv import load_dotenv
from types import NoneType
import pytest
import pandas as pd

from django.http import Http404

from api.services import VcfDataService

load_dotenv()

class TestVcfDataService(VcfDataService):
    """
        Replicate service functionality and 
        test its validity using a mock VCF file.
    """

    vcf_dir_path = os.environ.get('VCF_DIR')
    vcf_filename = os.environ.get('VCF_TEST_FILE')
    working_vcf_file = '/'.join([vcf_dir_path, vcf_filename])


    def test_read_vcf_file(self):
        headers, data = self.read_vcf_file()
        
        assert len(headers) == 2
        assert type(headers) == list
        
        assert len(data) == 2
        assert type(data) == pd.DataFrame


    def test_write_data_to_file(self):
        headers, data = self.read_vcf_file()

        return_value = self.write_data_to_file(
            headers, data
        )
        returned_headers, returned_data = self.read_vcf_file()

        assert type(return_value) == NoneType
        assert os.path.exists(self.working_vcf_file)

        assert headers == returned_headers        
        assert data.equals(returned_data)


    def test_get_vcf_data(self):
        # Return all data rows
        data = self.get_vcf_data(id=None)
        
        assert type(data) == list
        assert len(data) == 2

        # Return data rows with correct id
        data = self.get_vcf_data(id='rs62635284')

        assert type(data) == list
        assert len(data) == 1

        # Return empty list using wrong id
        with pytest.raises(Http404):
            # Make sure it raises correct exception
            data = self.get_vcf_data(id='rs1')
 

    def test_create_vcf_data_row(self):
        new_data_row = {
            "ID": "rs1000",
            "CHROM": "chr1",
            "POS": 10000,
            "ALT": "C",
            "REF": "T"
        }

        data = self.get_vcf_data()

        assert type(data) == list
        assert len(data) == 2

        self.create_vcf_data_row(new_data_row)
        data = self.get_vcf_data()

        assert type(data) == list
        assert len(data) == 3

        returned_data_list = self.get_vcf_data(id='rs1000')
        assert len(returned_data_list) == 1

        returned_data_row = returned_data_list[0]
        assert returned_data_row['ID'] == new_data_row['ID']
        assert returned_data_row['CHROM'] == new_data_row['CHROM']
        assert returned_data_row['POS'] == new_data_row['POS']
        assert returned_data_row['ALT'] == new_data_row['ALT']
        assert returned_data_row['REF'] == new_data_row['REF']


    def test_update_vcf_data_row(self):
        new_data_row = {
            "ID": "rs1000",
            "CHROM": "chrX",
            "POS": 2000,
            "ALT": "A",
            "REF": "G"
        }

        data = self.get_vcf_data()

        assert type(data) == list
        assert len(data) == 3

        self.update_vcf_data_row(
            id='rs1000', 
            new_data_row=new_data_row
        )
        data = self.get_vcf_data()

        assert type(data) == list
        assert len(data) == 3

        returned_data_list = self.get_vcf_data(id='rs1000')
        assert len(returned_data_list) == 1

        returned_data_row = returned_data_list[0]
        assert returned_data_row['ID'] == new_data_row['ID']
        assert returned_data_row['CHROM'] == new_data_row['CHROM']
        assert returned_data_row['POS'] == new_data_row['POS']
        assert returned_data_row['ALT'] == new_data_row['ALT']
        assert returned_data_row['REF'] == new_data_row['REF']


    def test_delete_vcf_data_row(self):
        data = self.get_vcf_data()

        assert type(data) == list
        assert len(data) == 3

        self.delete_vcf_data_row(id='rs1000')
        data = self.get_vcf_data()

        assert type(data) == list
        assert len(data) == 2

        with pytest.raises(Http404):
            data = self.get_vcf_data(id='rs1000')

            