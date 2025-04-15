

from typing import Dict, List, Optional, Tuple

class SimpleAssistant:
    """
    A lightweight rule-based assistant for the MediMatch AI application.
    """
    
    def __init__(self):
        # Common questions that users might ask
        self.common_questions = [
            "What's the difference between this and the alternative?",
            "How much can I save with the cheaper option?",
            "Will this work without insurance?",
            "What does this medication treat?",
            "Are supplements helpful?",
            "Why was no alternative found?",
            "Can I drink alcohol with this?",
            "Can I mix this with other medications?",
            "Is it safe to take with supplements?"
        ]
        
        # Medication and alcohol interaction database
        self.alcohol_interactions = {
            "zoloft": "⚠️ **Avoid alcohol with Zoloft.** Alcohol can increase side effects like drowsiness, dizziness, and difficulty concentrating. It may also worsen depression symptoms.",
            "xanax": "⚠️ **Do not mix Xanax with alcohol.** This combination can cause dangerous levels of sedation, respiratory depression, and even be life-threatening.",
            "prozac": "⚠️ **Avoid alcohol with Prozac.** This combination can increase drowsiness and impair your thinking and reactions.",
            "advil": "⚠️ **Use caution with alcohol and Advil.** Both can irritate the stomach lining, increasing the risk of ulcers and stomach bleeding.",
            "tylenol": "⚠️ **Limit alcohol with Tylenol.** Regular alcohol use while taking Tylenol (acetaminophen) increases the risk of liver damage.",
            "lisinopril": "⚠️ **Alcohol may enhance the blood-pressure-lowering effect** of Lisinopril, causing dizziness or fainting.",
            "lipitor": "✅ **Occasional alcohol is generally considered safe** with Lipitor, but heavy drinking may increase side effect risks.",
            "metformin": "⚠️ **Avoid alcohol with Metformin.** This combination increases the risk of lactic acidosis, a serious condition.",
            "prednisone": "⚠️ **Avoid alcohol with Prednisone.** Both can irritate the stomach and increase the risk of ulcers.",
            "amoxicillin": "⚠️ **Moderate alcohol consumption is unlikely to cause problems** with Amoxicillin, but alcohol may slow your healing process."
        }
        
        # Drug interaction database (simplified)
        self.drug_interactions = {
            "xanax": {
                "advil": "These can generally be taken together. No major interactions are known.",
                "tylenol": "These can generally be taken together. No major interactions are known.",
                "zoloft": "⚠️ Taking these together may increase side effects like drowsiness. Use caution and consult your doctor.",
                "benadryl": "⚠️ This combination can cause extreme drowsiness. Avoid tasks requiring alertness."
            },
            "zoloft": {
                "advil": "These can generally be taken together. No major interactions are known.",
                "tylenol": "These can generally be taken together. No major interactions are known.",
                "xanax": "⚠️ Taking these together may increase side effects like drowsiness. Use caution and consult your doctor.",
                "aspirin": "⚠️ This combination may increase bleeding risk. Consult your doctor."
            },
            "advil": {
                "tylenol": "These can generally be taken together and are often used for different types of pain.",
                "xanax": "These can generally be taken together. No major interactions are known.",
                "lisinopril": "⚠️ This combination may reduce the effectiveness of blood pressure medication."
            }
        }
        
        # Supplement interaction database
        self.supplement_interactions = {
            "turmeric": {
                "xanax": "No major known issues, but turmeric might increase drowsiness effects. Use caution.",
                "zoloft": "No major known interactions, but always inform your doctor about supplements you take.",
                "advil": "⚠️ Both have blood-thinning effects. May increase bleeding risk.",
                "default": "No known major interactions, but always consult your doctor before combining supplements with medications."
            },
            "omega-3": {
                "advil": "⚠️ Both have blood-thinning effects. May increase bleeding risk.",
                "zoloft": "Generally considered safe together, but inform your doctor.",
                "default": "Generally considered safe, but inform your doctor of all supplements you take."
            },
            "magnesium": {
                "lisinopril": "⚠️ May enhance blood pressure lowering effects. Monitor your blood pressure if combining these.",
                "default": "Generally safe with most medications, but take 2 hours apart from other medications for best absorption."
            },
            "vitamin d": {
                "default": "Generally safe with most medications. No significant interactions typically reported."
            },
            "st. john's wort": {
                "zoloft": "⚠️ **DO NOT COMBINE.** Can cause serotonin syndrome, a potentially dangerous condition.",
                "xanax": "⚠️ May reduce the effectiveness of Xanax. Not recommended to combine.",
                "default": "⚠️ St. John's Wort interacts with many medications. Always consult your doctor before using."
            }
        }
    
        # Common questions and responses
        self.responses = {
            "cheaper": [
                "Generic medications are usually cheaper because they don't have the marketing and research costs that brand-name drugs do.",
                "This medication is cheaper because multiple companies can produce it, creating competition that lowers prices.",
                "Once a drug's patent expires, other companies can make generic versions, which typically cost 80-85% less."
            ],
            "safe": [
                "Yes, the FDA requires generic medications to be as safe and effective as their brand-name counterparts.",
                "Alternatives within the same drug class are generally considered safe, but may have slightly different side effects.",
                "All FDA-approved medications meet safety standards, though individual responses may vary."
            ],
            "supplement": {
                "turmeric": "Turmeric contains curcumin, which has anti-inflammatory properties that may help with pain and inflammation similar to NSAIDs, but usually with milder effects.",
                "omega-3": "Omega-3 fatty acids have anti-inflammatory properties that may help reduce pain and inflammation. They're found in fish oil and some plant sources.",
                "red yeast rice": "Red yeast rice naturally contains compounds similar to statins and may help lower cholesterol, though effects are typically milder than prescription medications.",
                "coq10": "CoQ10 is often recommended alongside statins because statins can deplete this compound in the body. It may help reduce muscle pain associated with statins.",
                "st. john's wort": "St. John's Wort may help with mild depression, but it can interact dangerously with SSRIs and many other medications. Always consult a doctor before using.",
                "chamomile": "Chamomile tea has mild calming properties that may help with anxiety, though effects are much gentler than prescription anti-anxiety medications.",
                "meditation": "Regular meditation practice has been shown to help reduce anxiety and stress through mindfulness techniques.",
                "quercetin": "Quercetin is a natural antihistamine that may help reduce allergic responses, though it's typically less potent than prescription antihistamines.",
                "saline rinse": "Saline nasal rinses can help flush allergens from the nasal passages, reducing symptoms of allergies and congestion.",
                "cinnamon": "Some studies suggest cinnamon may help improve insulin sensitivity, though effects are mild compared to prescription diabetes medications.",
                "low-carb diet": "Reducing carbohydrate intake can help manage blood sugar levels by decreasing the amount of glucose entering the bloodstream.",
                "ginger tea": "Ginger has natural anti-nausea properties and may help soothe digestive discomfort associated with acid reflux.",
                "elevate head": "Elevating the head during sleep can help prevent stomach acid from flowing back into the esophagus, reducing reflux symptoms."
            }
        }
        
        # Information about drug classes
        self.drug_classes = {
            "nsaid": "NSAIDs (Non-Steroidal Anti-Inflammatory Drugs) reduce pain, fever, and inflammation by blocking certain enzymes in the body.",
            "statin": "Statins lower cholesterol by blocking an enzyme that the liver uses to make cholesterol.",
            "ssri": "SSRIs (Selective Serotonin Reuptake Inhibitors) are antidepressants that increase serotonin levels in the brain by blocking its reabsorption.",
            "benzodiazepine": "Benzodiazepines are sedatives that work by enhancing the effect of the GABA neurotransmitter, producing calming effects.",
            "antihistamine": "Antihistamines block the action of histamine, a substance in the body that causes allergic symptoms.",
            "antidiabetic": "Antidiabetic medications help control blood sugar levels in people with diabetes through various mechanisms.",
            "ppi": "Proton Pump Inhibitors (PPIs) reduce stomach acid production by blocking the enzymes that produce acid."
        }
    
    def answer_question(self, question: str, medication_info: Optional[Dict] = None, 
                        alternative_info: Optional[Dict] = None) -> str:
        """
        Provide an answer to the user's question based on rule-based matching.
        
        Args:
            question: The user's question
            medication_info: Information about the original medication (optional)
            alternative_info: Information about the alternative medication (optional)
            
        Returns:
            A text response to the question
        """
        question_lower = question.lower()
        
        # Match common pre-defined questions
        if "difference between" in question_lower and medication_info and alternative_info:
            drug_class = medication_info.get('Type/Class', '').lower()
            alt_class = alternative_info.get('drug_class', '').lower()
            
            if drug_class == alt_class:
                return f"Both {medication_info['Medication Name']} and {alternative_info['name']} belong to the same drug class ({drug_class}) and work in similar ways. The main differences are typically in cost, potential side effects, and insurance coverage. {alternative_info['name']} costs ${alternative_info['avg_cost']} per month while {medication_info['Medication Name']} costs ${medication_info['Avg Cost (USD)']} per month."
            else:
                return f"{medication_info['Medication Name']} belongs to the {drug_class} class, while {alternative_info['name']} is a {alt_class}. Although they treat similar conditions, they may work through different mechanisms."
        
        # Handle "how much can I save" question
        elif "save" in question_lower and "cheaper" in question_lower and medication_info and alternative_info:
            savings = medication_info['Avg Cost (USD)'] - alternative_info['avg_cost']
            savings_percent = (savings / medication_info['Avg Cost (USD)']) * 100
            return f"By switching from {medication_info['Medication Name']} to {alternative_info['name']}, you could save ${savings:.2f} per month (about {savings_percent:.0f}% of the original cost)."
        
        # Handle "will this work without insurance" question
        elif "without insurance" in question_lower:
            if alternative_info:
                response = f"Yes, you can purchase {alternative_info['name']} without insurance for about ${alternative_info['avg_cost']} per month. "
                response += f"This is {alternative_info['insurance_description']}"
                return response
            elif medication_info:
                response = f"Yes, you can purchase {medication_info['Medication Name']} without insurance for about ${medication_info['Avg Cost (USD)']} per month. "
                response += f"This may be expensive compared to alternatives."
                return response
            return "All medications can be purchased without insurance, but costs will vary. Generic medications are typically much more affordable than brand-name drugs."
        
        # Handle "what does this medication treat" question
        elif "what does" in question_lower and "treat" in question_lower:
            med_to_describe = medication_info
            if not med_to_describe and alternative_info:
                med_to_describe = alternative_info
                
            if med_to_describe:
                drug_class = med_to_describe.get('Type/Class', '').lower()
                name = med_to_describe.get('Medication Name', '') or med_to_describe.get('name', '')
                
                for class_key, description in self.drug_classes.items():
                    if class_key in drug_class.lower():
                        return f"{name} is a {drug_class}. {description}"
                
                return f"{name} is used to treat conditions related to {drug_class}."
            
            return "Please specify which medication you'd like to know about."
        
        # Handle "are supplements helpful" question
        elif "supplement" in question_lower and "helpful" in question_lower:
            if medication_info:
                supplements = str(medication_info.get('Supplement Suggestions', '')).lower()
                if supplements:
                    return f"Some supplements like {medication_info['Supplement Suggestions']} may help with your condition, but they're typically less effective than prescription medications. Always consult with your healthcare provider before starting any supplements, especially alongside medication."
            
            return "Supplements may offer some benefits, but they're typically less potent than prescription medications and aren't FDA-approved to treat medical conditions. Always discuss supplements with your healthcare provider before use, as some can interact with medications."
        
        # Handle "why was no alternative found" question
        elif "no alternative" in question_lower or "why wasn't" in question_lower:
            if medication_info:
                return f"Possible reasons include: 1) Your budget may be lower than the cost of alternatives, 2) You may have a restriction or allergy that conflicts with available alternatives, or 3) The database may not contain all possible alternatives for {medication_info['Medication Name']}. Try adjusting your search criteria or consult your healthcare provider."
            
            return "Possible reasons include budget constraints, medical restrictions, or limitations in our database. Try adjusting your search criteria or consult your healthcare provider."
        
        # Handle questions about why alternatives are cheaper
        elif any(term in question_lower for term in ["why cheaper", "why less expensive", "why cost less", "price difference"]):
            return self.responses["cheaper"][0]
        
        # Handle questions about safety
        elif any(term in question_lower for term in ["safe", "safety", "side effect", "dangerous"]):
            return self.responses["safe"][0]
        
        # Handle questions about drug classes
        elif "what is" in question_lower and medication_info:
            drug_class = medication_info.get('Type/Class', '').lower()
            
            for class_key, description in self.drug_classes.items():
                if class_key in drug_class.lower():
                    return description
                    
        # Handle questions about alcohol interactions
        elif any(term in question_lower for term in ["alcohol", "drink", "beer", "wine"]):
            if medication_info:
                med_name = medication_info.get('Medication Name', '').lower()
                generic_name = medication_info.get('Generic Name', '').lower()
                
                # Check for the medication in our alcohol interactions database
                for med_key in self.alcohol_interactions.keys():
                    if med_key in med_name or med_key in generic_name:
                        return self.alcohol_interactions[med_key]
                
                # Generic response if medication not found in database
                return "⚠️ **Use caution when mixing this medication with alcohol.** Alcohol may increase side effects or reduce medication effectiveness. Always consult your healthcare provider about alcohol consumption while taking any medication."
            
            return "To get information about alcohol interactions, please first search for a specific medication."
            
        # Handle questions about medication interactions
        elif any(term in question_lower for term in ["mix", "combine", "together", "interaction", "conflict"]):
            if medication_info:
                med_name = medication_info.get('Medication Name', '').lower()
                generic_name = medication_info.get('Generic Name', '').lower()
                
                # Extract the other medication name from the question
                other_med = None
                
                # List of common medications to check against
                common_meds = ["advil", "tylenol", "xanax", "zoloft", "prozac", "aspirin", "benadryl", "lisinopril"]
                
                for med in common_meds:
                    if med in question_lower:
                        other_med = med
                        break
                
                if other_med:
                    # Check if we have an interaction for this combination
                    med_keys = [key for key in self.drug_interactions.keys() if key in med_name or key in generic_name]
                    
                    if med_keys:
                        med_key = med_keys[0]
                        if other_med in self.drug_interactions[med_key]:
                            return f"**{medication_info['Medication Name']} + {other_med.capitalize()}:** {self.drug_interactions[med_key][other_med]}"
                    
                    # Reverse lookup in case the other medication is the primary one in our database
                    if other_med in self.drug_interactions:
                        other_med_interactions = self.drug_interactions[other_med]
                        for key in other_med_interactions.keys():
                            if key in med_name or key in generic_name:
                                return f"**{medication_info['Medication Name']} + {other_med.capitalize()}:** {other_med_interactions[key]}"
                    
                    # Generic answer if no specific interaction found
                    return f"I don't have specific information about interactions between {medication_info['Medication Name']} and {other_med.capitalize()}. Always consult your healthcare provider or pharmacist before combining medications."
                
                return "Please specify which medication you're asking about combining with this one. For example, 'Can I take this with Advil?'"
            
            return "To get information about medication interactions, please first search for a specific medication."
        
        # Handle specific supplement interaction questions
        elif any(term in question_lower for term in ["turmeric", "omega", "vitamin", "zinc", "magnesium", "st. john", "st john"]):
            if medication_info:
                med_name = medication_info.get('Medication Name', '').lower()
                generic_name = medication_info.get('Generic Name', '').lower()
                
                # Identify which supplement was asked about
                supplement = None
                for supp in self.supplement_interactions.keys():
                    if supp in question_lower:
                        supplement = supp
                        break
                
                if supplement:
                    # Check if we have specific interaction info
                    for med_key in self.supplement_interactions[supplement].keys():
                        if med_key in med_name or med_key in generic_name:
                            return f"**{medication_info['Medication Name']} + {supplement.capitalize()}:** {self.supplement_interactions[supplement][med_key]}"
                    
                    # Return default response for this supplement if no specific interaction
                    if "default" in self.supplement_interactions[supplement]:
                        return f"**{medication_info['Medication Name']} + {supplement.capitalize()}:** {self.supplement_interactions[supplement]['default']}"
                
                return f"I don't have specific information about interactions between {medication_info['Medication Name']} and this supplement. Always consult your healthcare provider before combining medications with supplements."
            
            return "To get information about supplement interactions, please first search for a specific medication."
        
        # Handle questions about supplements (general)
        elif any(term in question_lower for term in ["supplement", "natural", "alternative treatment"]):
            if medication_info:
                supplements = str(medication_info.get('Supplement Suggestions', '')).lower()
                
                for supp_key, description in self.responses["supplement"].items():
                    if supp_key.lower() in supplements.lower():
                        return description
            
            return "Various supplements or lifestyle changes might help manage your condition alongside medication. Always discuss these with your healthcare provider first."
        
        # Default response if no specific match
        return "I'm a simple assistant designed to help with basic medication questions. For specific medical advice, please consult your healthcare provider."


    def explain_recommendation(self, original_med: Dict, alternative_med: Dict) -> str:
        savings = original_med['Avg Cost (USD)'] - alternative_med['avg_cost']
        savings_percent = (savings / original_med['Avg Cost (USD)']) * 100

        explanation = (
            f"I recommend **{alternative_med['name']} ({alternative_med['generic_name']})** "
            f"as an alternative to **{original_med['Medication Name']}**.\n\n"
            #  ↓—— add a back‑slash before each $
            f"It costs **\\${alternative_med['avg_cost']:.2f} per month**, which is "
            f"**\\${savings:.2f} less** than **{original_med['Medication Name']}** "
            f"(a savings of about **{savings_percent:.0f}%**).\n\n"
        )



        insurance_level = alternative_med.get('insurance_coverage', 'None')
        if insurance_level == "Most":
            savings_min = max(5, int(alternative_med['avg_cost'] * 0.4))
            savings_max = max(10, int(alternative_med['avg_cost'] * 0.7))
            explanation += f"**Insurance Coverage:** Most plans cover this medication. You may save **${savings_min}–${savings_max}** per month with insurance.\n\n"
        elif insurance_level == "Some":
            savings_min = max(3, int(alternative_med['avg_cost'] * 0.2))
            savings_max = max(6, int(alternative_med['avg_cost'] * 0.4))
            explanation += f"**Insurance Coverage:** Some plans offer partial coverage. Estimated savings: **${savings_min}–${savings_max}** monthly.\n\n"
        elif insurance_level == "Limited":
            explanation += "**Insurance Coverage:** Only a few plans cover this drug. Savings may be small or none.\n\n"
        else:
            explanation += "**Insurance Coverage:** This medication is not covered. Expect to pay the full price out of pocket.\n\n"

        explanation += f"Both medications are in the **{original_med['Type/Class']}** class and work in similar ways."

        return explanation
