import csv
import io
import pandas as pd

vcf_file_path = "./api/test.vcf"

class VcfData:
    def __init__(self, ID, CHROM, POS, REF, ALT) -> None:
        self.ID = ID
        self.CHROM = CHROM
        self.POS = POS
        self.REF = REF
        self.ALT = ALT


class VcfDataService:
    @classmethod
    def get_vcf_data(cls, id = None):
        with open(vcf_file_path, 'r') as vcf:
            lines = [line for line in vcf if not line.startswith('##')]
            
            df = pd.read_csv(
                io.StringIO(''.join(lines)),
                dtype={
                    '#CHROM': str,
                    'POS': int,
                    'ID': str,
                    'REF': str,
                    'ALT': str, 
                },
                sep='\t'
            ).rename(columns={'#CHROM': 'CHROM'})

            data = df[['ID','CHROM', 'POS', 'REF', 'ALT']]
            
            if id is not None:
                data = data.loc[data['ID'] == id]

        return [VcfData(**item) for item in data.to_dict('records')]