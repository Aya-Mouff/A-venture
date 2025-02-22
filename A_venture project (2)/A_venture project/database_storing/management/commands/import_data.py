
print("helllloooo")
from django.core.management.base import BaseCommand
import pandas as pd
from pages.models import Record
import os

class Command(BaseCommand):
    help = 'Import data from Excel file to database'
 
    def handle(self, *args, **kwargs):
        print("Script started")  # Debugging: Confirm the script is running
        file_path = '15000-activities-propositions.xlsx'
        
        try:
            print(f"Reading file: {file_path}")  # Debugging: Confirm the file path
            data = pd.read_excel(file_path)
            print("File read successfully")  # Debugging: Confirm the file was read
            print(data.head())  # Debugging: Print the first few rows to verify the data
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        try:
            print("Creating records...")  # Debugging: Confirm record creation starts
            for index, row in data.iterrows():
                Record.objects.create(
                    code=row['code_pro'],
                    wilaya=row['wilaya'],
                    field=row['field'],
                    activity=row['activity'],
                    description=row['description'],
                    label=row['Predicted_Label'],
                )
            print("Records created successfully")  # Debugging: Confirm records were created
        except Exception as e:
            print(f"Error creating records: {e}")
            return

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        print("we didddddddddd")  # Debugging: Confirm the script reached the end