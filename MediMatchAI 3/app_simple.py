import streamlit as st
import pandas as pd
from simple_db import (
    get_medication_info, 
    find_alternatives, 
    get_supplement_suggestions, 
    get_insurance_description,
    get_medication_risks,
    get_do_not_combine
)
from simple_assistant import SimpleAssistant

# Initialize the simple assistant
assistant = SimpleAssistant()

# Set page configuration
st.set_page_config(
    page_title="MediMatch AI - Medication Alternatives",
    page_icon="💊",
    layout="wide",
)

# Initialize session state
if 'medication_info' not in st.session_state:
    st.session_state.medication_info = None
if 'alternative_info' not in st.session_state:
    st.session_state.alternative_info = None
if 'supplements' not in st.session_state:
    st.session_state.supplements = []
if 'user_question' not in st.session_state:
    st.session_state.user_question = ""
if 'assistant_response' not in st.session_state:
    st.session_state.assistant_response = ""
if 'selected_alternative' not in st.session_state:
    st.session_state.selected_alternative = 0
if 'original_medication' not in st.session_state:
    st.session_state.original_medication = ""

# Function to reset the application
def reset_app():
    st.session_state.medication_info = None
    st.session_state.alternative_info = None
    st.session_state.supplements = []
    st.session_state.user_question = ""
    st.session_state.assistant_response = ""
    st.session_state.selected_alternative = 0
    st.session_state.original_medication = ""
    st.rerun()

# Function to set question and get response
def ask_question(question):
    st.session_state.user_question = question

    # Get the selected alternative for context
    alternative = None
    if st.session_state.alternative_info and len(st.session_state.alternative_info) > st.session_state.selected_alternative:
        alternative = st.session_state.alternative_info[st.session_state.selected_alternative]

    st.session_state.assistant_response = assistant.answer_question(
        question, 
        st.session_state.medication_info, 
        alternative
    )
    st.rerun()

# Main app header with styled title and subheader
st.markdown("<h1 style='text-align: center; color: #2C8ECF;'>💊 MediMatch AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Find Affordable Medication Alternatives</h3>", unsafe_allow_html=True)

# Main content with better styling
st.markdown("""
<div style='background-color: rgba(44, 142, 207, 0.1); padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
<p style='font-size: 16px; line-height: 1.5;'>
This tool helps you find affordable and safer medication alternatives based on your prescription.
Enter your prescription details below to get personalized recommendations.
</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation and assistant with improved styling
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>💬 Medication Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    if st.session_state.medication_info is not None:
        st.markdown("### Ask me about your medications")

        user_question = st.text_input("Type your question here:", key="user_question_input")

        # Add buttons for common questions
        st.markdown("### Common Questions")

        # Create 3 columns for the question buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("What's the difference?"):
                ask_question("What's the difference between this and the alternative?")

            if st.button("Will this work without insurance?"):
                ask_question("Will this work without insurance?")

            if st.button("Are supplements helpful?"):
                ask_question("Are supplements helpful?")

        with col2:
            if st.button("How much can I save?"):
                ask_question("How much can I save with the cheaper option?")

            if st.button("What does this treat?"):
                ask_question("What does this medication treat?")

            if st.button("Why no alternative?"):
                ask_question("Why was no alternative found?")

        with col3:
            if st.button("Can I drink alcohol?"):
                ask_question("Can I drink alcohol with this medication?")

            if st.button("Mix with Advil?"):
                ask_question("Can I take this with Advil?")

            if st.button("Safe with supplements?"):
                ask_question("Is it safe to take with supplements?")

        if st.button("Ask", key="ask_button"):
            if user_question:
                ask_question(user_question)

        if st.session_state.user_question and st.session_state.assistant_response:
            st.markdown("<div style='background-color: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 5px; margin-top: 20px;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 18px; margin-bottom: 5px;'>Your Question</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: white;'><strong>Q:</strong> {st.session_state.user_question}</p>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 18px; margin-bottom: 5px; margin-top: 15px;'>Response</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: white;'><strong>A:</strong> {st.session_state.assistant_response}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("Enter your medication details to get started with personalized assistance.")

    st.markdown("---")

    if st.button("Start Over"):
        reset_app()

# Check if recommendations already exist
if st.session_state.medication_info is None:
    # Input form
    st.header("Enter Your Prescription Details")

    col1, col2 = st.columns(2)

    with col1:
        medication = st.text_input("Prescribed Medication Name*", 
                                  help="Enter the exact name of the medication prescribed to you")
        budget = st.number_input("Monthly Budget (USD)", 
                                min_value=0.0, value=50.0,
                                help="What's your maximum monthly budget for this medication?")

    with col2:
        insurance = st.selectbox(
            "Insurance Coverage",
            ["None / Self-pay", "Limited", "Some", "Most"],
            help="Select your level of insurance coverage"
        )
        allergies = st.text_area("Allergies or Restrictions", 
                               help="List any allergies or medical conditions")

    include_supplements = st.checkbox("I'm interested in supplements or lifestyle alternatives", 
                                     help="Check this to see evidence-based complementary options")

    search_button = st.button("Find Alternatives", type="primary")

    if search_button:
        if not medication:
            st.error("Please enter a medication name to continue.")
        else:
            # Look up the medication in our database
            med_info = get_medication_info(medication)

            if med_info is None:
                st.error(f"We couldn't find '{medication}' in our database. Please check the spelling or try a different medication.")
            else:
                # Save medication info and user selections to session state
                st.session_state.medication_info = med_info
                st.session_state.insurance = insurance
                st.session_state.budget = budget
                st.session_state.allergies = allergies
                st.session_state.original_medication = medication #Added this line

                # Find alternatives based on criteria
                alternatives = find_alternatives(
                    med_info,
                    budget,
                    insurance,
                    allergies
                )

                st.session_state.alternative_info = alternatives

                # Get supplement suggestions if requested
                if include_supplements:
                    st.session_state.supplements = get_supplement_suggestions(med_info)

                st.rerun()
else:
    # Display medication information and alternatives
    st.header(f"Medication Information: {st.session_state.medication_info['Medication Name']}")

    # Create a visually separated card for the prescribed medication
    st.markdown("""<div style="border: 1px solid rgba(44, 142, 207, 0.3); 
                               border-radius: 10px; 
                               padding: 20px; 
                               margin-bottom: 25px; 
                               background-color: rgba(44, 142, 207, 0.05);">""", 
               unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<h3 style='font-size: 20px;'>Your Prescribed Medication</h3>", unsafe_allow_html=True)
        med_info = st.session_state.medication_info

        st.markdown(f"**Name:** {med_info['Medication Name']} ({med_info['Generic Name']})")
        st.markdown(f"**Class:** {med_info['Type/Class']}")
        st.markdown(f"**Average Monthly Cost:** ${med_info['Avg Cost (USD)']}")

        # Display detailed insurance coverage information with savings estimates
        insurance_level = med_info['Insurance Coverage']

        if insurance_level == "Most":
            savings_min = max(5, int(med_info['Avg Cost (USD)'] * 0.4))
            savings_max = max(10, int(med_info['Avg Cost (USD)'] * 0.7))
            st.markdown(f"**Insurance Coverage:** Most plans cover this medication. You may save **${savings_min}–${savings_max}** per month with insurance.")
        elif insurance_level == "Some":
            savings_min = max(3, int(med_info['Avg Cost (USD)'] * 0.2))
            savings_max = max(6, int(med_info['Avg Cost (USD)'] * 0.4))
            st.markdown(f"**Insurance Coverage:** Some plans offer partial coverage. Estimated savings: **${savings_min}–${savings_max}** monthly.")
        elif insurance_level == "Limited":
            st.markdown("**Insurance Coverage:** Only a few plans cover this drug. Savings may be small or none.")
        else:
            st.markdown("**Insurance Coverage:** This medication is not covered. Expect to pay the full price out of pocket.")

        # Add spacing before warnings
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

        # Get the medication risks
        med_risks = get_medication_risks(med_info['Medication Name'])
        if med_risks:
            st.warning(f"⚠️ **Potential Risks:** {med_risks}")

        # Get do not combine information first (to avoid variable use before assignment)
        contraindications = get_do_not_combine(med_info['Medication Name'])

        # Add spacing between warning boxes
        if med_risks and contraindications:
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        if contraindications:
            st.error("🚫 **Do not take with:**")
            for item in contraindications:
                st.markdown(f"- {item}")

        # Add spacing between warning boxes
        if (med_risks and med_info['Restrictions'] != 'None') or (contraindications and med_info['Restrictions'] != 'None'):
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

        # Display restrictions if any
        if med_info['Restrictions'] != 'None':
            st.info(f"ℹ️ **Medical Caution:** May not be suitable for people with {med_info['Restrictions']}")

    with col2:
        st.markdown("<h3 style='font-size: 18px;'>Your Information</h3>", unsafe_allow_html=True)

        # Create a styled box for user information
        st.markdown("""<div style="background-color: rgba(255, 255, 255, 0.05); 
                                  padding: 15px; 
                                  border-radius: 5px;">""", 
                   unsafe_allow_html=True)

        # Use the user's actual insurance selection
        if 'insurance' in st.session_state:
            st.markdown(f"**Insurance:** {st.session_state.get('insurance', 'None / Self-pay')}")
        else:
            st.markdown(f"**Insurance:** None / Self-pay")

        if 'budget' in st.session_state:
            st.markdown(f"**Monthly Budget:** ${st.session_state.get('budget', 'Not specified')}")

        if 'allergies' in st.session_state and st.session_state.allergies:
            st.markdown(f"**Allergies/Restrictions:** {st.session_state.get('allergies', 'None specified')}")

        st.markdown("</div>", unsafe_allow_html=True)

    # Close the container div
    st.markdown("</div>", unsafe_allow_html=True)

    # Display alternatives if any
    st.header("Recommended Alternatives")

    if st.session_state.alternative_info:
        for alt in st.session_state.alternative_info:
            # Create a visually separated card with a light border
            st.markdown("""<div style="border: 1px solid rgba(44, 142, 207, 0.2); 
                                       border-radius: 10px; 
                                       padding: 20px; 
                                       margin-bottom: 25px; 
                                       background-color: rgba(255, 255, 255, 0.05);">""", 
                       unsafe_allow_html=True)

            st.subheader(f"{alt['name']} ({alt['generic_name']})")

            col1, col2 = st.columns([3, 1])

            with col1:
                # Get an explanation from the assistant
                explanation = assistant.explain_recommendation(
                    st.session_state.medication_info, 
                    alt
                )
                st.write(explanation)



                # Add spacing before warnings
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

                # Show potential risks in a yellow warning box
                if 'potential_risks' in alt and alt['potential_risks']:
                    st.warning(f"⚠️ **Potential Risks:** {alt['potential_risks']}")

                # Add spacing between warning boxes
                if 'potential_risks' in alt and alt['potential_risks'] and 'do_not_combine' in alt and alt['do_not_combine']:
                    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

                # Show "Do Not Combine With" information in a separate box
                if 'do_not_combine' in alt and alt['do_not_combine']:
                    st.error("🚫 **Do not take with:**")
                    for item in alt['do_not_combine']:
                        st.markdown(f"- {item}")

                # Add spacing between warning boxes
                if ('do_not_combine' in alt and alt['do_not_combine'] and alt.get('restrictions') and alt['restrictions'] != 'None') or \
                   ('potential_risks' in alt and alt['potential_risks'] and alt.get('restrictions') and alt['restrictions'] != 'None'):
                    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

                # Show restrictions if available
                if alt.get('restrictions') and alt['restrictions'] != 'None':
                    st.info(f"ℹ️ **Medical Caution:** May not be suitable for people with {alt['restrictions']}")

            with col2:
                st.markdown("<h3 style='font-size: 20px; text-align: right;'>Monthly Cost Comparison</h3>", unsafe_allow_html=True)

                # Create an improved bar chart for cost comparison
                original_cost = med_info['Avg Cost (USD)']
                alt_cost = alt['avg_cost']

                # Create data frame with better labels
                data = {
                    'Medication': [med_info['Medication Name'], alt['name']],
                    'Cost (USD)': [original_cost, alt_cost]
                }
                chart_data = pd.DataFrame(data)

                # Create custom bar chart with better formatting
                chart = st.bar_chart(chart_data.set_index('Medication'), use_container_width=True)

                # Display cost values directly and calculate savings
                st.markdown(f"""
                    <div style='text-align: center; font-weight: bold; font-size: 16px;
                                padding: 5px; background-color: rgba(44, 142, 207, 0.1);
                                border-radius: 5px;'>
                        It costs <strong>${alt_cost:.2f}</strong> per month,
                        which is <strong>${abs(alt_cost - original_cost):.2f} less</strong> than
                        <strong>{st.session_state.original_medication}</strong>
                        (a savings of about <strong>{((original_cost - alt_cost)/original_cost * 100):.0f}%</strong>).
                    </div>
                """, unsafe_allow_html=True)

            # Close the container div
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No suitable alternatives found based on your criteria.")

    # Display supplement suggestions if any
    if st.session_state.supplements:
        st.header("Supplement & Lifestyle Suggestions")

        # Create a container for all supplements
        st.markdown("""<div style="border: 1px solid rgba(44, 142, 207, 0.2); 
                                   border-radius: 10px; 
                                   padding: 20px; 
                                   margin-bottom: 25px; 
                                   background-color: rgba(44, 142, 207, 0.03);">""", 
                   unsafe_allow_html=True)

        for i, supplement in enumerate(st.session_state.supplements):
            # Create a container for each supplement to improve spacing
            with st.container():
                st.markdown(f"<h4 style='color: #2C8ECF; margin-bottom: 10px;'>{supplement}</h4>", unsafe_allow_html=True)

                # Look up information about this supplement
                supp_description = assistant.responses["supplement"].get(
                    supplement.lower().split()[0],  # Get first word of supplement
                    f"This may provide some benefit for your condition. Always consult with a healthcare professional before starting any supplement."
                )

                st.markdown(f"{supp_description}")
                st.markdown("<p style='font-style: italic; color: rgba(255, 255, 255, 0.7);'>Note: Supplements are not FDA-approved to treat medical conditions.</p>", unsafe_allow_html=True)

                # Add a separator if it's not the last item
                if i < len(st.session_state.supplements) - 1:
                    st.markdown("<hr style='margin: 15px 0; opacity: 0.2;'>", unsafe_allow_html=True)

        # Close the container div
        st.markdown("</div>", unsafe_allow_html=True)

    # Action buttons
    st.markdown("---")
    if st.button("Search for Another Medication"):
        reset_app()

# Footer
st.markdown("---")
st.markdown("**Disclaimer:** This tool is for informational purposes only and is not a substitute for professional medical advice. Always consult with your healthcare provider before making any changes to your medication regimen.")