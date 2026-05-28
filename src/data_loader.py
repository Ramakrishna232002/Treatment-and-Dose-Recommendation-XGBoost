"""
MIMIC-IV Demo Data Loader
Load and explore the MIMIC data for clinical decision support
"""

import pandas as pd
import os
import gzip
from pathlib import Path

class MIMICDataLoader:
    def __init__(self, data_path="data/raw/mimic_demo/mimic-iv-clinical-database-demo-2.2"):
        self.data_path = Path(data_path)
        self.hosp_path = self.data_path / "hosp"
        self.icu_path = self.data_path / "icu"
        
    def load_table(self, table_name, module="hosp"):
        """Load a gzipped CSV file from MIMIC data"""
        if module == "hosp":
            file_path = self.hosp_path / f"{table_name}.csv.gz"
        else:
            file_path = self.icu_path / f"{table_name}.csv.gz"
            
        if file_path.exists():
            print(f"Loading {file_path}...")
            return pd.read_csv(file_path, compression='gzip')
        else:
            print(f"File not found: {file_path}")
            return None
    
    def explore_data(self):
        """Print basic info about available tables"""
        print("=" * 50)
        print("MIMIC-IV Demo Data Explorer")
        print("=" * 50)
        
        # Check if paths exist
        print(f"\nHosp path exists: {self.hosp_path.exists()}")
        print(f"Hosp path: {self.hosp_path}")
        print(f"\nICU path exists: {self.icu_path.exists()}")
        print(f"ICU path: {self.icu_path}")
        
        if self.hosp_path.exists():
            print("\n Available Hosp tables:")
            for f in sorted(self.hosp_path.glob("*.csv.gz")):
                size_mb = f.stat().st_size / (1024 * 1024)
                print(f"  - {f.name} ({size_mb:.2f} MB)")
                
        if self.icu_path.exists():
            print("\n Available ICU tables:")
            for f in sorted(self.icu_path.glob("*.csv.gz")):
                size_mb = f.stat().st_size / (1024 * 1024)
                print(f"  - {f.name} ({size_mb:.2f} MB)")
    
    def load_patients(self):
        """Load patient demographics"""
        return self.load_table("patients", "hosp")
    
    def load_admissions(self):
        """Load admission records"""
        return self.load_table("admissions", "hosp")
    
    def load_diagnoses(self):
        """Load ICD diagnoses"""
        return self.load_table("diagnoses_icd", "hosp")
    
    def load_labevents(self):
        """Load lab events (creatinine, glucose, etc.)"""
        return self.load_table("labevents", "hosp")
    
    def load_prescriptions(self):
        """Load medication prescriptions"""
        return self.load_table("prescriptions", "hosp")
    
    def load_chartevents(self):
        """Load vitals and chart events (BP, HR, etc.)"""
        return self.load_table("chartevents", "icu")

# Quick test
if __name__ == "__main__":
    loader = MIMICDataLoader()
    loader.explore_data()
    
    # Try loading a small table
    print("\n" + "=" * 50)
    print("Loading sample data...")
    print("=" * 50)
    
    patients = loader.load_patients()
    if patients is not None:
        print(f"\n Patients table loaded: {patients.shape}")
        print(patients.head())
