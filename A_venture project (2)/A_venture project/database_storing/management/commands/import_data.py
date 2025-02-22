from django.core.management.base import BaseCommand
import pandas as pd
from pages.models import Record
import os

class Command(BaseCommand):
    help = 'Import data from Excel file to database'
 
    def handle(self, *args, **kwargs):
        print("Script started")
        
        # Get the directory where the current script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '15000-activities-propositions.xlsx')
        
        try:
            print(f"Reading file from: {file_path}")  # This will show the full path being used
            # List files in the directory for debugging
            print(f"Files in directory: {os.listdir(current_dir)}")
            
            data = pd.read_excel(file_path)
            print("File read successfully")
            print(data.head())  # Print first few rows to verify the data
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        try:
            print("Creating records...")
            for index, row in data.iterrows():
                Record.objects.create(
                    code=row['code_pro'],
                    wilaya=row['wilaya'],
                    field=row['field'],
                    activity=row['activity'],
                    description=row['description'],
                    label=row['Predicted_Label'],
                )
                # Print progress every 100 records
                if index % 100 == 0:
                    print(f"Processed {index} records...")
                    
            print("Records created successfully")
        except Exception as e:
            print(f"Error creating records: {e}")
            return

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        print("Import completed successfully")