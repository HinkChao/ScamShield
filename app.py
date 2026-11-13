import streamlit as st

from src.risk_engine import assess_risk
from src.explanation_engine import generate_explanation
from src.url_analyzer import analyze_urls


# ==================================
# 1. Page Configuration
# ==================================

st.set_page_config(
    page_title="BeiV | Explainable Scam Detection",
    page_icon="BeiVLogo.png",
    layout="wide"
)


# ==================================
# 2. Sidebar
# ==================================

with st.sidebar:
    logo_col, title_col = st.columns([1, 3])

    with logo_col:
        st.image("BeiVLogo.png", width=55)

    with title_col:
        st.title("BeiV")

    st.caption("Scams evolve. Stay one step ahead.")
    st.caption("Multilingual Scam Detection")
    st.divider()

    language = st.selectbox(
        "Output Language",
        ["繁體中文", "English"]
    )

    if language == "繁體中文":
        st.info(
            "Traditional Chinese output is not implemented yet. "
            "Analysis explanations are currently in English."
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

logo_col, title_col = st.columns([1, 8])

with logo_col:
    st.image("BeiVLogo.png", width=75)

with title_col:
    st.title("BeiV")

st.write("**Scams evolve. Stay one step ahead.**")
st.write("Analyze suspicious messages and identify potential scam indicators.")
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

    # Clear previous results to prevent stale data.
    for key in [
        "submitted_message",
        "url_results",
        "assessment",
        "explanation"
    ]:
        st.session_state.pop(key, None)

    if not message.strip():
        st.warning("Please enter a message first.")

    else:
        try:
            # Step 1: Analyze URLs in the message.
            url_results = analyze_urls(message)

            # Step 2: Assess overall risk.
            # ML and rule analysis are not connected yet.
            assessment = assess_risk(
                classifier_result=None,
                url_evidence=url_results,
                rule_evidence=None
            )

            # Step 3: Generate explanation.
            explanation = generate_explanation(
                assessment,
                language="en"
            )

            # Step 4: Save results.
            st.session_state["submitted_message"] = message
            st.session_state["url_results"] = url_results
            st.session_state["assessment"] = assessment
            st.session_state["explanation"] = explanation

        except (TypeError, ValueError) as error:
            st.error(f"Analysis error: {error}")


# ==================================
# 6. Result Area
# ==================================

st.divider()
st.subheader("Analysis Result")

if "explanation" in st.session_state:

    assessment = st.session_state["assessment"]
    explanation = st.session_state["explanation"]

    # Show the exact message that was analyzed.
    st.markdown("**Analyzed Message**")
    st.text(st.session_state["submitted_message"])

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
        "URL structural analysis is connected. "
        "ML classification and message-rule analysis "
        "are not connected yet."
    )

    # ==================================
    # 7. Evidence and Recommendations
    # ==================================

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.subheader("🔎 Evidence")

            # Display explanation findings.
            if explanation["explanations"]:
                for item in explanation["explanations"]:
                    st.write(item["reason"])
                    st.caption(f"Evidence: {item['evidence']}")
            else:
                st.write("No warning indicators found.")

            # Display URL analysis results.
            st.divider()
            st.markdown("**URL Analysis**")

            url_results = st.session_state.get("url_results", [])

            if not url_results:
                st.write("No supported URLs found in the message.")

            else:
                for index, result in enumerate(url_results, start=1):
                    with st.expander(f"URL {index}: {result['url']}"):

                        st.write(f"Status: {result['status']}")

                        if result.get("hostname"):
                            st.write(f"Hostname: {result['hostname']}")

                        if result["status"] == "invalid":
                            st.warning(
                                f"URL could not be analyzed: "
                                f"{result.get('reason', 'unknown')}"
                            )

                        else:
                            indicators = result.get("indicators", [])

                            if indicators:
                                for indicator in indicators:
                                    st.write(
                                        f"- {indicator['type']} "
                                        f"({indicator['severity']})"
                                    )
                                    st.caption(indicator["evidence"])
                            else:
                                st.write(
                                    "No structural warning indicators found."
                                )

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
