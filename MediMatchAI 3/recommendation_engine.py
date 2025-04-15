import pandas as pd
import random
from typing import Dict, List, Optional, Union
from medication_db import (
    get_medication_info, 
    get_medication_by_class, 
    get_generic_brand_pairs,
    get_brand_generic_pairs,
    load_medications
)

def identify_drug_class(medication: str) -> Optional[str]:
    """
    Identify the drug class of a medication.
    
    Args:
        medication: Name of the medication
        
    Returns:
        Drug class name or None if not found
    """
    med_info = get_medication_info(medication)
    
    if med_info:
        return med_info['drug_class']
    
    return None

def explain_medication(medication: str) -> str:
    """
    Generate an explanation of what a medication does.
    
    Args:
        medication: Name of the medication
        
    Returns:
        Explanation text
    """
    med_info = get_medication_info(medication)
    
    if med_info:
        return med_info['description']
    
    return "Information not available for this medication."

def format_side_effects(side_effects: str) -> str:
    """
    Format side effects for better readability.
    
    Args:
        side_effects: Side effects as a comma-separated string
        
    Returns:
        Formatted side effects
    """
    if not side_effects:
        return "Information not available"
    
    # Split by commas and format as bullet points
    effects = [effect.strip() for effect in side_effects.split(',')]
    return ", ".join(effects)

def check_if_generic_available(medication: str) -> Dict:
    """
    Check if a generic version is available for a brand-name medication.
    
    Args:
        medication: Name of the medication
        
    Returns:
        Dictionary with generic information if available
    """
    med_info = get_medication_info(medication)
    
    if not med_info:
        return {}
    
    # If it's already a generic, return empty
    if not med_info['is_brand']:
        return {}
    
    # Check for generic alternatives
    brand_generic_map = get_brand_generic_pairs()
    
    if medication in brand_generic_map:
        generic_name = brand_generic_map[medication]
        generic_info = get_medication_info(generic_name)
        
        if generic_info:
            savings = med_info['avg_cost'] - generic_info['avg_cost']
            savings_percent = (savings / med_info['avg_cost']) * 100
            
            return {
                'name': generic_info['name'],
                'avg_cost': generic_info['avg_cost'],
                'savings': savings,
                'savings_percent': savings_percent,
                'recommendation_type': "Generic version available",
                'explanation': f"This is a bioequivalent generic medication containing the same active ingredient as {medication}. It works the same way but costs {savings_percent:.0f}% less.",
                'side_effects': format_side_effects(generic_info['side_effects']),
                'source': generic_info['source'],
                'availability': "Available at most pharmacies"
            }
    
    return {}

def find_cheaper_alternatives(medication: str, drug_class: str) -> List[Dict]:
    """
    Find cheaper alternatives in the same drug class.
    
    Args:
        medication: Name of the medication
        drug_class: Drug class of the medication
        
    Returns:
        List of dictionaries with alternative medications
    """
    med_info = get_medication_info(medication)
    
    if not med_info:
        return []
    
    # Get medications in the same class
    class_medications = get_medication_by_class(drug_class)
    
    # Filter out the original medication
    alternatives = [med for med in class_medications if med['name'].lower() != medication.lower()]
    
    # Filter for cheaper alternatives
    cheaper_alternatives = [
        med for med in alternatives 
        if med['avg_cost'] < med_info['avg_cost']
    ]
    
    # Sort by cost (cheapest first)
    cheaper_alternatives.sort(key=lambda x: x['avg_cost'])
    
    # Format the alternatives for display
    formatted_alternatives = []
    for alt in cheaper_alternatives[:3]:  # Limit to top 3 cheapest
        savings = med_info['avg_cost'] - alt['avg_cost']
        savings_percent = (savings / med_info['avg_cost']) * 100
        
        formatted_alt = {
            'name': alt['name'],
            'avg_cost': alt['avg_cost'],
            'savings': savings,
            'savings_percent': savings_percent,
            'recommendation_type': "Cheapest with similar effect",
            'explanation': f"This medication is in the same drug class ({drug_class}) as {medication} and may provide similar therapeutic benefits. It costs {savings_percent:.0f}% less than your prescribed medication.",
            'side_effects': format_side_effects(alt['side_effects']),
            'source': alt['source'],
            'availability': "Available at most pharmacies"
        }
        
        formatted_alternatives.append(formatted_alt)
    
    return formatted_alternatives

def suggest_alternative_treatments(medication: str) -> List[Dict]:
    """
    Suggest evidence-based alternative treatments or supplements.
    
    Args:
        medication: Name of the medication
        
    Returns:
        List of dictionaries with alternative treatments
    """
    med_info = get_medication_info(medication)
    
    if not med_info:
        return []
    
    drug_class = med_info['drug_class']
    
    # Dictionary mapping drug classes to alternative treatments
    alternative_treatments = {
        'Statin': [
            {
                'name': 'Plant Sterols and Stanols',
                'type': 'Dietary Supplement',
                'avg_cost': 30.00,
                'explanation': 'Plant sterols and stanols are naturally occurring compounds that can help lower cholesterol by blocking its absorption. Studies suggest they can reduce LDL cholesterol by 5-15% when consumed as part of a heart-healthy diet.',
                'warning': 'Not as effective as statins for significant cholesterol reduction. Should be used as a complementary approach, not a replacement for prescribed medication.',
                'source': 'American Heart Association, Mayo Clinic'
            },
            {
                'name': 'Red Yeast Rice',
                'type': 'Dietary Supplement',
                'avg_cost': 20.00,
                'explanation': 'Red yeast rice naturally contains compounds similar to lovastatin. Some studies show it can lower cholesterol by 20-30% in some people.',
                'warning': 'Quality and active compound amounts vary widely between products. May cause the same side effects as statins. Not regulated by the FDA for consistency.',
                'source': 'National Center for Complementary and Integrative Health (NCCIH)'
            }
        ],
        'SSRI': [
            {
                'name': 'Omega-3 Fatty Acids',
                'type': 'Dietary Supplement',
                'avg_cost': 25.00,
                'explanation': 'Some research suggests omega-3 supplements may help alleviate mild to moderate depression symptoms. The EPA form appears to be more effective than DHA for mood improvement.',
                'warning': 'Effects are typically modest. Should not replace prescribed antidepressants for clinical depression. Consult your healthcare provider before using.',
                'source': 'Harvard Medical School, JAMA Psychiatry'
            },
            {
                'name': 'Regular Exercise',
                'type': 'Lifestyle Intervention',
                'avg_cost': 0.00,
                'explanation': 'Regular physical activity has been shown to reduce symptoms of depression and anxiety. For mild to moderate depression, research suggests exercise can be as effective as medication in some cases.',
                'warning': 'Should be used as a complementary approach for most cases of clinical depression, not as the sole treatment.',
                'source': 'American Psychological Association, Mayo Clinic'
            }
        ],
        'PPI': [
            {
                'name': 'Dietary Modifications',
                'type': 'Lifestyle Intervention',
                'avg_cost': 0.00,
                'explanation': 'Avoiding trigger foods (spicy, acidic, fatty), eating smaller meals, not eating before bedtime, and weight loss if needed can significantly reduce acid reflux symptoms.',
                'warning': 'May not be sufficient for severe GERD or conditions requiring acid suppression. Consult your healthcare provider before discontinuing prescribed medication.',
                'source': 'American College of Gastroenterology, Mayo Clinic'
            },
            {
                'name': 'Deglycyrrhizinated Licorice (DGL)',
                'type': 'Dietary Supplement',
                'avg_cost': 15.00,
                'explanation': 'DGL is a form of licorice root that has had a potentially dangerous compound (glycyrrhizin) removed. It may help protect the stomach lining and reduce heartburn symptoms.',
                'warning': 'Limited scientific evidence compared to conventional treatments. Should not replace prescribed medication without healthcare provider guidance.',
                'source': 'National Center for Complementary and Integrative Health (NCCIH)'
            }
        ],
        'NSAID': [
            {
                'name': 'Turmeric/Curcumin',
                'type': 'Dietary Supplement',
                'avg_cost': 20.00,
                'explanation': 'Curcumin, the active compound in turmeric, has anti-inflammatory properties. Some studies suggest it may help reduce pain and inflammation in conditions like arthritis.',
                'warning': 'Has poor bioavailability unless formulated with enhancers like piperine (black pepper extract). Effects are usually modest compared to NSAIDs.',
                'source': 'Arthritis Foundation, Journal of Medicinal Food'
            },
            {
                'name': 'Topical Capsaicin',
                'type': 'Topical Treatment',
                'avg_cost': 15.00,
                'explanation': 'Capsaicin, derived from chili peppers, can help relieve pain by reducing Substance P, a pain messenger. Effective for some types of muscle and joint pain.',
                'warning': 'Causes burning sensation upon application that decreases with continued use. Only works for localized pain conditions.',
                'source': 'American Academy of Family Physicians, Cochrane Database of Systematic Reviews'
            }
        ],
        'Antihistamine': [
            {
                'name': 'Nasal Irrigation',
                'type': 'Home Remedy',
                'avg_cost': 10.00,
                'explanation': 'Saline nasal irrigation (such as with a neti pot) helps flush allergens from nasal passages and thin mucus. Shown to reduce allergy symptoms and need for medications in some patients.',
                'warning': 'Use only distilled, sterile, or previously boiled water. Clean devices regularly to prevent infection.',
                'source': 'American Academy of Allergy, Asthma & Immunology'
            },
            {
                'name': 'Butterbur Extract',
                'type': 'Herbal Supplement',
                'avg_cost': 30.00,
                'explanation': 'Some studies suggest butterbur extract can be as effective as antihistamines for allergic rhinitis symptoms without causing drowsiness.',
                'warning': 'Only use products labeled "PA-free" (pyrrolizidine alkaloids removed), as these compounds can damage the liver. Not recommended for long-term use.',
                'source': 'National Center for Complementary and Integrative Health (NCCIH)'
            }
        ],
        'Biguanide': [
            {
                'name': 'Dietary Changes & Exercise',
                'type': 'Lifestyle Intervention',
                'avg_cost': 0.00,
                'explanation': 'A low-carbohydrate diet combined with regular physical activity can significantly improve blood glucose control. In some cases of early type 2 diabetes, lifestyle changes alone can achieve similar results to medication.',
                'warning': 'Should be implemented under medical supervision. Many patients will still require medication in addition to lifestyle changes.',
                'source': 'American Diabetes Association, New England Journal of Medicine'
            },
            {
                'name': 'Berberine',
                'type': 'Dietary Supplement',
                'avg_cost': 25.00,
                'explanation': 'Berberine is a compound found in several plants. Some clinical trials suggest it may lower blood glucose levels through mechanisms similar to metformin.',
                'warning': 'Not FDA-approved for diabetes treatment. Quality and potency vary between products. Potential for drug interactions.',
                'source': 'Journal of Ethnopharmacology, Metabolism'
            }
        ]
    }
    
    # Return alternatives for the specific drug class if available
    if drug_class in alternative_treatments:
        results = []
        for alt in alternative_treatments[drug_class]:
            alt_with_type = alt.copy()
            alt_with_type['recommendation_type'] = "Alternative treatment"
            results.append(alt_with_type)
        return results
    
    return []

def generate_recommendations(
    medication: str,
    budget: Optional[float] = None,
    insurance: str = "None/Self-pay",
    allergies: Optional[str] = None,
    pharmacy: str = "Any",
    include_holistic: bool = False
) -> List[Dict]:
    """
    Generate medication recommendations based on user inputs.
    
    Args:
        medication: The prescribed medication
        budget: Monthly budget constraint (optional)
        insurance: Insurance provider (optional)
        allergies: Allergies or restrictions (optional)
        pharmacy: Preferred pharmacy (optional)
        include_holistic: Whether to include holistic/alternative options
        
    Returns:
        List of recommendation dictionaries
    """
    recommendations = []
    
    # Check if medication exists in our database
    med_info = get_medication_info(medication)
    
    if not med_info:
        return []
    
    # Identify drug class
    drug_class = identify_drug_class(medication)
    
    if not drug_class:
        return []
    
    # Check if generic is available (if prescribed medication is brand name)
    if med_info['is_brand']:
        generic = check_if_generic_available(medication)
        if generic:
            recommendations.append(generic)
    
    # Find cheaper alternatives in the same drug class
    cheaper_alternatives = find_cheaper_alternatives(medication, drug_class)
    recommendations.extend(cheaper_alternatives)
    
    # Add alternative treatments if requested
    if include_holistic:
        alternative_treatments = suggest_alternative_treatments(medication)
        recommendations.extend(alternative_treatments)
    
    # Filter by budget if provided
    if budget and budget > 0:
        recommendations = [rec for rec in recommendations if rec['avg_cost'] <= budget]
    
    # Filter by allergies if provided
    if allergies:
        # This is a simplified implementation. A real system would need a more sophisticated
        # allergy checking mechanism against medication ingredients
        allergy_terms = [a.strip().lower() for a in allergies.split(',')]
        filtered_recs = []
        
        for rec in recommendations:
            # Skip if any allergy term appears in side effects or explanation
            should_skip = any(
                term in rec.get('side_effects', '').lower() or 
                term in rec.get('explanation', '').lower()
                for term in allergy_terms
            )
            
            if not should_skip:
                filtered_recs.append(rec)
        
        recommendations = filtered_recs
    
    # Sort by cost (cheapest first)
    recommendations.sort(key=lambda x: x['avg_cost'])
    
    # Limit to top 5 recommendations
    return recommendations[:5]
