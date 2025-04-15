import streamlit as st

def display_educational_content():
    """Display educational content about medications and healthcare."""
    st.header("Educational Resources")
    
    # Create tabs for different educational topics
    tabs = st.tabs([
        "Understanding Medications", 
        "Generic vs. Brand", 
        "Saving on Prescriptions", 
        "Talking to Your Doctor"
    ])
    
    with tabs[0]:
        st.subheader("Understanding Your Medications")
        
        st.markdown("""
        ### What Are Drug Classes?
        
        Medications are grouped into "classes" based on how they work in the body or what conditions they treat.
        For example, statins lower cholesterol, while SSRIs are a type of antidepressant.
        
        ### Reading Medication Labels
        
        Medication labels contain important information, including:
        
        - **Active Ingredient**: The therapeutic component of the drug
        - **Inactive Ingredients**: Fillers, binders, colors, or preservatives
        - **Dosage Information**: How much and how often to take the medication
        - **Warnings**: Potential side effects and when to contact a healthcare provider
        - **Expiration Date**: When the medication is no longer guaranteed to be safe and effective
        
        ### Important Questions to Ask About New Medications
        
        1. What is this medication supposed to do?
        2. How and when should I take it?
        3. What side effects might I experience?
        4. Should I take it with food or on an empty stomach?
        5. Will it interact with other medications I'm taking?
        6. How will I know if it's working?
        7. What should I do if I miss a dose?
        
        Source: FDA, American Pharmacists Association
        """)
    
    with tabs[1]:
        st.subheader("Generic vs. Brand-Name Medications")
        
        st.markdown("""
        ### What Are Generic Medications?
        
        Generic medications are copies of brand-name drugs that have the same:
        
        - Active ingredient
        - Strength
        - Dosage form (pill, liquid, etc.)
        - Administration route
        - Safety profile
        - Intended use
        
        ### Key Facts About Generics
        
        - The FDA requires generics to be "bioequivalent" to brand-name drugs, meaning they work the same way
        - Generics typically cost 80-85% less than brand-name medications
        - About 90% of prescriptions filled in the US are for generic drugs
        - Differences in inactive ingredients (colors, fillers) may exist but don't affect how the drug works
        
        ### Why Are Generics Cheaper?
        
        1. No need to repeat expensive clinical trials
        2. Multiple companies can produce them, creating competition
        3. Lower marketing expenses
        4. No need to recover research and development costs
        
        ### When Brand Names Might Be Preferred
        
        - For "narrow therapeutic index" drugs where small differences in blood levels matter (e.g., certain thyroid medications)
        - If you've had a negative reaction to a specific generic's inactive ingredients
        - Some extended-release formulations may have different release mechanisms
        
        Source: FDA, American Medical Association
        """)
        
        # Add a comparison table
        st.markdown("### Brand vs. Generic Comparison")
        
        data = {
            "Feature": ["Active Ingredient", "FDA Approval", "Appearance", "Cost", "Safety & Effectiveness"],
            "Brand-Name": ["Original formula", "Full clinical trials", "Consistent", "Higher", "Proven in clinical trials"],
            "Generic": ["Identical", "Bioequivalence testing", "May differ", "Lower (80-85% less)", "Same as brand-name"]
        }
        
        st.dataframe(data)
    
    with tabs[2]:
        st.subheader("Strategies for Saving on Prescriptions")
        
        st.markdown("""
        ### Insurance Optimization
        
        - **Formulary Tiers**: Understand your insurance's preferred drug list and tiers
        - **Prior Authorization**: Learn when and how to request it for non-preferred medications
        - **Mail-Order Options**: Many insurance plans offer discounts for 90-day supplies through mail order
        
        ### Patient Assistance Programs
        
        - **Manufacturer Programs**: Many pharmaceutical companies offer programs to help eligible patients get medications at reduced or no cost
        - **Non-Profit Organizations**: Organizations specific to certain conditions often provide medication assistance
        
        ### Discount Programs and Coupons
        
        - **Discount Cards**: Programs like GoodRx, SingleCare, or RxSaver can offer significant savings
        - **Manufacturer Coupons**: Search for "[Medication Name] savings card" online
        - **Pharmacy Memberships**: Many pharmacies offer membership programs with prescription discounts
        
        ### Medication Alternatives
        
        - **Therapeutic Substitution**: Different medications in the same class that might cost less
        - **Over-the-Counter Options**: For some conditions, OTC medicines may be effective and less expensive
        - **Pill Splitting**: With doctor approval, sometimes a higher dose can be split to save money
        
        Source: Consumer Reports, Medicare.gov, GoodRx
        """)
    
    with tabs[3]:
        st.subheader("Talking to Your Doctor About Medication Costs")
        
        st.markdown("""
        ### Starting the Conversation
        
        Many patients feel uncomfortable discussing medication costs, but doctors want to help you manage your health affordably. 
        Here are some conversation starters:
        
        - "I'm concerned about the cost of this medication. Are there less expensive options that would work for me?"
        - "My insurance doesn't cover this medication well. Could you recommend an alternative that's on my formulary?"
        - "I'm having trouble affording my medications. Can we discuss some options?"
        
        ### Questions to Ask Your Doctor
        
        1. "Is a generic version available?"
        2. "Is there a similar medication that costs less?"
        3. "Are there any patient assistance programs for this medication?"
        4. "Can I safely split a higher-dose pill to save money?"
        5. "Is this medication absolutely necessary, or are there other approaches we could try first?"
        6. "Can I get a 90-day supply to reduce costs?"
        
        ### Preparing for Your Appointment
        
        - Bring a list of your current medications
        - Research your insurance formulary beforehand
        - Check discount prices on GoodRx or similar sites
        - Bring information about your financial concerns
        - Consider asking for samples to try a medication before paying for a full prescription
        
        Source: American Academy of Family Physicians, Mayo Clinic
        """)

def display_resources():
    """Display links to medication assistance resources."""
    st.header("Helpful Resources")
    
    st.markdown("""
    ### Prescription Savings Programs
    
    - [GoodRx](https://www.goodrx.com) - Compare prices and find coupons
    - [NeedyMeds](https://www.needymeds.org) - Information on patient assistance programs
    - [RxHope](https://www.rxhope.com) - Patient assistance program applications
    - [Medicine Assistance Tool](https://medicineassistancetool.org) - Help finding assistance programs
    - [RxAssist](https://www.rxassist.org) - Directory of patient assistance programs
    
    ### Government Resources
    
    - [Medicare.gov Drug Coverage](https://www.medicare.gov/drug-coverage-part-d) - Information about Medicare prescription coverage
    - [FDA Generic Drugs](https://www.fda.gov/drugs/generic-drugs) - Official information about generic medications
    - [HealthCare.gov](https://www.healthcare.gov) - Information about health insurance options
    
    ### Educational Resources
    
    - [MedlinePlus](https://medlineplus.gov) - Reliable information about medications and health conditions
    - [FDA Medication Guides](https://www.fda.gov/drugs/drug-safety-and-availability/medication-guides) - Detailed information about specific medications
    - [Consumer Reports Best Buy Drugs](https://www.consumerreports.org/health/best-buy-drugs) - Independent evaluations of medication effectiveness and value
    
    ### Assistance for Specific Populations
    
    - [Partnership for Prescription Assistance](https://medicineassistancetool.org) - Help for patients with limited resources
    - [Extra Help with Medicare Prescription Drug Costs](https://www.ssa.gov/benefits/medicare/prescriptionhelp.html) - Program for Medicare recipients
    - [State Pharmaceutical Assistance Programs](https://www.medicare.gov/pharmaceutical-assistance-program) - State-specific programs
    """)
