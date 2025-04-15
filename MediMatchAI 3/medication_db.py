import pandas as pd
import os
import re
from typing import Dict, List, Optional, Union

# Data file paths
MEDICATIONS_CSV = os.path.join("data", "medications.csv")
DRUG_CLASSES_CSV = os.path.join("data", "drug_classes.csv")

def load_medications() -> pd.DataFrame:
    """
    Load the medications database from CSV.
    Creates a sample database if file doesn't exist.
    """
    try:
        # Check if the data directory exists, create if not
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Check if the CSV file exists
        if not os.path.exists(MEDICATIONS_CSV):
            # Create sample medication data
            data = {
                'name': [
                    'Lipitor', 'Atorvastatin', 'Crestor', 'Rosuvastatin', 
                    'Zoloft', 'Sertraline', 'Prozac', 'Fluoxetine',
                    'Nexium', 'Esomeprazole', 'Prilosec', 'Omeprazole',
                    'Advil', 'Ibuprofen', 'Tylenol', 'Acetaminophen',
                    'Claritin', 'Loratadine', 'Zyrtec', 'Cetirizine',
                    'Metformin', 'Glucophage', 'Januvia', 'Sitagliptin',
                    'Simvastatin', 'Zocor', 'Lovastatin', 'Mevacor',
                    'Amoxicillin', 'Augmentin', 'Cephalexin', 'Keflex'
                ],
                'drug_class': [
                    'Statin', 'Statin', 'Statin', 'Statin',
                    'SSRI', 'SSRI', 'SSRI', 'SSRI',
                    'PPI', 'PPI', 'PPI', 'PPI',
                    'NSAID', 'NSAID', 'Analgesic', 'Analgesic',
                    'Antihistamine', 'Antihistamine', 'Antihistamine', 'Antihistamine',
                    'Biguanide', 'Biguanide', 'DPP-4 Inhibitor', 'DPP-4 Inhibitor',
                    'Statin', 'Statin', 'Statin', 'Statin',
                    'Penicillin', 'Penicillin combination', 'Cephalosporin', 'Cephalosporin'
                ],
                'description': [
                    'Used to lower cholesterol and prevent heart disease', 'Used to lower cholesterol and prevent heart disease',
                    'Used to lower cholesterol and prevent heart disease', 'Used to lower cholesterol and prevent heart disease',
                    'Used to treat depression, anxiety, and other mental health conditions', 'Used to treat depression, anxiety, and other mental health conditions',
                    'Used to treat depression, anxiety, and other mental health conditions', 'Used to treat depression, anxiety, and other mental health conditions',
                    'Used to reduce stomach acid and treat acid reflux', 'Used to reduce stomach acid and treat acid reflux',
                    'Used to reduce stomach acid and treat acid reflux', 'Used to reduce stomach acid and treat acid reflux',
                    'Used to reduce pain, inflammation, and fever', 'Used to reduce pain, inflammation, and fever',
                    'Used to reduce fever and relieve pain', 'Used to reduce fever and relieve pain',
                    'Used to treat allergies', 'Used to treat allergies',
                    'Used to treat allergies', 'Used to treat allergies',
                    'Used to control blood sugar in type 2 diabetes', 'Used to control blood sugar in type 2 diabetes',
                    'Used to control blood sugar in type 2 diabetes', 'Used to control blood sugar in type 2 diabetes',
                    'Used to lower cholesterol and prevent heart disease', 'Used to lower cholesterol and prevent heart disease',
                    'Used to lower cholesterol and prevent heart disease', 'Used to lower cholesterol and prevent heart disease',
                    'Used to treat bacterial infections', 'Used to treat bacterial infections',
                    'Used to treat bacterial infections', 'Used to treat bacterial infections'
                ],
                'avg_cost': [
                    250.00, 20.00, 280.00, 35.00,
                    120.00, 15.00, 135.00, 15.00,
                    250.00, 25.00, 30.00, 15.00,
                    15.00, 5.00, 12.00, 5.00,
                    45.00, 10.00, 40.00, 12.00,
                    20.00, 15.00, 500.00, 450.00,
                    20.00, 180.00, 18.00, 150.00,
                    20.00, 45.00, 15.00, 25.00
                ],
                'is_brand': [
                    True, False, True, False,
                    True, False, True, False,
                    True, False, True, False,
                    True, False, True, False,
                    True, False, True, False,
                    False, True, True, False,
                    False, True, False, True,
                    False, True, False, True
                ],
                'brand_equivalent': [
                    '', 'Lipitor', '', 'Crestor',
                    '', 'Zoloft', '', 'Prozac',
                    '', 'Nexium', '', 'Prilosec',
                    '', 'Advil', '', 'Tylenol',
                    '', 'Claritin', '', 'Zyrtec',
                    'Glucophage', '', '', 'Januvia',
                    'Zocor', '', 'Mevacor', '',
                    '', '', '', ''
                ],
                'side_effects': [
                    'Muscle pain, liver problems, digestive issues', 'Muscle pain, liver problems, digestive issues',
                    'Muscle pain, headache, weakness', 'Muscle pain, headache, weakness',
                    'Nausea, insomnia, sexual dysfunction, dry mouth', 'Nausea, insomnia, sexual dysfunction, dry mouth',
                    'Nausea, insomnia, anxiety, headache', 'Nausea, insomnia, anxiety, headache',
                    'Headache, diarrhea, nausea, abdominal pain', 'Headache, diarrhea, nausea, abdominal pain',
                    'Headache, abdominal pain, diarrhea', 'Headache, abdominal pain, diarrhea',
                    'Stomach pain, heartburn, nausea, dizziness', 'Stomach pain, heartburn, nausea, dizziness',
                    'Nausea, headache, liver damage (with overuse)', 'Nausea, headache, liver damage (with overuse)',
                    'Headache, drowsiness, fatigue, dry mouth', 'Headache, drowsiness, fatigue, dry mouth',
                    'Drowsiness, fatigue, dry mouth', 'Drowsiness, fatigue, dry mouth',
                    'Diarrhea, nausea, abdominal discomfort', 'Diarrhea, nausea, abdominal discomfort',
                    'Upper respiratory tract infection, headache', 'Upper respiratory tract infection, headache',
                    'Muscle pain, liver problems, digestive issues', 'Muscle pain, liver problems, digestive issues',
                    'Muscle pain, liver problems, digestive issues', 'Muscle pain, liver problems, digestive issues',
                    'Diarrhea, nausea, rash', 'Diarrhea, nausea, rash, abdominal discomfort',
                    'Diarrhea, nausea, allergic reactions', 'Diarrhea, nausea, allergic reactions'
                ],
                'interactions': [
                    'Grapefruit juice, certain antibiotics, antifungals', 'Grapefruit juice, certain antibiotics, antifungals',
                    'Cyclosporine, gemfibrozil, antacids', 'Cyclosporine, gemfibrozil, antacids',
                    'MAOIs, other antidepressants, aspirin', 'MAOIs, other antidepressants, aspirin',
                    'MAOIs, other antidepressants, NSAIDs', 'MAOIs, other antidepressants, NSAIDs',
                    'Diazepam, digoxin, cilostazol', 'Diazepam, digoxin, cilostazol',
                    'Diazepam, warfarin, phenytoin', 'Diazepam, warfarin, phenytoin',
                    'Aspirin, blood thinners, blood pressure medications', 'Aspirin, blood thinners, blood pressure medications',
                    'Alcohol, NSAIDs, anticoagulants', 'Alcohol, NSAIDs, anticoagulants',
                    'Alcohol, sedatives', 'Alcohol, sedatives',
                    'Alcohol, sedatives', 'Alcohol, sedatives',
                    'Alcohol, certain diuretics, contrast dyes', 'Alcohol, certain diuretics, contrast dyes',
                    'Digoxin, certain antifungals', 'Digoxin, certain antifungals',
                    'Grapefruit juice, certain antibiotics', 'Grapefruit juice, certain antibiotics',
                    'Grapefruit juice, certain antibiotics', 'Grapefruit juice, certain antibiotics',
                    'Probenecid, allopurinol, oral contraceptives', 'Probenecid, allopurinol, oral contraceptives',
                    'Probenecid, anticoagulants', 'Probenecid, anticoagulants'
                ],
                'source': [
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic',
                    'FDA, Mayo Clinic', 'FDA, Mayo Clinic'
                ]
            }
            
            # Create and save the dataframe
            df = pd.DataFrame(data)
            df.to_csv(MEDICATIONS_CSV, index=False)
        
        # Load drug classes if file doesn't exist
        if not os.path.exists(DRUG_CLASSES_CSV):
            # Create sample drug class data
            class_data = {
                'class_name': [
                    'Statin', 'SSRI', 'PPI', 'NSAID', 'Analgesic', 
                    'Antihistamine', 'Biguanide', 'DPP-4 Inhibitor',
                    'Penicillin', 'Cephalosporin'
                ],
                'full_name': [
                    'HMG-CoA Reductase Inhibitors', 'Selective Serotonin Reuptake Inhibitors',
                    'Proton Pump Inhibitors', 'Nonsteroidal Anti-inflammatory Drugs',
                    'Pain Relievers', 'Antihistamines', 'Biguanides',
                    'Dipeptidyl Peptidase-4 Inhibitors', 'Penicillins', 'Cephalosporins'
                ],
                'description': [
                    'Medications that lower cholesterol levels by inhibiting the HMG-CoA reductase enzyme',
                    'Antidepressants that increase serotonin levels in the brain by blocking reabsorption',
                    'Medications that reduce stomach acid production by blocking the proton pump enzyme',
                    'Medications that reduce pain, inflammation, and fever by blocking certain enzymes',
                    'Medications that relieve pain by various mechanisms',
                    'Medications that block histamine receptors to treat allergies',
                    'Medications that decrease glucose production in the liver and improve insulin sensitivity',
                    'Medications that increase insulin production and decrease glucagon levels to control blood sugar',
                    'Antibiotics that kill bacteria by disrupting cell wall synthesis',
                    'Antibiotics similar to penicillins that disrupt bacterial cell wall synthesis'
                ],
                'common_uses': [
                    'High cholesterol, heart disease prevention',
                    'Depression, anxiety, obsessive-compulsive disorder, PTSD',
                    'Heartburn, acid reflux, GERD, stomach ulcers',
                    'Pain, inflammation, fever, arthritis',
                    'Pain relief for various conditions',
                    'Allergies, hay fever, cold symptoms',
                    'Type 2 diabetes management',
                    'Type 2 diabetes management',
                    'Bacterial infections of various types',
                    'Bacterial infections, often used for penicillin-allergic patients'
                ]
            }
            
            # Create and save the dataframe
            class_df = pd.DataFrame(class_data)
            class_df.to_csv(DRUG_CLASSES_CSV, index=False)
            
        # Load medications data
        return pd.read_csv(MEDICATIONS_CSV)
    
    except Exception as e:
        print(f"Error loading medications database: {e}")
        # Return an empty DataFrame as fallback
        return pd.DataFrame(columns=['name', 'drug_class', 'description', 'avg_cost', 
                                    'is_brand', 'brand_equivalent', 'side_effects', 
                                    'interactions', 'source'])

def load_drug_classes() -> pd.DataFrame:
    """Load the drug classes database from CSV."""
    try:
        return pd.read_csv(DRUG_CLASSES_CSV)
    except Exception as e:
        print(f"Error loading drug classes database: {e}")
        # Return an empty DataFrame as fallback
        return pd.DataFrame(columns=['class_name', 'full_name', 'description', 'common_uses'])

def get_medication_info(medication_name: str) -> Optional[Dict]:
    """
    Get information about a specific medication.
    
    Args:
        medication_name: Name of the medication to look up
        
    Returns:
        Dictionary with medication information or None if not found
    """
    df = load_medications()
    
    # Case-insensitive search for exact match
    medication = df[df['name'].str.lower() == medication_name.lower()]
    
    if not medication.empty:
        return medication.iloc[0].to_dict()
    
    # If no exact match, try partial matching
    medication = df[df['name'].str.lower().str.contains(medication_name.lower())]
    
    if not medication.empty:
        return medication.iloc[0].to_dict()
    
    return None

def get_medication_by_class(drug_class: str) -> List[Dict]:
    """
    Get all medications in a specific drug class.
    
    Args:
        drug_class: Name of the drug class to look up
        
    Returns:
        List of dictionaries with medication information
    """
    df = load_medications()
    
    # Case-insensitive search
    medications = df[df['drug_class'].str.lower() == drug_class.lower()]
    
    if medications.empty:
        return []
    
    return medications.to_dict('records')

def search_medications(query: str) -> List[Dict]:
    """
    Search for medications by name or drug class.
    
    Args:
        query: Search term
        
    Returns:
        List of dictionaries with medication information
    """
    df = load_medications()
    
    # Search in name or drug class (case-insensitive)
    medications = df[
        df['name'].str.lower().str.contains(query.lower()) |
        df['drug_class'].str.lower().str.contains(query.lower())
    ]
    
    if medications.empty:
        return []
    
    return medications.to_dict('records')

def get_brand_generic_pairs() -> Dict[str, str]:
    """
    Get all brand-generic medication pairs.
    
    Returns:
        Dictionary mapping brand names to their generic equivalents
    """
    df = load_medications()
    
    # Filter for brand medications
    brands = df[df['is_brand'] == True]
    
    pairs = {}
    for _, row in brands.iterrows():
        # Find the generic equivalent
        generic = df[(df['brand_equivalent'] == row['name']) & (df['is_brand'] == False)]
        
        if not generic.empty:
            pairs[row['name']] = generic.iloc[0]['name']
    
    return pairs

def get_generic_brand_pairs() -> Dict[str, str]:
    """
    Get all generic-brand medication pairs.
    
    Returns:
        Dictionary mapping generic names to their brand equivalents
    """
    df = load_medications()
    
    # Filter for generic medications
    generics = df[df['is_brand'] == False]
    
    pairs = {}
    for _, row in generics.iterrows():
        if row['brand_equivalent']:
            pairs[row['name']] = row['brand_equivalent']
    
    return pairs

def get_drug_class_info(class_name: str) -> Optional[Dict]:
    """
    Get information about a specific drug class.
    
    Args:
        class_name: Name of the drug class to look up
        
    Returns:
        Dictionary with drug class information or None if not found
    """
    df = load_drug_classes()
    
    # Case-insensitive search
    drug_class = df[df['class_name'].str.lower() == class_name.lower()]
    
    if not drug_class.empty:
        return drug_class.iloc[0].to_dict()
    
    # If no exact match, try partial matching
    drug_class = df[df['class_name'].str.lower().str.contains(class_name.lower())]
    
    if not drug_class.empty:
        return drug_class.iloc[0].to_dict()
    
    return None
