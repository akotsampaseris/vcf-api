import os
import io
import pandas as pd
from dotenv import load_dotenv

from django.http import Http404

load_dotenv()


class VcfDataService:
    vcf_dir_path = os.environ.get('VCF_DIR')
    vcf_filename = os.environ.get('VCF_FILENAME')
    working_vcf_file = '/'.join([vcf_dir_path, vcf_filename])

    @classmethod
    def read_vcf_file(cls) -> pd.DataFrame:
        headers = []
        rows = []

        with open(cls.working_vcf_file, 'r') as vcf:
            for line in vcf:
                if line.startswith('##'):
                    headers.append(line)
                else:
                    rows.append(line)
            
            data = pd.read_csv(
                io.StringIO(''.join(rows)),
                dtype={
                    '#CHROM': str,
                    'POS': int,
                    'ID': str,
                    'REF': str,
                    'ALT': str, 
                },
                sep='\t'
            ).rename(columns={'#CHROM': 'CHROM'})

        return headers, data


    @classmethod
    def write_data_to_file(cls, 
        headers: list[str], data: pd.DataFrame
    ) -> None:
        f = open(cls.working_vcf_file, 'w')
        f.write(''.join(headers))
        f.close()

        data.rename(columns={'CHROM': '#CHROM'}).to_csv(
            cls.working_vcf_file,
            mode='a',
            sep='\t',
            index=False,
            header=True
        )


    @classmethod
    def get_vcf_data(cls, id = None):
        headers, data = cls.read_vcf_file()
        
        data = data.loc[data['ID']==id] if id else data
        if data.empty: raise Http404 

        return data.to_dict('records')


    @classmethod
    def create_vcf_data_row(cls, 
        new_data_row: dict = {}
    ) -> None:
        headers, data = cls.read_vcf_file()

        data = pd.concat([
            data, 
            pd.DataFrame.from_records([new_data_row]
        )], sort=False)
        
        cls.write_data_to_file(headers, data)


    @classmethod
    def update_vcf_data_row(cls, 
        id: str = None, new_data_row: dict = {}
    ) -> None:
        
        headers, data = cls.read_vcf_file()

        rows_to_be_updated = data.loc[data['ID']==id]
        
        if rows_to_be_updated.empty:
            raise Http404
        else:
            data.loc[data['ID']==id, 
                [key for key, values in new_data_row.items()]
            ] = [
                new_data_row[key] 
                for key, values in new_data_row.items()
            ]
        
        cls.write_data_to_file(headers, data)


    @classmethod
    def delete_vcf_data_row(cls, id: str = None) -> None:
        headers, data = cls.read_vcf_file()

        data_to_be_dropped = data.loc[data['ID']==id]
        
        if data_to_be_dropped.empty:
            raise Http404
        else:
            data = data.drop([
                data.index[index] 
                for index in data_to_be_dropped.index
            ])
        
        cls.write_data_to_file(headers, data)
