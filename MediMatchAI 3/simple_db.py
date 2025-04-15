import pandas as pd
import os
from typing import Dict, List, Optional

# Path to the simplified medications database
MEDICATIONS_CSV = os.path.join("data", "medications_simple.csv")

# Medication risks database (static for now)
MEDICATION_RISKS = {
    "Diphenhydramine": "May cause drowsiness, dry mouth, urinary retention. Not recommended for elderly.",
    "Benadryl": "May cause drowsiness, dry mouth, urinary retention. Not recommended for elderly.",
    "Cetirizine": "May cause drowsiness or dry mouth. Generally well-tolerated.",
    "Zyrtec": "May cause drowsiness or dry mouth. Generally well-tolerated.",
    "Loratadine": "May cause headache or dry mouth. Non-drowsy for most people.",
    "Claritin": "May cause headache or dry mouth. Non-drowsy for most people.",
    "Ibuprofen": "Can cause ulcers or kidney problems. Not advised for people with asthma.",
    "Advil": "Can cause ulcers or kidney problems. Not advised for people with asthma.",
    "Naproxen": "May cause stomach upset or raise blood pressure. Avoid with kidney problems.",
    "Aleve": "May cause stomach upset or raise blood pressure. Avoid with kidney problems.",
    "Acetaminophen": "Can cause liver damage at high doses. Avoid with alcohol.",
    "Tylenol": "Can cause liver damage at high doses. Avoid with alcohol.",
    "Atorvastatin": "May cause muscle pain or liver enzyme elevations.",
    "Lipitor": "May cause muscle pain or liver enzyme elevations.",
    "Rosuvastatin": "May cause muscle pain or weakness. Requires liver monitoring.",
    "Crestor": "May cause muscle pain or weakness. Requires liver monitoring.",
    "Simvastatin": "Higher risk of muscle damage. Avoid with grapefruit juice.",
    "Zocor": "Higher risk of muscle damage. Avoid with grapefruit juice.",
    "Escitalopram": "May cause nausea, insomnia, or sexual dysfunction.",
    "Lexapro": "May cause nausea, insomnia, or sexual dysfunction.",
    "Sertraline": "May cause diarrhea, nausea, or sexual side effects.",
    "Zoloft": "May cause diarrhea, nausea, or sexual side effects.",
    "Fluoxetine": "May cause anxiety, insomnia, or weight changes.",
    "Prozac": "May cause anxiety, insomnia, or weight changes.",
    "Alprazolam": "Risk of dependency. Can cause drowsiness and impaired coordination.",
    "Xanax": "Risk of dependency. Can cause drowsiness and impaired coordination.",
    "Lorazepam": "May cause sedation and memory problems. Risk of dependence.",
    "Ativan": "May cause sedation and memory problems. Risk of dependence.",
    "Clonazepam": "May cause dizziness or confusion. Not for long-term use.",
    "Klonopin": "May cause dizziness or confusion. Not for long-term use.",
    "Metformin": "May cause stomach upset or rarely, lactic acidosis in kidney issues.",
    "Glucophage": "May cause stomach upset or rarely, lactic acidosis in kidney issues.",
    "Glyburide": "Can cause hypoglycemia (low blood sugar). Weight gain possible.",
    "Glynase": "Can cause hypoglycemia (low blood sugar). Weight gain possible.",
    "Glipizide": "Risk of low blood sugar. Take with first meal of the day.",
    "Glucotrol": "Risk of low blood sugar. Take with first meal of the day.",
    "Omeprazole": "Long-term use may affect magnesium levels or increase fracture risk.",
    "Prilosec": "Long-term use may affect magnesium levels or increase fracture risk.",
    "Famotidine": "Generally well-tolerated. May cause headache or constipation.",
    "Pepcid": "Generally well-tolerated. May cause headache or constipation.",
    "Pantoprazole": "May affect absorption of other medications. Can cause diarrhea.",
    "Protonix": "May affect absorption of other medications. Can cause diarrhea."
}

# Do not combine with database
DO_NOT_COMBINE = {
    "Diphenhydramine": ["Other antihistamines (Cetirizine, Loratadine)", "Alcohol or sedatives"],
    "Benadryl": ["Other antihistamines (Cetirizine, Loratadine)", "Alcohol or sedatives"],
    "Cetirizine": ["Other antihistamines", "MAO inhibitors"],
    "Zyrtec": ["Other antihistamines", "MAO inhibitors"],
    "Loratadine": ["Other antihistamines", "Ketoconazole, erythromycin"],
    "Claritin": ["Other antihistamines", "Ketoconazole, erythromycin"],
    "Ibuprofen": ["Other NSAIDs", "Blood thinners (Warfarin)", "Corticosteroids"],
    "Advil": ["Other NSAIDs", "Blood thinners (Warfarin)", "Corticosteroids"],
    "Naproxen": ["Other NSAIDs", "Blood thinners", "ACE inhibitors"],
    "Aleve": ["Other NSAIDs", "Blood thinners", "ACE inhibitors"],
    "Acetaminophen": ["Alcohol", "Other acetaminophen-containing products"],
    "Tylenol": ["Alcohol", "Other acetaminophen-containing products"],
    "Atorvastatin": ["Grapefruit juice", "Certain antibiotics", "Cyclosporine"],
    "Lipitor": ["Grapefruit juice", "Certain antibiotics", "Cyclosporine"],
    "Rosuvastatin": ["Cyclosporine", "Gemfibrozil", "Warfarin"],
    "Crestor": ["Cyclosporine", "Gemfibrozil", "Warfarin"],
    "Simvastatin": ["Grapefruit juice", "Certain antibiotics", "HIV protease inhibitors"],
    "Zocor": ["Grapefruit juice", "Certain antibiotics", "HIV protease inhibitors"],
    "Escitalopram": ["MAOIs", "Other SSRIs", "Triptans"],
    "Lexapro": ["MAOIs", "Other SSRIs", "Triptans"],
    "Sertraline": ["MAOIs", "Other SSRIs", "St. John's Wort"],
    "Zoloft": ["MAOIs", "Other SSRIs", "St. John's Wort"],
    "Fluoxetine": ["MAOIs", "Thioridazine", "Pimozide"],
    "Prozac": ["MAOIs", "Thioridazine", "Pimozide"],
    "Alprazolam": ["Alcohol", "Opioids", "Other CNS depressants"],
    "Xanax": ["Alcohol", "Opioids", "Other CNS depressants"],
    "Lorazepam": ["Alcohol", "Opioid pain medications", "Anticonvulsants"],
    "Ativan": ["Alcohol", "Opioid pain medications", "Anticonvulsants"],
    "Clonazepam": ["Alcohol", "Opioids", "Other benzodiazepines"],
    "Klonopin": ["Alcohol", "Opioids", "Other benzodiazepines"],
    "Metformin": ["Alcohol", "Iodinated contrast (used in scans)", "Certain kidney medications"],
    "Glucophage": ["Alcohol", "Iodinated contrast (used in scans)", "Certain kidney medications"],
    "Glyburide": ["Beta-blockers", "Corticosteroids", "Niacin"],
    "Glynase": ["Beta-blockers", "Corticosteroids", "Niacin"],
    "Glipizide": ["Beta-blockers", "Diuretics", "NSAIDs"],
    "Glucotrol": ["Beta-blockers", "Diuretics", "NSAIDs"],
    "Omeprazole": ["Clopidogrel (Plavix)", "Certain HIV medications", "St. John's Wort"],
    "Prilosec": ["Clopidogrel (Plavix)", "Certain HIV medications", "St. John's Wort"],
    "Famotidine": ["Itraconazole", "Ketoconazole", "Atazanavir"],
    "Pepcid": ["Itraconazole", "Ketoconazole", "Atazanavir"],
    "Pantoprazole": ["Methotrexate", "Rilpivirine", "Clopidogrel"],
    "Protonix": ["Methotrexate", "Rilpivirine", "Clopidogrel"]
}

def load_medications() -> pd.DataFrame:
    """
    Load the simplified medications database from CSV.
    """
    try:
        # Check if the data directory exists, create if not
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Check if the medications file exists
        if os.path.exists(MEDICATIONS_CSV):
            return pd.read_csv(MEDICATIONS_CSV)
        else:
            print(f"Warning: Medications file not found at {MEDICATIONS_CSV}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error loading medications database: {e}")
        return pd.DataFrame()

def get_medication_info(medication_name: str) -> Optional[Dict]:
    """
    Get information about a specific medication.
    
    Args:
        medication_name: Name of the medication to look up
        
    Returns:
        Dictionary with medication information or None if not found
    """
    df = load_medications()
    
    if df.empty:
        return None
    
    # Case-insensitive search for the medication name
    medication = df[df['Medication Name'].str.lower() == medication_name.lower()]
    
    if not medication.empty:
        return medication.iloc[0].to_dict()
    
    # If no exact match, try partial matching
    medication = df[df['Medication Name'].str.lower().str.contains(medication_name.lower())]
    
    if not medication.empty:
        return medication.iloc[0].to_dict()
    
    return None

def get_insurance_description(insurance_level: str) -> str:
    """
    Get a more detailed description of insurance coverage levels.
    
    Args:
        insurance_level: The insurance level (None, Some, Most, Limited)
        
    Returns:
        A descriptive string about the insurance coverage
    """
    insurance_descriptions = {
        "Most": "Most plans cover this medication, but costs may vary.",
        "Some": "Some plans may offer partial coverage or require prior authorization.",
        "Limited": "Only a few insurance plans cover this medication.",
        "None": "This medication is not covered by insurance. You'll likely pay the full price.",
        "None / Self-pay": "This medication is not covered by insurance. You'll likely pay the full price."
    }
    
    return insurance_descriptions.get(insurance_level, insurance_level)

def find_alternatives(medication_info: Dict, budget: Optional[float] = None, insurance: str = "None / Self-pay", 
                     restrictions: Optional[str] = None) -> List[Dict]:
    """
    Find alternative medications based on the user's criteria.
    
    Args:
        medication_info: Dictionary with original medication information
        budget: Optional budget constraint
        insurance: Insurance coverage level ("None / Self-pay", "Some", "Most")
        restrictions: Optional medical restrictions/allergies
        
    Returns:
        List of alternative medication dictionaries
    """
    df = load_medications()
    
    if df.empty:
        return []
    
    # Get the alternative medication names - multiple alternatives separated by commas
    alternatives_str = medication_info.get('Alternatives', '')
    
    if not alternatives_str:
        return []
    
    # Split the alternatives by comma
    alternative_names = [name.strip() for name in alternatives_str.split(',')]
    
    results = []
    
    # Process each alternative
    for alt_name in alternative_names:
        # Find the alternative in the database
        alternative = df[df['Medication Name'].str.lower() == alt_name.lower()]
        
        if alternative.empty:
            # Try looking for the generic name instead
            alternative = df[df['Generic Name'].str.lower() == alt_name.lower()]
            
        if alternative.empty:
            continue
        
        alt_info = alternative.iloc[0].to_dict()
        
        # Check if this alternative meets the user's criteria
        if budget and alt_info['Avg Cost (USD)'] > budget:
            continue  # Over budget
            
        if restrictions and str(alt_info['Restrictions']).lower() != 'none':
            # Check if any restriction keywords match
            user_restrictions = [r.strip().lower() for r in str(restrictions).split(',')]
            med_restrictions = [r.strip().lower() for r in str(alt_info['Restrictions']).split(',')]
            
            should_skip = False
            for user_r in user_restrictions:
                for med_r in med_restrictions:
                    if user_r in med_r or med_r in user_r:
                        should_skip = True
                        break
                if should_skip:
                    break
                        
            if should_skip:
                continue  # Restriction match found
        
        # Format and add this alternative to results
        alt_name = alt_info['Medication Name']
        
        results.append({
            'name': alt_name,
            'generic_name': alt_info['Generic Name'],
            'drug_class': alt_info['Type/Class'],
            'avg_cost': alt_info['Avg Cost (USD)'],
            'insurance_coverage': alt_info['Insurance Coverage'],
            'insurance_description': get_insurance_description(alt_info['Insurance Coverage']),
            'restrictions': alt_info['Restrictions'],
            'savings': medication_info['Avg Cost (USD)'] - alt_info['Avg Cost (USD)'],
            'potential_risks': get_medication_risks(alt_name),
            'do_not_combine': get_do_not_combine(alt_name)
        })
    
    # Sort by cost (cheapest first)
    results.sort(key=lambda x: x['avg_cost'])
    
    return results

def get_supplement_suggestions(medication_info: Dict) -> List[str]:
    """
    Get supplement suggestions for a medication.
    
    Args:
        medication_info: Dictionary with medication information
        
    Returns:
        List of supplement suggestions
    """
    supplements_str = medication_info.get('Supplement Suggestions', '')
    
    if not supplements_str:
        return []
    
    # Split by comma and strip whitespace
    return [supp.strip() for supp in str(supplements_str).split(',')]

def get_medication_risks(medication_name: str) -> str:
    """
    Get potential risks for a medication.
    
    Args:
        medication_name: Name of the medication
        
    Returns:
        String with potential risks
    """
    # First check by exact name
    risk = MEDICATION_RISKS.get(medication_name, "")
    
    if risk:
        return risk
    
    # If no exact match, try case-insensitive search
    for med_name, med_risk in MEDICATION_RISKS.items():
        if med_name.lower() == medication_name.lower():
            return med_risk
    
    # If still not found, return default risk message
    return "No specific risk information available. All medications have potential side effects."

def get_do_not_combine(medication_name: str) -> List[str]:
    """
    Get list of medications or substances that should not be combined with this medication.
    
    Args:
        medication_name: Name of the medication
        
    Returns:
        List of contraindicated medications/substances
    """
    # First check by exact name
    contraindications = DO_NOT_COMBINE.get(medication_name, [])
    
    if contraindications:
        return contraindications
    
    # If no exact match, try case-insensitive search
    for med_name, med_contra in DO_NOT_COMBINE.items():
        if med_name.lower() == medication_name.lower():
            return med_contra
    
    # If still not found, return empty list
    return []