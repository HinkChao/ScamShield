
import streamlit as st

# ==================================
# 1. Page Configuration
# ==================================

st.set_page_config(
    page_title="ScamShield AI",
    page_icon="🛡️",
    layout="wide"
)

# ==================================
# 2. Sidebar
# ==================================

with st.sidebar:
    st.title("🛡️ ScamShield AI")

    st.caption("Multilingual Scam Detection")

    st.divider()

    language = st.selectbox(
        "Output Language",
        ["繁體中文", "English"]
    )

    st.divider()

    st.subheader("About")

    st.write(
        "ScamShield AI helps users identify "
        "potential scam messages through "
        "text and URL analysis."
    )

# ==================================
# 3. Main Header
# ==================================

st.title("ScamShield AI")

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

        st.session_state["submitted_message"] = message

        st.info(
            "Message received. "
            "The analysis backend has not been connected yet."
        )

# ==================================
# 6. Result Area
# ==================================

st.divider()

st.subheader("Analysis Result")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.caption("Risk Level")
        st.markdown("### Not analyzed")

with col2:
    with st.container(border=True):
        st.caption("Analysis Status")
        st.markdown("### Pending")

# ==================================
# 7. Evidence and Recommendations
# ==================================

col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):

        st.subheader("🔎 Evidence")

        st.write(
            "Detected indicators and supporting "
            "evidence will appear here."
        )

with col4:
    with st.container(border=True):

        st.subheader("🛡️ Safety Recommendations")

        st.write(
            "Safety recommendations will appear here."
        )

# ==================================
# 8. Disclaimer
# ==================================

st.divider()

st.caption(
    "Disclaimer: ScamShield AI provides "
    "risk indicators, not a guarantee that "
    "a message is safe or fraudulent."
)
