import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import streamlit as st

from app.analyzer import analyze_code, run_flake8
from app.complexity import analyze_complexity
from app.quality_checker import check_quality
from app.ai_explainer import explain_issue, fix_code, review_code
from app.security_checker import check_security
from app.report_generator import generate_report

st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide"
)

# -------------------------
# Session State
# -------------------------

if "current_code" not in st.session_state:
    st.session_state.current_code = ""
    
if "report" not in st.session_state:
    st.session_state.report = ""

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "fixed_code" not in st.session_state:
    st.session_state.fixed_code = ""

if "ai_review" not in st.session_state:
    st.session_state.ai_review = ""

# -------------------------
# Title
# -------------------------

st.title("🤖 AI Code Reviewer")

st.write(
    "Upload Python code or paste code to get AI-powered review, "
    "complexity analysis, explanations and automatic fixes."
)

# -------------------------
# Input
# -------------------------

uploaded_file = st.file_uploader(
    "📂 Upload Python File",
    type=["py"]
)

pasted_code = st.text_area(
    "📝 Or paste your Python code here",
    height=250
)

code = ""

if uploaded_file:

    code = uploaded_file.read().decode("utf-8")

elif pasted_code.strip():

    code = pasted_code

if code:

    st.session_state.current_code = code

st.subheader("📝 Your Code")

if st.session_state.current_code:

    st.code(
        st.session_state.current_code,
        language="python"
    )

# -------------------------
# Main Review Button
# -------------------------

if st.button(
    "🔍 Review Code"
):

    st.session_state.analysis_done = True
    st.session_state.ai_review = ""
    st.session_state.fixed_code = ""


# -------------------------
# Analysis
# -------------------------

if st.session_state.analysis_done:


    code = st.session_state.current_code


    (
        functions,
        loops,
        classes,
        imports,
        variables,
        lines,
        syntax_error
    ) = analyze_code(code)



    if syntax_error:

        st.error(
            "❌ Syntax Error Found"
        )

        st.write(
            syntax_error
        )

    else:

        complexity = analyze_complexity(code)

        os.makedirs(
            "app/test_files",
            exist_ok=True
        )

        temp_file = (
            "app/test_files/uploaded_code.py"
        )

        with open(
            temp_file,
            "w"
        ) as file:

            file.write(code)



        quality = check_quality(
            temp_file
        )


        issues = run_flake8(
            temp_file
        )
        security_issues = check_security(code)

        # -------------------------
        # Tabs
        # -------------------------

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
            [
                "📌 Code Analysis",
                "⚡ Complexity",
                "🔍 Quality Report",
                "🛡️ Security Report",
                "🤖 AI Review",
                "🛠 Fix Code",
                "📄 Report"
            ]
        )

        # -------------------------
        # Code Analysis
        # -------------------------

        with tab1:


            st.subheader(
                "📌 Code Analysis"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Functions",
                    len(functions)
                )

                st.metric(
                    "Classes",
                    len(classes)
                )

                st.metric(
                    "Lines",
                    lines
                )


            with col2:

                st.metric(
                    "Loops",
                    len(loops)
                )

                st.metric(
                    "Imports",
                    len(imports)
                )

                st.metric(
                    "Variables",
                    len(variables)
                )
                
        # -------------------------
        # Complexity
        # -------------------------

        with tab2:


            st.subheader(
                "⚡ Complexity Analysis"
            )


            st.write(
                "### Time Complexity"
            )

            st.success(
                complexity["time_complexity"]
            )


            st.write(
                complexity["explanation"]
            )


            st.write(
                "### Space Complexity"
            )


            st.success(
                complexity["space_complexity"]
            )


            st.write(
                complexity["space_reason"]
            )

        # -------------------------
        # Quality Report
        # -------------------------

        with tab3:


            st.subheader(
                "🔍 Code Quality Report"
            )

            if issues:


                st.warning(
                    "Issues Found"
                )


                for issue in issues:

                    st.error(
                        f"{issue['severity']} : {issue['message']}"
                    )

            else:

                st.success(
                    "✅ No quality issues found"
                )


           # -------------------------
                # Security Report
            # -------------------------

        with tab4:

           st.subheader(
            "🛡 Security Report"
           )


        if security_issues:


           for issue in security_issues:


                if issue["severity"] == "Critical":

                    st.error(
                      f"🚨 {issue['severity']}: {issue['problem']}"
                    )

                else:

                    st.warning(
                       f"⚠️ {issue['severity']}: {issue['problem']}"
                    )

                st.write(
                   "Reason:"
                )

                st.write(
                   issue["reason"]
                )


                st.write(
                   "Solution:"
                )

                st.write(
                    issue["solution"]
                )

        else:

           st.success(
                "✅ No security issues detected."
            )
           
        # -------------------------
        # AI Review
        # -------------------------

        with tab5:

            st.subheader(
                "🤖 AI Code Review"
            )


            if st.button(
                "Generate AI Review",
                key="ai_button"
            ):


                with st.spinner(
                    "AI reviewing code..."
                ):


                    try:

                        st.session_state.ai_review = review_code(
                            code
                        )


                    except Exception as e:

                        st.session_state.ai_review = (
                            f"Error: {e}"
                        )

            # if st.session_state.ai_review:

            #     st.markdown(
            #         st.session_state.ai_review
            #     )

            if st.session_state.ai_review:

                review_text = st.session_state.ai_review

                 # Extract Quality Score

                score = None

                if "Code Quality Score" in review_text:

                    try:

                        score_part = review_text.split(
                            "Code Quality Score"
                        )[1]


                        score = score_part.split(
                            "/10"
                        )[0].strip()

                    except:

                       score = None

                if score:

                   st.metric(
                      "📊 Code Quality Score",
                      f"{score}/10"
                    )

                # Remove score section before displaying AI text

                clean_review = review_text


                if "📊 Code Quality Score" in clean_review:

                    parts = clean_review.split(
                        "❌ Problems Found"
                    )

                    if len(parts) > 1:

                        clean_review = (
                           "❌ Problems Found"
                           + parts[1]
                        )

                st.markdown(
                    clean_review 
                ) 
            
        # -------------------------
        # Fix Code
        # -------------------------

        with tab6:

            st.subheader(
                "🛠 Automatic Code Fix"
            )

            if st.button(
                "Generate Fixed Code",
                key="fix_button"
            ):

                with st.spinner(
                    "AI fixing code..."
                ):

                    try:

                        st.session_state.fixed_code = fix_code(
                            code
                        )

                    except Exception as e:

                        st.error(
                            f"Fix Error: {e}"
                        )

            if st.session_state.fixed_code:


                st.success(
                    "Fixed Code Generated"
                )

                st.code(
                    st.session_state.fixed_code,
                    language="python"
                )

                st.download_button(

                    label="⬇ Download Fixed Code",

                    data=st.session_state.fixed_code,

                    file_name="fixed_code.py",

                    mime="text/python"

                )
            # -------------------------
                # Report Generation
            # -------------------------

        with tab7:

            st.subheader(
               "📄 Generate Report"
            )
            
            if st.button(
                "Create Review Report",
                key="report_button"
            ):

                try:

                    report = generate_report(

                        functions,
                        classes,
                        loops,
                        imports,
                        variables,
                        lines,
                        complexity,
                        issues,
                        security_issues,
                        st.session_state.ai_review

                    )

                    st.session_state.report = report

                    st.success(
                       "Report generated successfully"
                    )

                except Exception as e:

                    st.error(
                        f"Report Error: {e}"
                    )

            if st.session_state.report:

                st.download_button(

                    label="⬇ Download Report",

                    data=st.session_state.report,

                    file_name="AI_Code_Review_Report.txt",

                    mime="text/plain"

                )