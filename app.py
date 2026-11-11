from src.risk_engine import assess_risk 
from src.explanation_engine import generate_explanation
import streamlit as st

# ==================================
# 1. Page Configuration
# ==================================

st.set_page_config(
    page_title="BeiV | Explainable Scam Detection",
    page_icon="🛡️",
    layout="wide"
)

# ==================================
# 2. Sidebar
# ==================================

with st.sidebar:
    st.title("🛡️ BeiV")
    st.caption("Scams evolve. Stay one step ahead.")
    st.caption("Multilingual Scam Detection")
    st.divider()
    language = st.selectbox(
        "Output Language",
        ["繁體中文", "English"]
    )
    st.divider()
    st.subheader("About")
    st.write(
        "BeiV helps users identify potential scam messages "
        "through text and URL analysis."
    )

# ==================================
# 3. Main Header
# ==================================

st.title("🛡️ BeiV")
st.write("**Scams evolve. Stay one step ahead.**")
st.write(
    "Analyze suspicious messages and "
    "identify potential scam indicators."
)
st.divider()

# ==================================
# 4. Input Area
# ==================================

st.subheader("Message Analysis")
message = st.text_area(
    "Enter a suspicious message",
    placeholder="Paste your suspicious message here...",
    height=180
)

analyze_button = st.button(
    "🔍 Analyze Message",
    type="primary",
    use_container_width=True
)


# ==================================
# 5. Analysis Trigger
# ==================================

if analyze_button:
    if not message.strip():
        st.warning("Please enter a message first.")
    else:
        try:
            # Temporary integration:
            # Upstream analysis modules are not ready yet.
            assessment = assess_risk(
                classifier_result=None,
                url_evidence=None,
                rule_evidence=None
            )

            # Explanation engine currently supports English only.
            explanation = generate_explanation(
                assessment,
                language="en"
            )

            st.session_state["assessment"] = assessment
            st.session_state["explanation"] = explanation
            st.session_state["submitted_message"] = message

        except Exception as error:
            st.error(f"Analysis error: {error}")


# ==================================
# 6. Result Area
# ==================================

st.divider()
st.subheader("Analysis Result")

if "explanation" in st.session_state:

    assessment = st.session_state["assessment"]
    explanation = st.session_state["explanation"]

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.caption("Risk Level")
            st.markdown(
                f"### {explanation['risk_level'].replace('_', ' ').title()}"
            )

    with col2:
        with st.container(border=True):
            st.caption("Analysis Status")
            st.markdown(
                f"### {assessment['analysis_status'].replace('_', ' ').title()}"
            )

    st.warning(
        "This is a temporary integration test. "
        "Actual message detection is not connected yet."
    )

    # ==================================
    # 7. Evidence and Recommendations
    # ==================================

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.subheader("🔎 Evidence")

            if explanation["explanations"]:
                for item in explanation["explanations"]:
                    st.write(item["reason"])
                    st.caption(f"Evidence: {item['evidence']}")
            else:
                st.write("No evidence has been provided yet.")

    with col4:
        with st.container(border=True):
            st.subheader("🛡️ Safety Recommendations")

            for action in explanation["recommended_actions"]:
                st.write(f"- {action}")

    # ==================================
    # 8. Uncertainty and Disclaimer
    # ==================================

    st.subheader("Analysis Limitations")

    for item in explanation["uncertainty"]:
        st.write(f"- {item}")

    st.caption(explanation["disclaimer"])

else:
    st.info("Enter a message and click Analyze Message to begin.")
