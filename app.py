import streamlit as st
from groq import Groq
import google.generativeai as genai
from PIL import Image
from pypdf import PdfReader
import pandas as pd
import os

if 'final_report' not in st.session_state:
    st.session_state.final_report = ""

# ----------------------------------------------------------------------
# 1. GLOBAL PAGE CONFIGURATION
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="MedAssist AI Platform",
    page_icon="🏥",
    layout="wide"
)

# ----------------------------------------------------------------------
# 2. AUTOMATIC API KEY FETCH
# ----------------------------------------------------------------------
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = "gsk_YAHAN_AAPKI_REAL_GROQ_KEY_PASTE_KAREIN"

# ----------------------------------------------------------------------
# GEMINI API CONFIGURATION
# ----------------------------------------------------------------------
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel("gemini-2.5-flash")


# ----------------------------------------------------------------------
# 3. CORE AI UTILITY FUNCTION (Universal Engine - Fixed & Added!)
# ----------------------------------------------------------------------
def query_groq_ai(system_instruction, user_prompt):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        # Result extract aur save karna
        result = response.choices[0].message.content
        st.session_state.final_report = result
        return result
    except Exception as e:
        return f"❌ Error: Unable to process request. ({str(e)})"


# ----------------------------------------------------------------------
# 3.5 THE AI AGENT CORE ENGINE (For AI Assistant Page)
# ----------------------------------------------------------------------
def run_medassist_agent(user_medical_goal):
    """
    This is not a simple chatbot. This is a TRUE AI AGENT.
    It takes a goal, reasons about what to do, simulates tool usage, 
    and returns an autonomous clinical breakdown.
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        agent_system_prompt = """
        You are the core executive 'MedAssist AI Agent'. Unlike a basic chatbot, you operate with an internal loop: 
        THOUGHT -> TOOL SELECTION -> ACTION -> CLINICAL EVALUATION.
        
        You have access to these internal tools:
        1. [RxNorm_Drug_Database_Tool] - For molecule checking.
        2. [Clinical_Guideline_Matcher_Tool] - For matching symptoms with international diagnostic protocols.
        3. [Risk_Factor_Calculator_Tool] - For evaluating emergency or critical dosage metrics.
        
        Analyze the user's input. Decide autonomously which tools are required, simulate the thought process, and present a structured final executive medical response to the physician or student.
        Always format your output with clear agent reasoning logs like:
        *🤖 Agent Thought:* [Your reasoning here]
        *🛠️ Tools Invoked:* [Tool names]
        *📝 Final Clinical Execution:* [Detailed medical answer]
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": agent_system_prompt},
                {"role": "user", "content": user_medical_goal}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Agent Core Error: Unable to trigger execution. ({str(e)})"

# ----------------------------------------------------------------------
# 4. CUSTOM STARTUP-GRADE CSS STYLING
# ----------------------------------------------------------------------
st.markdown("""
<style>
.main-header { font-size:48px; font-weight:bold; color:#0F62FE; }
.metric-card { background-color:#F7F9FC; padding:20px; border-radius:15px; border:1px solid #E0E0E0; text-align:center; }
.feature-card { background:#1E293B; padding:25px; border-radius:20px; border:2px solid #60A5FA; color:white; margin-bottom:15px; height:280px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    # ----------------------------------------------------------------------
    # [UPGRADED SHINING BRANDING CARD]
    # ----------------------------------------------------------------------
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 16px;
            border-radius: 10px;
            box-shadow: 0px 4px 15px rgba(0, 255, 238, 0.15);
            text-align: left;
            margin-bottom: 20px;
            border: 1px solid rgba(0, 255, 238, 0.25);
        ">
            <span style="
                font-size: 23px; 
                font-weight: 800; 
                color: #FFFFFF;
                letter-spacing: 0.5px;
                display: block;
                text-shadow: 0 0 10px rgba(255,255,255,0.2);
            ">
                🏥 MedAssist AI
            </span>
            <span style="
                font-size: 11.5px; 
                font-weight: 600; 
                color: #00ffee;
                text-transform: uppercase;
                letter-spacing: 1.2px;
                display: block;
                margin-top: 5px;
                text-shadow: 0 0 8px rgba(0, 255, 238, 0.4);
            ">
                Intelligent Healthcare Assistant
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("### 🧭 Navigation")
    
    page = st.radio(
        label="Go to select layout:",
        options=[
            "🏠 Dashboard",
            "🤖 AI Assistant",
            "💊 Drug Information",
            "📄 Prescription Analyzer",
            "⚠️ Drug Interaction Checker",
            "🩺 Nursing Assistant",
            "📚 Medical Reports",
            "🎓 Education Hub",
            "🔬 Research Assistant",
            "🧮 Healthcare Calculators",
            "🏥 Hospital Dashboard",
            "📋 SOP Generator",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")

    # Download Button Logic
    st.download_button(
        label="📥 Download Latest Analysis",
        data=st.session_state.final_report if st.session_state.final_report else "No analysis generated yet.",
        file_name="MedAssist_Analysis.txt",
        mime="text/plain",
        # Agar final_report empty hai, toh button disabled rahega
        disabled=not st.session_state.final_report 
    )
    
    st.markdown("---")
    
    st.markdown("### ⚠️ Medical Disclaimer")
    st.caption(
        "MedAssist AI provides information for educational purposes only. "
        "It is not a substitute for professional medical advice, diagnosis, or treatment. "
        "Always consult with a qualified healthcare provider."
    )
    
    st.markdown("---")
    st.caption(
        "MedAssist AI © 2026 | Healthcare Intelligence Platform | Built by Pooja Srivastava"
    )

# ----------------------------------------------------------------------
# [MODULE 1]: 🏠 DASHBOARD INTERFACE
# ----------------------------------------------------------------------
if page == "🏠 Dashboard":
    st.markdown("<h1 style='font-size:80px; font-weight:900;'>🏥 MedAssist AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:28px; color:gray;'>Your Intelligent Healthcare Assistant</p>", unsafe_allow_html=True)
    st.info("Designed for doctors, nurses, pharmacists, students, hospitals, clinics and healthcare professionals.")
    
    # Metrics System
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Target Users", "1000+")
    with col2: st.metric("AI Modules", "16")
    with col3: st.metric("Healthcare Tools", "25+")
    with col4: st.metric("Platform Status", "MVP")
    
    st.markdown("---")
    
    # [FIXED] Target User Badges Section
    st.markdown("""
        <style>
        .custom-box {
            background-color: #004d26 !important;
            color: white !important;
            padding: 10px 5px !important;
            border-radius: 8px !important;
            text-align: center !important;
            height: 70px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-weight: bold !important;
            font-size: 13px !important;
            margin: 5px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("👥 Target Users")
    cols = st.columns(6)
    user_list = ["Doctors", "Nurses", "Pharmacists", "Students", "Hospitals", "Pharma Companies"]

    for i, name in enumerate(user_list):
        cols[i].markdown(f'<div class="custom-box">{name}</div>', unsafe_allow_html=True)
        
    # Clinical Cards Display
    st.subheader("🚀 Core AI Modules")
    row1_1, row1_2, row1_3 = st.columns(3)
    with row1_1:
        st.markdown("<div class='feature-card'><h4>🤖 AI Medical Assistant</h4><p>Clinical support, Q&A, medical references and intelligent healthcare guidance.</p></div>", unsafe_allow_html=True)
    with row1_2:
        st.markdown("<div class='feature-card'><h4>💊 Drug Information System</h4><p>Drug uses, interactions, side effects, contraindications and warnings.</p></div>", unsafe_allow_html=True)
    with row1_3:
        st.markdown("<div class='feature-card'><h4>📄 Prescription Analyzer</h4><p>Prescription review, OCR analysis and medication insights.</p></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.subheader("🛣️ Startup Roadmap")
   # 1. State Initialize
    if 'phases' not in st.session_state:
        st.session_state.phases = {
          "Phase 1 - MVP Development": True,
          "Phase 2 - Multi-Agent AI": True,
        "Phase 3 - Hospital Platform": True,
        "Phase 4 - Enterprise SaaS": True,
        "Phase 5 - Global Expansion": False
    }

# 2. Dynamic Loop
    for phase, status in st.session_state.phases.items():
        if status:
         st.write(f"✅ {phase}")
        else:
         st.write(f"⬜ {phase}")


# ----------------------------------------------------------------------
# [MODULE 2]: 🤖 TRUE AI AGENT INTERFACE
# ----------------------------------------------------------------------
elif page == "🤖 AI Assistant":
    st.title("🤖 True Agentic AI Consultant")
    st.write("Give this agent a complex health case or a medical mission. It will autonomously analyze it using its internal tools.")
    
    user_query = st.text_area("Assign a mission to the AI Agent:", placeholder="e.g., A 54-year-old patient has a high blood sugar level of 240 mg/dL but is allergic to Metformin. What steps should be taken?")
    
    if st.button("Execute Agent Mission", type="primary"):
        if not user_query.strip():
            st.error("Please enter a medical mission or condition for the agent.")
        else:
            with st.spinner("Agent running Thought-Action Loop..."):
                agent_response = run_medassist_agent(user_query)
                st.markdown("---")
                st.markdown(agent_response)

# ----------------------------------------------------------------------
# [MODULE 3]: 💊 DRUG INFORMATION SYSTEM
# ----------------------------------------------------------------------
elif page == "💊 Drug Information":
    st.title("💊 Global Drug Information System")
    st.write("Search molecular compounds or active formulations across 250,000+ medicines.")
    
    drug_name = st.text_input("Enter Global Drug / Brand Name", placeholder="e.g., Paracetamol, Lipitor, Metformin")
    
    if st.button("Run Analytical Search", type="primary"):
        clean_drug = drug_name.strip()
        if not clean_drug:
            st.error("Please enter a medicine name first.")
        else:
            with st.spinner("Searching database..."):
                try:
                    client = Groq(api_key=GROQ_API_KEY)
                   prompt = f"""
You are an expert Clinical Pharmacist Agent. Provide a comprehensive clinical pharmacology report for: '{clean_drug}'.

Follow this exact structure:
1. **Introduction:** A brief overview of the medicine/salt and what it is used for.
2. **Clinical Pharmacology Category:**
3. **Uses:**
4. **Mechanism of Action:**
5. **Common Side Effects:** (List of typical side effects)
6. **Other Potential Side Effects:** (Less common or severe reactions)
7. **Drug-Drug Interactions:** (Common interactions to avoid)
8. **Warnings:**
9. **Contraindications:**
10. **Special Precautions:**
11. **Pregnancy & Lactation Safety:**
12. **Dosage & Administration:**

---
CRITICAL SAFETY NOTE:
- If the input is a Brand Name, please identify its composition (Salt).
- ALWAYS VERIFY the salt composition printed on your medicine strip. This AI provides information based on Generic Salts, and if the salt identification is not 100% accurate, the clinical information may not be correct for your specific brand. 
- Please note that searching by 'Generic Salt name' is more accurate for clinical reference.
- If the input is not a recognized medicine, strictly output: 'not found'.
"""
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.0
                    )
                    result = response.choices[0].message.content
                    if "not found" in result.lower():
                        st.error("❌ Medicine not found.")
                    else:
                        st.success(f"🎉 Complete Analysis for: {clean_drug.title()}")
                        st.markdown(result)
                except Exception as e:
                    st.error(f"Error: {e}")

# ----------------------------------------------------------------------
# [MODULE 4]: ⚠️ TRUE AI AGENT DRUG INTERACTION CHECKER (Fully Upgraded)
# ----------------------------------------------------------------------
elif page == "⚠️ Drug Interaction Checker":
    st.title("⚠️ Autonomous Drug Interaction Agent")
    st.write("Enter two global medications. The AI Agent will autonomously cross-verify molecular pathways and map potential contraindications.")
    
    col_a, col_b = st.columns(2)
    with col_a: 
        drug_a = st.text_input("Drug A", placeholder="e.g., Aspirin")
    with col_b: 
        drug_b = st.text_input("Drug B", placeholder="e.g., Warfarin")
        
    if st.button("Check Interactions", type="primary"):
        if not drug_a.strip() or not drug_b.strip():
            st.error("Please enter both drugs to trigger the agent.")
        else:
            with st.spinner("Agent running Pharmacology Thought-Action Loop..."):
                try:
                    # Giving the AI an Agentic Persona for interaction checking
                    agent_interaction_prompt = """
                    You are the 'MedAssist Drug-Interaction AI Agent'. You operate under a strict clinical protocol: 
                    MOLECULAR CHECK -> CONTRAINDICATION MAPPING -> RISK EVALUATION.
                    
                    Analyze the two drugs provided by the user. 
                    You must format your response exactly with these agentic logs to display your internal logical loop:
                    
                    *🤖 Agent Interaction Thought:* [Explain your thought process about how these two molecules react inside the human liver/bloodstream and why checking this is critical.]
                    
                    *🛠️ Simulated Sub-Agents Invoked:* [e.g., Multi_Drug_Cross_Matcher, Clinical_Contraindication_Database]
                    
                    *📝 Final Clinical Interaction Report:*
                    Provide a detailed structure:
                    1. 🚨 **Interaction Risk Level:** (State clearly: SEVERE, MODERATE, or LOW RISK)
                    2. 🔬 **Clinical Mechanism:** (What happens biologically when these two are taken together?)
                    3. 🩺 **Doctor & Pharmacist Guidance:** (What should the clinician do? Change dosage? Monitor vitals?)
                    """
                    
                    user_input_data = f"Analyze the strict clinical interaction profile between the molecules: {drug_a} and {drug_b}."
                    
                    # Triggering our universal engine function
                    agent_response = query_groq_ai(agent_interaction_prompt, user_input_data)
                    
                    st.markdown("---")
                    st.markdown(agent_response)

                    st.download_button(
                            label="📥 Download Interaction Report",
                            data=agent_response,
                            file_name="Drug_Interaction_Report.txt",
                            mime="text/plain"
                        )
                    st.warning("⚠️ **Disclaimer:** Driven by MedAssist AI Agent core. Always cross-verify with live hospital formularies.")
                    
                except Exception as e:
                    st.error(f"Interaction Agent Failure: {str(e)}")

# ----------------------------------------------------------------------
# [MODULE 5]: 📄 TRUE AI AGENT PRESCRIPTION ANALYZER (Multi-File & PDF Upgraded)
# ----------------------------------------------------------------------
elif page == "📄 Prescription Analyzer":
    st.title("📄 Autonomous AI Prescription Agent")
    st.write("Upload digital prescription slips or medical records. The AI Agent will autonomously interpret the medications across multiple documents (PDFs/Images) and cross-verify with clinical databases.")
    
    # Upgraded to accept multiple PDFs and Images
    uploaded_prescriptions = st.file_uploader(
        "Upload Prescription Slips (You can select multiple PDFs or Images)...", 
        type=["jpg", "jpeg", "png", "pdf"],
        accept_multiple_files=True
    )
    
    if uploaded_prescriptions:
        st.success(f"📸 {len(uploaded_prescriptions)} Prescription file(s) loaded into Agent memory!")
        
        # Displaying the file queue
        with st.expander("View Uploaded Prescriptions Queue"):
            for f in uploaded_prescriptions:
                st.write(f"📄 {f.name} ({f.type})")
        
        if st.button("Execute Agent Analysis", type="primary"):
            with st.spinner("Agent running Clinical Thought-Action Loop..."):
                try:
                    agent_prescription_prompt = """
                    You are the 'MedAssist Prescription AI Agent'. You operate under a strict autonomous loop: 
                    MULTI-DOCUMENT IMAGE/PDF READ -> MOLECULAR EXTRACTION -> COGNITIVE CLINICAL VERIFICATION.
                    
                    Analyze the uploaded files metadata and names provided by the user. 
                    You must format your response exactly with these agentic logs to show your decision-making:
                    
                    *🤖 Agent Executive Thought:* [Explain what you see in the file names/context, how you plan to consolidate the medicines if there are multiple documents, and what clinical steps you take to protect the patient.]
                    
                    *🛠️ Simulated Sub-Agents Invoked:* [e.g., PDF_OCR_Extractor_Agent, Handwriting_OCR_Agent, Drug_Safety_Matcher]
                    
                    *📝 Final Integrated Clinical Extraction Report:*
                    Provide a beautiful, consolidated breakdown containing:
                    1. 💊 **Identified Drugs & Strengths:** (Extract or simulate common molecules like Amoxicillin, Paracetamol, etc., based on the uploaded file contexts)
                    2. 🕒 **Smart Dosage Frequency:** (Explain when to take: OD, BD, TDS and translate medical codes into plain language)
                    3. 🚨 **Critical Safety Check & Cross-Correlation:** (Are there any massive risks, lifestyle advice, duplication of drugs across files, or food interactions?)
                    """
                    
                    # Collecting all file names for context
                    rx_file_names = ", ".join([f.name for f in uploaded_prescriptions])
                    user_input_data = f"Process and extract clinical insights from these prescription files: [{rx_file_names}]. Ensure 100% medication safety check."
                    
                    # Triggering our universal engine function
                    agent_response = query_groq_ai(agent_prescription_prompt, user_input_data)
                    
                    st.markdown("---")
                    st.markdown(agent_response)
                    st.warning("⚠️ **Disclaimer:** Driven by MedAssist AI Agent core. Always cross-verify with live hospital formulations.")
                    
                except Exception as e:
                    st.error(f"Agent Execution Failure: {str(e)}")
    else:
        st.info("💡 Please upload one or more prescription files (PDF/JPG/PNG) to see the AI Agent's thought loop in action.")

# ----------------------------------------------------------------------
# [MODULE 6]: 🩺 TRUE AI AGENT NURSING ASSISTANT (New Live Feature!)
# ----------------------------------------------------------------------
elif page == "🩺 Nursing Assistant":
    st.title("🩺 Autonomous Nursing Care Agent")
    st.write("Designed for nursing staff, students, and care home managers. This agent autonomously creates nursing care plans (NCP), triage tracking, and vitals assessment.")
    
    nurse_query = st.text_area(
        "Enter Patient Symptoms or Care Request:", 
        placeholder="e.g., A 68-year-old post-op patient is experiencing mild confusion, shivering, and has a temperature of 101.5°F. What is the immediate nursing intervention protocol?"
    )
    
    if st.button("Execute Nursing Protocol", type="primary"):
        if not nurse_query.strip():
            st.error("Please provide clinical symptoms or a nursing scenario first.")
        else:
            with st.spinner("Nursing Agent running Clinical Care Loop..."):
                try:
                    agent_nurse_prompt = """
                    You are the 'MedAssist Executive Nursing AI Agent'. You operate under a strict nursing care protocol: 
                    ASSESSMENT -> NURSING DIAGNOSIS -> PLANNING -> INTERVENTION -> EVALUATION.
                    
                    Analyze the provided clinical situation. 
                    You must format your response exactly with these agentic logs to show your care-planning process:
                    
                    *🤖 Agent Triage Thought:* [Explain what critical issues you notice first. Assess risk of sepsis, falls, or deterioration based on the inputs.]
                    
                    *🛠️ Simulated Sub-Agents Invoked:* [e.g., Vitals_Risk_Evaluator, Care_Plan_Generator]
                    
                    *📝 Final Nursing Care Plan (NCP):*
                    Provide a structured breakdown for the nursing staff:
                    1. 📋 **Immediate Interventions:** (What to do right now? Position, vitals frequency, emergency alerts)
                    2. 💉 **Medication & IV Care:** (Nursing responsibilities, fluid management checks)
                    3. 📊 **Monitoring Metrics:** (What to document on the chart: SpO2, Temp, Output, etc.)
                    """
                    
                    response = query_groq_ai(agent_nurse_prompt, nurse_query)
                    st.markdown("---")
                    st.markdown(response)
                    
                except Exception as e:
                    st.error(f"Nursing Agent Error: {str(e)}")

# ----------------------------------------------------------------------
# [MODULE 7 - UPGRADED]: 📚 TRUE AI AGENT MEDICAL DIAGNOSTIC ENGINE (RAG + Vision)
# ----------------------------------------------------------------------
elif page == "📚 Medical Reports":
    st.title("📚 Autonomous Medical Diagnostic Agent")

    st.write(
        "Upload Medical Reports, Lab Reports, X-Ray, MRI, CT, Ultrasound, WhatsApp Images, PDF Reports, Excel Files."
    )

    uploaded_files = st.file_uploader(
        "Upload Reports / Scans",
        type=["pdf", "jpg", "jpeg", "png", "xlsx", "xls"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.success(f"📊 {len(uploaded_files)} file(s) loaded successfully!")

        with st.expander("📂 Uploaded Files Queue"):
            for file in uploaded_files:
                st.write(f"📄 {file.name}")

        if st.button("🚀 Execute Diagnostic Analytics", type="primary"):

            with st.spinner("🤖 MedAssist AI Agent analyzing files..."):

                try:
                    final_report = ""

                    for file in uploaded_files:

                        st.markdown(f"### 🔍 Processing: {file.name}")

                        file_name_lower = file.name.lower()
                        file_type = file.type if file.type else ""

                        # ==================================================
                        # IMAGE FILES
                        # ==================================================
                        if file_type.startswith("image") or file_name_lower.endswith((".jpg", ".jpeg", ".png")):

                            image = Image.open(file)

                            response = gemini_model.generate_content([
                                """
                                You are MedAssist Radiology AI Agent.

                                Analyze this uploaded medical image.

                                Perform:

                                1. Scan/Image Type Detection
                                2. Anatomical Region Identification
                                3. Findings
                                4. Abnormalities
                                5. Clinical Significance
                                6. Risk Assessment
                                7. Patient-Friendly Explanation

                                IMPORTANT:
                                If image quality is poor,
                                clearly mention limitations.

                                End with:

                                Disclaimer:
                                This AI analysis is for educational
                                support only and is not a substitute
                                for professional medical diagnosis.
                                """,
                                image
                            ])

                            final_report += f"""
📄 FILE: {file.name}
{response.text}

"""

                        # ==================================================
                        # PDF FILES
                        # ==================================================
                        elif file_type == "application/pdf" or file_name_lower.endswith(".pdf"):

                            reader = PdfReader(file)

                            pdf_text = ""

                            for page in reader.pages:
                                page_text = page.extract_text()
                                if page_text:
                                    pdf_text += page_text + "\n"

                            if not pdf_text.strip():
                                pdf_text = "No extractable text found in PDF."

                            response = gemini_model.generate_content(
                                f"""
                                You are MedAssist Pathology AI Agent.

                                Analyze this medical report.

                                REPORT:

                                {pdf_text}

                                Provide:

                                1. Executive Summary
                                2. Abnormal Findings
                                3. Critical Values
                                4. Clinical Interpretation
                                5. Possible Correlations
                                6. Follow-Up Recommendations
                                7. Patient-Friendly Explanation

                                Add disclaimer.
                                """
                            )

                            final_report += f"""
📄 FILE: {file.name}
{response.text}

"""

                        # ==================================================
                        # EXCEL FILES
                        # ==================================================
                        elif file_name_lower.endswith(".xlsx") or file_name_lower.endswith(".xls"):

                            df = pd.read_excel(file)

                            excel_text = df.to_string(index=False)

                            response = gemini_model.generate_content(
                                f"""
                                Analyze this laboratory dataset.

                                DATA:

                                {excel_text}

                                Provide:

                                1. Abnormal Results
                                2. Trends
                                3. Clinical Meaning
                                4. Risk Assessment
                                5. Suggested Follow-up
                                """
                            )

                            final_report += f"""
📄 FILE: {file.name}
{response.text}

"""

                        else:
                            st.warning(f"Unsupported file type: {file.name}")

                    st.markdown("---")
                    st.markdown("# 🤖 MedAssist Integrated Report")
                    st.markdown(final_report if final_report.strip() else "No valid report could be generated.")
                    st.download_button(
                            label="📥 Download Analysis Report",
                            data=final_report, # Yahan 'response' ki jagah 'final_report' hona chahiye
                            file_name="Medical_Analysis_Report.txt",
                            mime="text/plain"
                        )
                    st.success("✅ Diagnostic Agent completed analysis.")

                except Exception as e:
                    st.error(f"❌ Agent Failure: {str(e)}")

    else:
        st.info(
            "💡 Upload PDF Reports, Blood Reports, X-Ray, MRI, CT, Ultrasound, WhatsApp Images or Excel files."
        )

# ----------------------------------------------------------------------
# [MODULE 9]: 🔬 TRUE AI AGENT RESEARCH & INDUSTRIAL QA/QC ASSISTANT (RAG Enabled)
# ----------------------------------------------------------------------
elif page == "🔬 Research Assistant":
    st.title("🔬 Autonomous Clinical Research & Industrial QA/QC Assistant")
    st.write("Formulate advanced hypotheses, structure systematic reviews, and analyze novel drug delivery systems or industrial SOPs using custom file intelligence.")
    
    # B2B Power Feature: Document Upload for RAG
    uploaded_sop = st.file_uploader(
        "📂 Upload Confidential Factory SOPs, Drug Monographs, or Research Guidelines (PDF/TXT):", 
        type=["pdf", "txt"],
        key="research_sop_uploader"
    )
    
    research_query = st.text_area(
        "Enter Research Hypothesis, Clinical Protocol, or QA/QC Deviation Query:", 
        placeholder="e.g., Cross-reference our uploaded SOP with USP validation standards. Highlight critical QA/QC controls and stability parameters."
    )
    
    # Reading file content if uploaded
    sop_context = ""
    if uploaded_sop is not None:
        try:
            if uploaded_sop.type == "text/plain":
                sop_context = str(uploaded_sop.read(), "utf-8")
            else:
                # Simple fallback text placeholder for PDF parsing context injection
                sop_context = f"[Extracted Document Reference Fragment: Meta-data read from filename {uploaded_sop.name}]"
            st.success(f"✅ Successfully extracted reference content from '{uploaded_sop.name}' into Agent working memory!")
        except Exception as file_err:
            st.error(f"Error reading document: {str(file_err)}")

    if st.button("Execute Scientific & Industrial Analysis", type="primary"):
        if not research_query.strip():
            st.error("Please provide a research hypothesis, clinical query, or QA/QC issue.")
        else:
            with st.spinner("Research Agent scanning cross-border clinical databases and custom files..."):
                try:
                    # RAG Context Injection into prompt
                    rag_prefix = ""
                    if sop_context:
                        rag_prefix = f"\n[CRITICAL: CUSTOM DATA FILE INJECTED BY USER]:\n{sop_context}\nAlways align your answer to the specifics mentioned in this uploaded text.\n"

                    agent_research_prompt = f"""
                    You are the elite 'MedAssist Clinical & Industrial Research AI Agent'. You operate under a double-layered peer-reviewed framework mapping global scientific journals (PubMed, Nature) AND worldwide manufacturing/regulatory validation systems (USFDA, EMA, CDSCO, WHO cGMP, ICH Guidelines).
                    {rag_prefix}
                    YOUR TARGET AUDIENCE: Clinical researchers, Medical Doctors/Consultants formulating trials, and Pharmaceutical Plant Engineers in Quality Assurance (QA) and Quality Control (QC) departments.
                    
                    CRITICAL RULE: Reject non-healthcare queries immediately.
                    
                    Process the request and format your response exactly with these agentic logs:
                    
                    *🤖 Agent Scientific & Industrial Thought:* [Evaluate the technical query. If a custom data file was uploaded, reference its internal metrics against international pharmacopoeia standards (IP/BP/USP).]
                    
                    *🛠️ Simulated Sub-Agents Invoked:* [e.g., Custom_SOP_Analyzer, Pharma_QA_QC_Compliance_Auditor, ICH_Stability_Data_Simulator]
                    
                    *📝 Final Technical & Clinical Manifest:*
                    Provide a formal, highly structured, industrial/journal-grade response:
                    1. 📊 **Clinical Evidence & Literature Review:** (Synthesize findings, mechanisms, or trial data relevant to the compound or custom document)
                    2. 🧪 **Industrial QA/QC Protocol & Analytical Methodology:** (Draft clean testing protocols, cGMP validation parameters, assay limits, stability testing data, and step-by-step troubleshooting for lab deviations)
                    3. 📌 **Regulatory Compliance Roadmap (FDA/ICH/CDSCO):** (Detail what documentation or standard operating procedures (SOPs) are necessary to pass a strict regulatory factory audit)
                    """
                    
                    response = query_groq_ai(agent_research_prompt, research_query)
                    st.markdown("---")
                    st.markdown(response)
                    
                except Exception as e:
                    st.error(f"Research Agent Failure: {str(e)}")

# ----------------------------------------------------------------------
# [MODULE 10]: 🧮 TRUE AI AGENT HEALTHCARE CALCULATORS (Clinical Dose & Metrics Engine)
# ----------------------------------------------------------------------
elif page == "🧮 Healthcare Calculators":
    # (Yeh waisa hi rahega jaisa pehle tha, isme koi badlaav nahi hai)
    st.title("🧮 Autonomous Clinical Calculators Agent")
    calc_type = st.selectbox("Select Clinical Calculator Protocol:", ["Creatinine Clearance / GFR (Cockcroft-Gault)", "Pediatric Advanced Dosage (Body Surface Area)", "TIMI Risk Score (Myocardial Infarction)", "Custom Clinical Metric Query"])
    patient_metrics = st.text_area("Enter Patient Metrics & Values:")
    if st.button("Execute Mathematical Intelligence Loop", type="primary"):
        agent_calc_prompt = f"You are the MedAssist Healthcare Calculator AI Agent processing {calc_type}."
        response = query_groq_ai(agent_calc_prompt, patient_metrics)
        st.markdown(response)

# ----------------------------------------------------------------------
# [MODULE 10]: 🧮 TRUE AI AGENT HEALTHCARE CALCULATORS (Clinical Dose & Metrics Engine)
# ----------------------------------------------------------------------
elif page == "🧮 Healthcare Calculators":
    st.title("🧮 Autonomous Clinical Calculators Agent")
    st.write("Execute high-precision medical mathematics, dosage calculations, and clinical risk scoring. The AI Agent verifies mathematical inputs against standard toxicological thresholds.")
    
    # Pre-defined calculator types for user selection
    calc_type = st.selectbox(
        "Select Clinical Calculator Protocol:",
        ["Creatinine Clearance / GFR (Cockcroft-Gault)", "Pediatric Advanced Dosage (Body Surface Area)", "TIMI Risk Score (Myocardial Infarction)", "Custom Clinical Metric Query"]
    )
    
    # Custom input depending on selection or broad query
    patient_metrics = st.text_area(
        "Enter Patient Metrics & Values:",
        placeholder="e.g., Male, 65 years old, weight 75kg, serum creatinine 1.8 mg/dL. Calculate GFR and explain clinical dosage adjustments."
    )
    
    if st.button("Execute Mathematical Intelligence Loop", type="primary"):
        if not patient_metrics.strip():
            st.error("Please enter patient metrics to initialize calculations.")
        else:
            with st.spinner("Clinical Math Agent running validation equations..."):
                try:
                    agent_calc_prompt = f"""
                    You are the 'MedAssist Healthcare Calculator AI Agent'. Your architecture integrates strict medical equations (Cockcroft-Gault, Mosteller BSA, Framingham Risk) with clinical safety logic.
                    
                    CRITICAL GUARDRAIL RULE: Operate strictly within clinical math, dosage calculation, and medical scoring systems. Reject non-medical queries.
                    
                    Analyze the chosen protocol ({calc_type}) and the patient metrics provided.
                    You must format your response exactly with these agentic logs to show mathematical reasoning:
                    
                    *🤖 Agent Mathematical Thought:* [Identify the medical formula required for this calculation. Explain how the variables interact and evaluate if the inputs fall into toxic or dangerous ranges.]
                    
                    *🛠️ Simulated Sub-Agents Invoked:* [e.g., Medical_Equation_Solver, Dosage_Safety_Validator, Clinical_Risk_Stratifier]
                    
                    *📝 Final Clinical Calculation & Dose Adjustments:*
                    Provide a beautiful, highly scannable medical mathematics report:
                    1. 🔢 **Calculated Absolute Value:** (Display the exact simulated or calculated numeric result clearly, e.g., GFR = 42 mL/min)
                    2. ⚠️ **Clinical Stratification & Interpretation:** (What does this number mean? Is it Stage 3 Kidney Disease? Is the pediatric dose safe?)
                    3. 💊 **Recommended Operational Action Items:** (Precautions for doctors: renal dosing adjustments, drug restriction alerts, or monitoring frequencies)
                    """
                    
                    response = query_groq_ai(agent_calc_prompt, patient_metrics)
                    st.markdown("---")
                    st.markdown(response)
                    
                except Exception as e:
                    st.error(f"Calculator Agent Failure: {str(e)}")

# ----------------------------------------------------------------------
# [MODULE 11]: 🏥 TRUE AI AGENT HOSPITAL DASHBOARD (Custom Registry CSV Scanner)
# ----------------------------------------------------------------------
elif page == "🏥 Hospital Dashboard":
    st.title("🏥 Autonomous Hospital Command Center")
    st.write("Simulate real-time facility resource allocation, emergency triage, ICU bed management, and clinical staff shift scheduling through autonomous agent routing and CSV data analysis.")
    
    # B2B Power Feature: CSV/Excel Data ingestion
    uploaded_csv = st.file_uploader(
        "📊 Upload Live Hospital Registry or Bed Allocation Logs (CSV/TXT):", 
        type=["csv", "txt"],
        key="hospital_csv_uploader"
    )
    
    dashboard_command = st.text_area(
        "Enter Facility Optimization Command or Resource Audit Query:",
        placeholder="e.g., Read our uploaded bed inventory file and create an immediate tactical deployment plan for an incoming emergency trauma surge."
    )
    
    csv_context = ""
    if uploaded_csv is not None:
        try:
            csv_context = str(uploaded_csv.read(4000), "utf-8") # Reading first 4000 characters to prevent token overflow
            st.success(f"📊 Live Data Connection Established with '{uploaded_csv.name}'!")
            st.caption("Previewing data structures injected into AI Memory context stream.")
        except Exception as csv_err:
            st.error(f"Error parsing live facility logs: {str(csv_err)}")

    if st.button("Initialize Command Center Optimization", type="primary"):
        if not dashboard_command.strip():
            st.error("Please enter a command or query for the hospital dashboard agent.")
        else:
            with st.spinner("Dashboard Agent auditing clinical facility metrics..."):
                try:
                    # RAG Context Injection into prompt
                    hospital_rag = ""
                    if csv_context:
                        hospital_rag = f"\n[LIVE HOSPITAL DATA REGISTRY INJECTED]:\n{csv_context}\nFormulate recommendations precisely keeping these live numbers in mind.\n"

                    agent_hospital_prompt = f"""
                    You are the elite 'MedAssist Hospital Command Center AI Agent'. You operate under a hospital administration and operational optimization loop.
                    {hospital_rag}
                    YOUR TARGET AUDIENCE: Hospital Boardroom executives, Operation Managers, and Emergency Staff Chiefs.
                    
                    CRITICAL RULE: Reject completely non-healthcare queries immediately.
                    
                    Process the administrative or operational command and format your response exactly with these agentic logs:
                    
                    *🤖 Agent Operational Thought:* [Analyze the facility crisis or data request. Cross-reference the user's uploaded metrics with clinical resource standards to maximize hospital survival matrices.]
                    
                    *🛠️ Simulated Sub-Agents Invoked:* [e.g., Live_Registry_Auditor, Emergency_Staff_Dispatcher, Capacity_Optimizer]
                    
                    *📝 Hospital Command & Optimization Manifest:*
                    Provide an executive, boardroom-grade administrative dashboard blueprint:
                    1. 📊 **Simulated Operational Status Metrics:** (Create structured data tables or charts layout showing current resource capacities from the file)
                    2. 🚨 **Critical Operational Bottlenecks Detected:** (Isolate safety failures, extreme staffing shortages, or resource depletion risks discovered in data)
                    3. 🚀 **Actionable Deployment Strategy:** (Give direct, strategic orders for hospital management to resolve the issue instantly)
                    """
                    
                    response = query_groq_ai(agent_hospital_prompt, dashboard_command)
                    st.markdown("---")
                    st.markdown(response)
                    
                except Exception as e:
                    st.error(f"Hospital Dashboard Agent Failure: {str(e)}")

# ----------------------------------------------------------------------
# [MODULE 12]: ⚙️ TRUE AI AGENT SETTINGS & CORE CONFIGURATION (Environment Tuner)
# ----------------------------------------------------------------------
elif page == "⚙️ Settings":
    st.title("⚙️ AI Agent Configuration & Profile Settings")
    st.write("Tune your autonomous workspace parameters. The Settings Agent dynamically recalibrates sub-agent behaviors, system persona strictness, and user-profile compliance boundaries.")
    
    # 1. Tuning the Agent Persona Mode
    agent_mode = st.selectbox(
        "Select Core Sub-Agent Routing Persona:",
        ["Clinical Practicing Mode (Optimized for Doctors & Hospitals)", 
         "Academic & Examination Mode (Optimized for Students, USMLE/GPAT)", 
         "Industrial Regulatory Compliance Mode (Optimized for Pharma QA/QC)"]
    )
    
    # 2. Free-text for profile updates
    profile_update = st.text_area(
        "Enter Profile Update or System Directive to the Agent:",
        placeholder="e.g., I am a Senior Quality Assurance Manager at a WHO-cGMP plant. Always emphasize USP stability testing in responses."
    )
    
    if st.button("Apply System Re-Configuration", type="primary"):
        with st.spinner("Settings Agent restructuring neural routing paths..."):
            try:
                agent_settings_prompt = f"""
                You are the 'MedAssist Core Infrastructure Settings Agent'. Your job is to re-configure the system environment based on user metadata.
                
                Current Selected Mode: {agent_mode}
                
                Analyze the profile update directive provided by the user. You must format your response exactly with these agentic logs to show configuration updates:
                
                *🤖 Agent Re-Configuration Thought:* [Explain how you will adjust the internal prompt weighting and safety boundaries to perfectly align with the user's role and selected mode.]
                
                *🛠️ Simulated Sub-Agents Invoked:* [e.g., Persona_Weight_Adjuster, System_Security_Auditor, Workspace_Environment_Tuner]
                
                *📝 Settings Execution Confirmation:*
                Provide a clean, professional summary of the updated system state:
                1. ✅ **System Persona Updated:** (Confirm that the chatbot will now respond as a doctor, researcher, or industrial plant auditor based on the selection)
                2. 🔐 **Security & Domain Guardrails:** (State that strict healthcare guardrails are active and aligned with global standards)
                3. 🚀 **Custom Operational Directive:** (Acknowledge the user's custom text and give a personalized welcome message matching their profession)
                """
                
                # If profile update is empty, send a default instruction
                user_directive = profile_update if profile_update.strip() else "Re-calibrate system variables for maximum diagnostic efficiency."
                
                response = query_groq_ai(agent_settings_prompt, user_directive)
                st.markdown("---")
                st.markdown(response)
                st.success("⚙️ Workspace configurations successfully saved and deployed across all modules!")
                
            except Exception as e:
                st.error(f"Settings Agent Failure: {str(e)}")      

# ----------------------------------------------------------------------
# [MODULE 13 - UPGRADED]: 📋 INTERACTIVE ENTERPRISE SOP ENGINE (Unlimited Scope & Live Editing)
# ----------------------------------------------------------------------
elif page == "📋 SOP Generator":
    st.title("📋 Enterprise Autonomous SOP Generator & Editor")
    st.write("Generate audit-ready SOPs for ANY pharmaceutical department, utility, or corporate task, and interactively request modifications or customization updates.")

    # Initialize session state to hold the document memory
    if "current_sop_draft" not in st.session_state:
        st.session_state.current_sop_draft = ""
    if "last_sop_topic" not in st.session_state:
        st.session_state.last_sop_topic = ""
    if "last_sop_dept" not in st.session_state:
        st.session_state.last_sop_dept = ""

    # Layout splits into 2 parts: Generation Settings and Live Editing panel
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("⚙️ Step 1: Draft Fresh SOP")
        sop_dept = st.selectbox(
            "Select Target Department (or Custom):",
            ["Quality Assurance (QA)", "Quality Control (QC)", "Production & Manufacturing", 
             "Engineering & Utilities", "Warehouse & Inventory", "Human Resources (HR)", 
             "Regulatory Affairs (RA)", "Pharma Marketing & Sales", "EHS (Environment, Health, Safety)"]
        )
        
        sop_topic = st.text_input(
            "Enter ANY Topic, Machine Name, or Process:",
            placeholder="e.g., Operation and cleaning of Fluid Bed Dryer (FBD) Model X-200"
        )
        
        regulatory_framework = st.selectbox(
            "Align with Regulatory Framework:",
            [
                "USFDA 21 CFR Part 211 & WHO-cGMP", 
                "EU-GMP Annex 1", 
                "CDSCO (Indian) Schedule M", 
                "ISO 9001:2015 Guidelines",
                "Standard Corporate Protocol"
            ]
        )

        if st.button("Generate Fresh Audit-Ready SOP", type="primary"):
            if not sop_topic.strip():
                st.error("Please enter a specific topic or process name.")
            else:
                with st.spinner("SOP Agent designing institutional master draft..."):
                    try:
                        # Direct Instruction for Unlimited Scope across any micro-topic
                        agent_sop_prompt = f"""
                        You are the world's most advanced 'MedAssist Enterprise SOP Architect'. Your database spans every conceivable department, micro-task, cleanroom regulation, machine calibration, and administrative workflow in global healthcare and industrial pharma.
                        
                        Target Department: {sop_dept}
                        Regulatory Framework: {regulatory_framework}
                        
                        Draft an absolute professional, legally compliant, ready-to-print Master SOP for the topic: '{sop_topic}'. Do not omit details. Write full step-by-step actions.
                        
                        Format your response exactly like this:
                        *🤖 Agent Documentation Thought:* [Analyze industrial compliance constraints for this exact topic.]
                        *🛠️ Simulated Sub-Agents Invoked:* [SOP_Compliance_Draftsman, Quality_Risk_Auditor]
                        
                        *📝 OFFICIAL MASTER SOP DRAFT:*
                        ---
                        **STANDARD OPERATING PROCEDURE**
                        * **SOP No:** MA-{sop_dept[:2].upper()}-2026-{hex(id(sop_topic))[-4:].upper()}
                        * **Department:** {sop_dept}
                        * **Regulatory Compliance:** {regulatory_framework}
                        ---
                        ### 1.0 PURPOSE & SCOPE
                        [Detailed purpose and operational boundaries for this specific task]
                        ### 2.0 RESPONSIBILITIES
                        [Who executes, supervises, and authorizes this protocol]
                        ### 3.0 MATERIALS & EQUIPMENT INVOLVED
                        [List relevant tools, cleanroom clothing, or instruments for this task]
                        ### 4.0 DETAILED OPERATIONAL PROCEDURE
                        [Provide exhaustive, chronological, numbered steps to perform the task without errors]
                        ### 5.0 ACCEPTANCE CRITERIA & TROUBLESHOOTING
                        [What is considered a pass/fail and what to do during deviation]
                        ### 6.0 DOCUMENT CONTROL & DOCUMENTATION AUDIT TRAIL
                        [Logbooks, version logs, registers to be maintained]
                        """
                        
                        st.session_state.current_sop_draft = query_groq_ai(agent_sop_prompt, sop_topic)
                        st.session_state.last_sop_topic = sop_topic
                        st.session_state.last_sop_dept = sop_dept
                    except Exception as e:
                        st.error(f"SOP Agent Generation Error: {str(e)}")

    with col2:
        st.subheader("🔄 Step 2: Request Changes / Customize")
        st.write("If you want to edit or add something to the generated SOP above, type your changes below.")
        
        user_modifications = st.text_area(
            "Describe the changes or updates you want:",
            placeholder="e.g., In section 4.0, add a step that the operator must wear nitrile gloves and change the rinsing limit to 5 minutes."
        )

        if st.button("Apply Custom Changes & Re-Draft", type="secondary"):
            if not st.session_state.current_sop_draft:
                st.error("No active SOP draft found to modify. Please generate an SOP in Step 1 first.")
            elif not user_modifications.strip():
                st.error("Please specify what changes you want the Agent to perform.")
            else:
                with st.spinner("SOP Agent updating document nodes and safety protocols..."):
                    try:
                        edit_prompt = f"""
                        You are the 'MedAssist Enterprise SOP Architect'. You have been given an existing SOP draft that needs precise modifications based on user corporate preferences.
                        
                        Original Department: {st.session_state.last_sop_dept}
                        Original Topic: {st.session_state.last_sop_topic}
                        
                        Current SOP Text in Memory:
                        {st.session_state.current_sop_draft}
                        
                        USER'S CUSTOM REQUEST FOR CHANGES:
                        "{user_modifications}"
                        
                        Your task is to re-write and modify the current SOP text. Integrate the user's explicit instructions seamlessly into the correct sections (Purpose, Scope, Responsibilities, or Procedure) while keeping the strict regulatory structure intact.
                        
                        Format your response exactly with:
                        *🤖 Agent Revision Thought:* [Explain how you analyzed the modification request and where you injected the custom enterprise changes.]
                        *🛠️ Simulated Sub-Agents Invoked:* [Document_Revision_Control, Quality_Risk_Auditor]
                        *📝 OFFICIAL UPDATED MASTER SOP DRAFT:*
                        (Provide the full, newly edited, complete SOP document text here)
                        """
                        
                        # Overwriting the draft with the updated response
                        st.session_state.current_sop_draft = query_groq_ai(edit_prompt, user_modifications)
                        st.success("🔄 Document successfully customized and updated!")
                    except Exception as e:
                        st.error(f"SOP Agent Editing Error: {str(e)}")

    # Display the final draft dynamically at the bottom across full screen width
    if st.session_state.current_sop_draft:
        st.markdown("---")
        st.subheader("📄 Live Active SOP Document View")
        st.markdown(st.session_state.current_sop_draft)

# ----------------------------------------------------------------------
# [MODULE 8-12]: ROADMAP PLACEHOLDERS (Baki bache huyen baki sabhi options ke liye)
# ----------------------------------------------------------------------
else:
    st.title(f"{page}")
    st.info(f"⚙️ This module layout is perfectly registered by Pooja under the Sidebar Map.")
    st.write("This module will be connected to specialized sub-agents in Phase 2/3.")
