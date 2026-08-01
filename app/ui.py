from analyzer import analyze_code
from complexity import analyze_complexity
from quality_checker import check_quality
from security_checker import check_security
import tempfile
import os

from ai_explainer import review_code, fix_code
import streamlit as st
from pathlib import Path

# =====================================
# PAGE CONFIG
# =====================================

def configure_page():
    st.set_page_config(
        page_title="AI Code Reviewer",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    ) 
    
    session_defaults = {
        "analysis": None,
        "complexity": None,
        "security": None,
        "quality": None,
        "review": None,
        "fixed_code": None,
        "analysis_done": False,
    }

    for key, value in session_defaults.items():
        st.session_state.setdefault(key, value)
        
# =====================================
# LOAD CSS
# =====================================

def load_css():
    css_file = Path(__file__).parent / "assets" / "styles.css"

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )
      
def get_quality_report(code):
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".py",
        mode="w",
        encoding="utf-8"
    ) as temp:
        temp.write(code)
        temp_path = temp.name

    try:
        return check_quality(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.markdown("# 🤖 AI Code Reviewer")

    st.markdown(
        "<p style='color:#9FB6D9;'>Professional Python Analysis Platform</p>",
        unsafe_allow_html=True
    )

    st.divider()
    
    st.markdown("""
🏠 Dashboard

🧠 AI Code Review

⚡ Complexity Analysis

🛡 Security Scan

📊 Quality Report

🛠 Automatic Code Fix

📄 Report Generation
""")

    st.markdown(
    """
<div class="sidebar-footer">

<p><strong>Version</strong> 1.0</p>

<p>Built with Python + Streamlit</p>

<p>Powered by Groq AI</p>

</div>
""",
    unsafe_allow_html=True
)
        
def render_hero():
    st.markdown(
        """
<div class="hero-container">

<div class="hero-badge">
🚀 Professional AI-Powered Code Analysis Platform
</div>

<div class="hero-header">

<div class="hero-logo">
🔍
</div>

<div>
<div class="hero-title">
AI Code Reviewer
</div>

<div class="hero-subtitle">
Professional Static Analysis & AI-Powered Code Review for Python
</div>
</div>

</div>

<div class="hero-description">
Analyze Python source code for syntax errors, complexity,
security vulnerabilities, code quality, maintainability,
and receive AI-powered review with automatic code improvement
from one professional dashboard.
</div>

<div class="hero-badges">
<span>🐍 Python</span>
<span>🤖 Groq AI</span>
<span>🌳 AST Analysis</span>
<span>🛡 Security</span>
<span>📈 Quality</span>
<span>⚡ Complexity</span>
</div>

</div>
""",
        unsafe_allow_html=True,
    )      
    
# =====================================
# FEATURE CARDS
# =====================================

def render_analysis_metrics(functions, classes, loops, lines, imports, variables, error):

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Functions", len(functions))

    with c2:
        st.metric("Classes", len(classes))

    with c3:
        st.metric("Loops", len(loops))

    with c4:
        st.metric("Lines", lines)

    c5, c6, c7 = st.columns(3)

    with c5:
        st.metric("Imports", len(imports))

    with c6:
        st.metric("Variables", len(variables))

    with c7:
        st.metric("Errors", 0 if error is None else 1)

# =====================================
# INPUT SECTION
# =====================================

def render_input_section():
    
    left, right = st.columns([1, 2], gap="large")

    with left:

        st.markdown(
            '<div class="section-title">📂 Upload Python File</div>',
            unsafe_allow_html=True
        )

        uploaded_file = st.file_uploader(
            "Choose Python File",
            type=["py"],
            label_visibility="collapsed"
        )

    with right:

        st.markdown(
            '<div class="section-title">💻 Code Editor</div>',
            unsafe_allow_html=True
        )

        code = st.text_area(
            "Python Code",
            height=430,
            placeholder="Paste your Python code here...",
            label_visibility="collapsed"
        )
    
    return uploaded_file, code
# =====================================
# ANALYSIS SECTION
# =====================================

def render_analysis(uploaded_file, code):
    
    analyze = st.button(
        "🚀 Analyze Code",
        width="stretch"
    )

    # When Analyze is clicked
    if analyze:
        st.session_state.analysis_done = True

    if not st.session_state.analysis_done:
        return
        
    if uploaded_file:
        code = uploaded_file.read().decode("utf-8")
         
    if analyze:

        for key in (
            "analysis",
            "complexity",
            "security",
            "quality",
            "review",
            "fixed_code",
        ):
            st.session_state[key] = None

    if not code.strip():
        st.warning("Please upload or paste Python code.")
        return   

    if analyze:
        
        with st.spinner("🤖 AI is reviewing your code..."):

            st.session_state.analysis = analyze_code(code)     

    analysis = st.session_state.analysis
    
    if analysis is None:
        return

    functions, loops, classes, imports, variables, lines, error = analysis

    st.success("Analysis Completed Successfully ✅")
    
    st.markdown("""
    <div class="dashboard-card">
    <div class="dashboard-title">
    📄 Your Code
    </div>
    """, unsafe_allow_html=True)

    st.code(
        code,
        language="python"
    )

    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("")
     
    st.markdown("""
    <div class="dashboard-card">
    <div class="dashboard-title">
    📊 Analysis Dashboard
    </div>
    """, unsafe_allow_html=True)


    render_analysis_metrics(
        functions,
        classes,
        loops,
        lines,
        imports,
        variables,
        error
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("")

    st.markdown("## 📝 AI Summary")

    complexity = st.session_state.complexity
    if complexity is None:
        complexity = analyze_complexity(code)
        st.session_state.complexity = complexity
    
    
    security_issues = st.session_state.security
    if security_issues is None:
        security_issues = check_security(code)
        st.session_state.security = security_issues

    quality = st.session_state.quality
    if quality is None:
        quality = get_quality_report(code)
        st.session_state.quality = quality

    summary = f"""
    ✅ Functions detected: {len(functions)}

    ✅ Loops detected: {len(loops)}

    ✅ Time Complexity: {complexity.get("Estimated Time Complexity", "N/A")}

    ✅ Space Complexity: {complexity.get("Estimated Space Complexity", "N/A")}

    ✅ Security: {"PASS" if not security_issues else "WARNING"}

    ✅ Quality Score: {quality["score"]}/100
    """

    st.markdown(summary)
    
    tabs = st.tabs([
        "📊 Overview",
        "⚡ Complexity",
        "🛡 Security",
        "📈 Quality",
        "🤖 AI Review",
        "🛠 Code Fix",
        "📄 Report"
    ])
    
    with tabs[0]:
         
        st.write("### 🔹 Functions")

        if functions:
            st.code("\n".join(functions), language="text")
        else:
            st.info("No functions found.")


        st.write("### 🔹 Classes")

        if classes:
            st.code("\n".join(classes), language="text")
        else:
            st.info("No classes found.")
                 
        st.write("### 🔹 Imports")

        if imports:
            st.code("\n".join(imports), language="text")
        else:
            st.info("No imports found.")

        st.write("### 🔹 Variables")

        if variables:
            st.code("\n".join(variables), language="text")
        else:
            st.info("No variables found.")
              
    with tabs[1]:
        
        if st.session_state.complexity is None:
            st.session_state.complexity = analyze_complexity(code)
            
        complexity = st.session_state.complexity
        
        
        if complexity is None:

            st.warning("Please analyze the code first.")
        
        else:

            st.markdown("## ⚡ Complexity Analysis")

            if "error" in complexity:

                st.error(complexity["error"])

            else:

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Functions",
                        complexity["Functions"]
                    )

                    st.metric(
                        "Loops",
                        complexity["Loops"]
                    )

                    st.metric(
                        "Nested Loops",
                        complexity["Nested Loops"]
                    )

                with col2:

                    st.metric(
                        "Time Complexity",
                        complexity["Estimated Time Complexity"]
                    )

                    st.metric(
                        "Space Complexity",
                        complexity["Estimated Space Complexity"]
                    )
        
    with tabs[2]:
        
        if st.session_state.security is None:
            st.session_state.security = check_security(code)

        security_issues = st.session_state.security
        
        st.markdown("## 🛡 Security Scan")

        if not security_issues:

            left, right = st.columns(2)

            with left:
                st.success("✅ No security issues detected")

            with right:
                st.metric("Risk Score", "LOW")
                st.metric("Issues Found", 0)
                st.metric("Security Status", "PASS")
                
                st.progress(1.0)

                st.caption("100% Secure")

        else:

            left, right = st.columns(2)

            with left:
                st.metric("Issues Found", len(security_issues))

            with right:
                
                st.metric("Security Status", "WARNING")
                
                security_score = max(0, 1 - (len(security_issues) * 0.2))

                st.progress(security_score)

                st.caption(f"{int(security_score * 100)}% Security Score")

            st.error("Security issues were found in the code.")

            for issue in security_issues:

                with st.expander(
                    f"{issue['severity']} : {issue['problem']}"
                ):

                    st.write(f"**Reason:** {issue['reason']}")

                    st.write(f"**Solution:** {issue['solution']}")            
             
    with tabs[3]:

        quality = st.session_state.quality

        if quality is None:
            quality = get_quality_report(code)
            st.session_state.quality = quality

        st.markdown("## 📈 Code Quality Report")

        left, right = st.columns(2)

        with left:

            st.metric(
                "Quality Score",
                f"{quality['score']}/100"
            )
            
            st.progress(quality["score"] / 100)

            st.caption(f"{quality['score']}% Quality Score")

            st.metric(
                "Issues Found",
                quality["total_issues"]
            ) 
            
        with right:

            if quality["score"] >= 90:

                st.success("Excellent Code Quality")

            elif quality["score"] >= 70:

                st.warning("Good Code Quality")

            else:

                st.error("Needs Improvement")

            st.markdown("---")

        st.code(
            quality["flake8"],
            language="text"
        )
        
    with tabs[4]:
        
        st.markdown("## 🤖 AI Code Review")

        try:

            with st.spinner("Reviewing code with AI..."):

            
                if st.session_state.review is None:
                    st.session_state.review =  review_code(code)

                review = st.session_state.review

                st.markdown(review)
                
            st.download_button(
                "📥 Download AI Review",
                review,
                file_name="ai_review.txt"
            )

        except Exception :

            st.error("❌ Unable to generate AI review.")

            st.info(
                "Please check your internet connection or API key."
            )
            
            
    with tabs[5]:

        try:

            fixed_code = st.session_state.fixed_code

            if error is None:

                st.success("✅ No syntax errors detected.")

                if st.button(
                    "Improve Code with AI",
                    key="improve_code"
                ):

                    with st.spinner("🤖 Improving code..."):

                        fixed_code = fix_code(code)

                        st.session_state.fixed_code = fixed_code

            else:

                st.error("❌ Syntax errors detected.")

                if st.button(
                    "🤖 Fix Code with AI",
                    key="syntax_fix"
                ):

                    with st.spinner("🤖 Fixing syntax errors..."):

                        fixed_code = fix_code(code)

                        st.session_state.fixed_code = fixed_code

            # Get latest fixed code from session state
            fixed_code = st.session_state.fixed_code

            if fixed_code:

                st.success("✅ Code fixed successfully.")

                st.code(
                    fixed_code,
                    language="python"
                )

                st.download_button(
                    "⬇ Download Fixed Code",
                    fixed_code,
                    file_name="fixed_code.py"
                )

        except Exception as e:

            st.error("❌ Unable to fix the code.")

            st.exception(e)                   
    
    with tabs[6]:

        st.markdown("## 📄 Analysis Report")

        report = f"""
        
====================================================
              AI CODE REVIEW REPORT
====================================================

📊 CODE STATISTICS
----------------------------------------------------

Functions            : {len(functions)}
Classes              : {len(classes)}
Loops                : {len(loops)}
Imports              : {len(imports)}
Variables            : {len(variables)}

⚡ COMPLEXITY ANALYSIS
---------------------------------------------------- 

Estimated Complexity : {
    complexity["Estimated Time Complexity"]
    if "error" not in complexity
    else "Not Available"
}

🛡 SECURITY ANALYSIS
----------------------------------------------------

Status               : {"PASS" if not security_issues else "WARNING"}
Issues Found         : {len(security_issues)}

📈 QUALITY ANALYSIS
----------------------------------------------------

Quality Score        : {quality["score"]}/100
Quality Issues       : {quality["total_issues"]}

====================================================
Generated by AI Code Reviewer
====================================================
"""       
        st.code(
            report,
            language="text"
        )

        st.download_button(
            "⬇ Download Report",
            report,
           file_name="analysis_report.txt"
        )
                
# =====================================
# MAIN
# =====================================

def main():

    configure_page()

    load_css()

    # render_sidebar()

    render_hero()

    uploaded_file, code = render_input_section()

    render_analysis(uploaded_file, code)

if __name__ == "__main__":
    main()
    