import streamlit as st
import pandas as pd
import os
from medication_db import get_medication_info, get_medication_by_class, search_medications
from recommendation_engine import generate_recommendations, explain_medication
from pdf_generator import generate_pdf
from utils import display_educational_content, display_resources

# Set page configuration
st.set_page_config(
    page_title="MediMatch AI - Smarter Medication Options",
    page_icon="🏥",
    layout="wide",
)

# Initialize session state variables if they don't exist
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'original_medication' not in st.session_state:
    st.session_state.original_medication = None
if 'budget' not in st.session_state:
    st.session_state.budget = None
if 'insurance' not in st.session_state:
    st.session_state.insurance = None
if 'allergies' not in st.session_state:
    st.session_state.allergies = None
if 'pharmacy' not in st.session_state:
    st.session_state.pharmacy = None

# Function to reset the application state
def reset_app():
    st.session_state.recommendations = None
    st.session_state.original_medication = None
    st.session_state.budget = None
    st.session_state.insurance = None
    st.session_state.allergies = None
    st.session_state.pharmacy = None
    st.rerun()

# Main app header
st.title("🏥 MediMatch AI")
st.subheader("Find Smarter Medication Options for Your Prescriptions")

# App description
st.markdown("""
This tool helps you find better, more affordable, and personalized medicine options for your prescriptions.
Enter your prescription details below to get personalized recommendations.
""")

# Sidebar for navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Go to", ["Home", "Educational Resources", "About"])
    
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("""
    1. Enter your prescription details
    2. Review alternative options
    3. Get explanations and cost comparisons
    4. Save or share your results
    """)
    
    if st.button("Start Over"):
        reset_app()

# Main content based on selected page
if page == "Home":
    # Check if recommendations already exist
    if st.session_state.recommendations is None:
        # Input form
        st.header("Enter Your Prescription Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            medication = st.text_input("Prescribed Medication Name*", help="Enter the exact name of the medication prescribed to you")
            budget = st.number_input("Monthly Budget (USD)", min_value=0.0, help="Optional: What's your maximum monthly budget for this medication?")
            insurance = st.selectbox(
                "Insurance Provider",
                ["None/Self-pay", "Medicare", "Medicaid", "Blue Cross Blue Shield", "Aetna", "Cigna", "UnitedHealthcare", "Humana", "Kaiser Permanente", "Other"],
                help="Select your insurance provider or 'None' if you're paying out of pocket"
            )
        
        with col2:
            allergies = st.text_area("Allergies or Restrictions", help="List any allergies or dietary restrictions (e.g., no lactose, vegetarian capsule)")
            pharmacy = st.selectbox(
                "Preferred Pharmacy",
                ["Any", "CVS", "Walgreens", "Walmart", "Rite Aid", "Costco", "Sam's Club", "Local/Independent"],
                help="Optional: Select your preferred pharmacy for local results"
            )
            holistic = st.checkbox("I'm interested in supplements or lifestyle alternatives", help="Check this to see evidence-based complementary options")
        
        submit = st.button("Find Alternatives", type="primary")
        
        if submit:
            if not medication:
                st.error("Please enter a medication name to continue.")
            else:
                # Save inputs to session state
                st.session_state.original_medication = medication
                st.session_state.budget = budget
                st.session_state.insurance = insurance
                st.session_state.allergies = allergies
                st.session_state.pharmacy = pharmacy
                
                # Check if medication exists in our database
                med_info = get_medication_info(medication)
                
                if med_info is None:
                    st.error(f"We couldn't find '{medication}' in our database. Please check the spelling or try a different medication.")
                else:
                    # Show loading indicator while generating recommendations
                    with st.spinner("Analyzing alternatives and generating recommendations..."):
                        # Generate recommendations based on inputs
                        recommendations = generate_recommendations(
                            medication,
                            budget,
                            insurance,
                            allergies,
                            pharmacy,
                            holistic
                        )
                        
                        if recommendations:
                            st.session_state.recommendations = recommendations
                            st.rerun()
                        else:
                            st.error("We couldn't generate recommendations for this medication. Please try again or contact support.")
    
    else:
        # Display recommendations
        st.header(f"Medication Alternatives for {st.session_state.original_medication}")
        
        # Original medication information
        med_info = get_medication_info(st.session_state.original_medication)
        
        with st.expander("About Your Prescribed Medication", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader(med_info['name'])
                st.markdown(f"**Drug Class:** {med_info['drug_class']}")
                st.markdown(f"**Purpose:** {med_info['description']}")
                st.markdown(f"**Average Monthly Cost:** ${med_info['avg_cost']:.2f}")
                st.markdown(f"**Common Side Effects:** {med_info['side_effects']}")
                st.markdown(f"**Source:** {med_info['source']}")
            
            with col2:
                # Insurance and budget information
                st.markdown("### Your Details")
                st.markdown(f"**Insurance:** {st.session_state.insurance}")
                if st.session_state.budget:
                    st.markdown(f"**Budget:** ${st.session_state.budget:.2f}/month")
                else:
                    st.markdown("**Budget:** Not specified")
                
                if st.session_state.allergies:
                    st.markdown(f"**Restrictions:** {st.session_state.allergies}")
        
        # Recommended alternatives
        st.markdown("## Recommended Alternatives")
        
        # Create tabs for different categories of recommendations
        tabs = st.tabs(["All Options", "Generics", "Affordability", "Alternative Treatments"])
        
        with tabs[0]:
            for i, rec in enumerate(st.session_state.recommendations):
                with st.container():
                    st.markdown(f"### {i+1}. {rec['name']} - {rec['recommendation_type']}")
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Average Monthly Cost:** ${rec['avg_cost']:.2f}")
                        if 'savings' in rec:
                            st.markdown(f"**Potential Savings:** ${rec['savings']:.2f}/month")
                        
                        st.markdown(f"**Why We Recommend This:**")
                        st.markdown(rec['explanation'])
                        
                        if 'availability' in rec:
                            st.markdown(f"**Availability:** {rec['availability']}")
                        
                        st.markdown(f"**Side Effects:** {rec['side_effects']}")
                        st.markdown(f"**Source:** {rec['source']}")
                    
                    with col2:
                        st.markdown("### Cost Comparison")
                        # Create a simple bar chart for cost comparison
                        data = {
                            'Medication': [med_info['name'], rec['name']],
                            'Monthly Cost': [med_info['avg_cost'], rec['avg_cost']]
                        }
                        chart_data = pd.DataFrame(data)
                        st.bar_chart(chart_data.set_index('Medication'))
                    
                    st.markdown("---")
        
        with tabs[1]:
            # Filter to show only generic alternatives
            generics = [rec for rec in st.session_state.recommendations if rec['recommendation_type'] == "Generic version available"]
            
            if generics:
                for i, rec in enumerate(generics):
                    with st.container():
                        st.markdown(f"### {i+1}. {rec['name']}")
                        
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Average Monthly Cost:** ${rec['avg_cost']:.2f}")
                            if 'savings' in rec:
                                st.markdown(f"**Potential Savings:** ${rec['savings']:.2f}/month")
                            
                            st.markdown(f"**Why We Recommend This:**")
                            st.markdown(rec['explanation'])
                            
                            st.markdown(f"**Side Effects:** {rec['side_effects']}")
                            st.markdown(f"**Source:** {rec['source']}")
                        
                        with col2:
                            st.markdown("### Cost Comparison")
                            # Create a simple bar chart for cost comparison
                            data = {
                                'Medication': [med_info['name'], rec['name']],
                                'Monthly Cost': [med_info['avg_cost'], rec['avg_cost']]
                            }
                            chart_data = pd.DataFrame(data)
                            st.bar_chart(chart_data.set_index('Medication'))
                        
                        st.markdown("---")
            else:
                st.info("No generic alternatives found for this medication.")
        
        with tabs[2]:
            # Filter to show only affordability options
            affordability = [rec for rec in st.session_state.recommendations if rec['recommendation_type'] == "Cheapest with similar effect"]
            
            if affordability:
                for i, rec in enumerate(affordability):
                    with st.container():
                        st.markdown(f"### {i+1}. {rec['name']}")
                        
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Average Monthly Cost:** ${rec['avg_cost']:.2f}")
                            if 'savings' in rec:
                                st.markdown(f"**Potential Savings:** ${rec['savings']:.2f}/month")
                            
                            st.markdown(f"**Why We Recommend This:**")
                            st.markdown(rec['explanation'])
                            
                            if 'availability' in rec:
                                st.markdown(f"**Availability:** {rec['availability']}")
                            
                            st.markdown(f"**Side Effects:** {rec['side_effects']}")
                            st.markdown(f"**Source:** {rec['source']}")
                        
                        with col2:
                            st.markdown("### Cost Comparison")
                            # Create a simple bar chart for cost comparison
                            data = {
                                'Medication': [med_info['name'], rec['name']],
                                'Monthly Cost': [med_info['avg_cost'], rec['avg_cost']]
                            }
                            chart_data = pd.DataFrame(data)
                            st.bar_chart(chart_data.set_index('Medication'))
                        
                        st.markdown("---")
            else:
                st.info("No affordability alternatives found for this medication.")
        
        with tabs[3]:
            # Filter to show only alternative treatments
            alternatives = [rec for rec in st.session_state.recommendations if rec['recommendation_type'] == "Alternative treatment"]
            
            if alternatives:
                for i, rec in enumerate(alternatives):
                    with st.container():
                        st.markdown(f"### {i+1}. {rec['name']}")
                        
                        st.markdown(f"**Type:** {rec.get('type', 'Supplement/Lifestyle')}")
                        st.markdown(f"**Average Monthly Cost:** ${rec['avg_cost']:.2f}")
                        
                        st.markdown(f"**Evidence-Based Benefits:**")
                        st.markdown(rec['explanation'])
                        
                        st.markdown(f"**Important Note:** {rec.get('warning', 'Always consult with your healthcare provider before making any changes to your treatment plan.')}")
                        st.markdown(f"**Source:** {rec['source']}")
                        
                        st.markdown("---")
            else:
                st.info("No alternative treatments found for this medication.")
        
        # Action buttons
        st.markdown("## Next Steps")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Download PDF Report"):
                # Generate and download PDF
                pdf_file = generate_pdf(
                    st.session_state.original_medication,
                    med_info,
                    st.session_state.recommendations,
                    st.session_state.insurance,
                    st.session_state.budget
                )
                
                st.download_button(
                    label="Click to download PDF",
                    data=pdf_file,
                    file_name=f"MediMatch_Report_{st.session_state.original_medication}.pdf",
                    mime="application/pdf"
                )
        
        with col2:
            if st.button("Start a New Search"):
                reset_app()
        
        # Educational section
        st.markdown("## Educational Information")
        
        with st.expander("Understanding Brand vs. Generic Medications"):
            st.markdown("""
            ### Brand vs. Generic Medications
            
            **Brand-name medications** are developed and marketed by pharmaceutical companies that initially discover and patent them. 
            These companies have exclusive rights to sell the medication for a certain period, typically 20 years from the patent filing date.
            
            **Generic medications** contain the same active ingredients as brand-name drugs and work the same way in the body. 
            They become available after the patent for the brand-name drug expires. The FDA requires generic drugs to be:
            
            - Bioequivalent to the brand-name version (same active ingredient, strength, dosage form, and route of administration)
            - Manufactured under the same strict standards
            - Equally safe and effective
            
            **Key differences:**
            
            | Brand-Name | Generic |
            |------------|---------|
            | More expensive | Typically 80-85% less expensive |
            | Protected by patent | Available after patent expiration |
            | Well-known company | Various manufacturers |
            | Marketing costs included in price | Lower marketing costs |
            
            **Why generics are cheaper:**
            - No need to repeat costly clinical trials
            - Multiple companies can produce them, creating competition
            - Lower marketing expenses
            - No need to recover expensive research and development costs
            
            Source: FDA, American Medical Association
            """)
        
        with st.expander("How to Talk to Your Doctor About Medication Costs"):
            st.markdown("""
            ### How to Discuss Medication Costs with Your Doctor
            
            Many patients feel uncomfortable discussing medication costs with their healthcare providers, but it's an important conversation to have. Here are some tips:
            
            1. **Be honest about your financial concerns.** Doctors often don't know the cost of medications with your specific insurance.
            
            2. **Ask specifically about generic alternatives.** Use phrasing like: "Is there a generic version of this medication that would work just as well for my condition?"
            
            3. **Bring this report with you.** Having information about specific alternatives can make the conversation more productive.
            
            4. **Ask about medication assistance programs.** Many pharmaceutical companies offer assistance for those who qualify.
            
            5. **Discuss the possibility of a higher dose that can be split** (only with doctor approval and if the medication is safe to split).
            
            6. **Inquire about therapeutic alternatives** in the same drug class that might be less expensive.
            
            7. **Be clear about adherence concerns.** If cost might prevent you from taking your medication as prescribed, your doctor needs to know.
            
            Source: Mayo Clinic, American Academy of Family Physicians
            """)
        
        # Doctor note template
        with st.expander("Doctor Discussion Note Template"):
            note_template = f"""
            Dear Healthcare Provider,
            
            I recently received a prescription for {st.session_state.original_medication}. After reviewing my insurance coverage and budget, I'm concerned about the cost of this medication.
            
            I've researched some potential alternatives and would like to discuss if any of these options might be appropriate for my condition:
            
            {', '.join([rec['name'] for rec in st.session_state.recommendations[:3]])}
            
            I understand that my health is the priority, and I'm not requesting any changes that would compromise my treatment. I'm simply hoping to explore options that might be more financially sustainable for me long-term.
            
            Thank you for considering these alternatives.
            
            Sincerely,
            [Your Name]
            """
            
            st.text_area("Copy this note to discuss with your doctor:", note_template, height=300)
            if st.button("Copy to Clipboard"):
                st.info("Note copied to clipboard! You can paste this into an email or print it for your next appointment.")

elif page == "Educational Resources":
    # Display educational content
    display_educational_content()
    
    # Display resource links
    display_resources()

else:  # About page
    st.header("About MediMatch AI")
    
    st.markdown("""
    ### Our Mission
    
    MediMatch AI aims to empower patients to make informed decisions about their medications, with a focus on affordability and personalized care. We believe that everyone deserves access to the medications they need at prices they can afford.
    
    ### How We Work
    
    1. **Data Sources**: We utilize publicly available information from the FDA, NIH, and other reputable healthcare sources.
    
    2. **Recommendations**: Our algorithm analyzes medication alternatives based on drug class, cost, and your personal factors.
    
    3. **Privacy**: We do not store your personal health information or medication searches.
    
    ### Important Disclaimer
    
    MediMatch AI is designed to provide information and suggestions only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition or medication.
    
    Never disregard professional medical advice or delay in seeking it because of something you have read on this website. Always consult with your healthcare provider before making any changes to your medication regimen.
    
    ### Contact Us
    
    For questions, feedback, or support, please email us at support@medimatchai.com
    """)

# Footer
st.markdown("---")
st.markdown("© 2023 MediMatch AI | Disclaimer: This tool provides information only and is not a substitute for professional medical advice.")
