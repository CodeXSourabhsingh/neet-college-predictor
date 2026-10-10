import streamlit as st
import pandas as pd
from Predictor import score_to_air, bucket_colleges
from sheets import save_lead, phone_exists, send_event

st.set_page_config(page_title="NEET College Predictor", layout="centered")

st.title("NEET College Predictor")
st.write("Enter your score to see which government MBBS colleges you can likely get.")

if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "buckets" not in st.session_state:
    st.session_state.buckets = None

if "utm_source" not in st.session_state:
    st.session_state.utm_source = st.query_params.get("utm_source", "")
    st.session_state.utm_medium = st.query_params.get("utm_medium", "")
    st.session_state.utm_campaign = st.query_params.get("utm_campaign", "")

if "device" not in st.session_state:
    st.session_state.device = "mobile_unknown"

score = st.slider("Your NEET score", 0, 720, 500)

category = st.selectbox(
    "Category",
    ["General", "EWS", "OBC", "SC", "ST"]
)

state = st.selectbox(
    "Home state",
    [
        "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Delhi",
        "Gujarat", "Haryana", "Himachal Pradesh", "Jammu & Kashmir",
        "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
        "Maharashtra", "Odisha", "Puducherry", "Punjab", "Rajasthan",
        "Tamil Nadu", "Telangana", "Uttar Pradesh", "Uttarakhand",
        "West Bengal", "Other"
    ]
)

air = score_to_air(score)
st.info(f"Your estimated All India Rank: **{air:,}**")

if "page_view_fired" not in st.session_state:
    send_event("page_view",
               utm_source=st.session_state.utm_source,
               device=st.session_state.device)
    st.session_state.page_view_fired = True

st.subheader("Unlock your college list")

with st.form("lead_form"):
    name = st.text_input("Name")
    phone = st.text_input("10-digit mobile number", max_chars=10)
    consent = st.checkbox(
        "We'll use this number to share your result and NEET counselling updates."
    )
    submitted = st.form_submit_button("Show my colleges")


if submitted:
    if name and "form_start_fired" not in st.session_state:
        send_event("form_start", utm_source=st.session_state.utm_source)
        st.session_state.form_start_fired = True

    if not name.strip():
        st.error("Please enter your name.")
    elif not (phone.isdigit() and len(phone) == 10):
        st.error("Please enter a valid 10-digit mobile number.")
    elif not consent:
        st.error("Please accept the consent note to continue.")
    else:
        send_event("form_submit",
                   score=score, category=category, state=state,
                   utm_source=st.session_state.utm_source)

        if phone_exists(phone):
            st.warning("This phone number is already in our list. Showing your results anyway.")
        else:
            save_lead(
                name, phone, score, category, state, air,
                st.session_state.utm_source,
                st.session_state.utm_medium,
                st.session_state.utm_campaign,
            )

        safe, moderate, reach = bucket_colleges(air, category, state)
        st.session_state.buckets = (safe, moderate, reach)
        st.session_state.submitted = True

if st.session_state.submitted and st.session_state.buckets:

    safe, moderate, reach = st.session_state.buckets

    send_event("result_view",
               safe_count=len(safe),
               moderate_count=len(moderate),
               reach_count=len(reach),
               utm_source=st.session_state.utm_source)

    st.divider()
    st.subheader("Colleges you can likely get")

    if not safe and not moderate and not reach:
        st.warning(
            "No colleges match your score in this category. "
            "Consider state-quota counselling — it often has lower cutoffs."
        )
    else:
        st.markdown("### 🟢 Safe")
        if safe:
            for c in safe:
                badge = " ⭐ Home state" if c["home_state_badge"] else ""
                st.write(f"**{c['college']}** — {c['city']} (closing AIR {c['closing_rank']}){badge}")
        else:
            st.caption("No colleges in this bucket.")

        st.markdown("### 🟡 Moderate")
        if moderate:
            for c in moderate:
                badge = " ⭐ Home state" if c["home_state_badge"] else ""
                st.write(f"**{c['college']}** — {c['city']} (closing AIR {c['closing_rank']}){badge}")
        else:
            st.caption("No colleges in this bucket.")

        st.markdown("### 🔴 Reach")
        if reach:
            for c in reach:
                badge = " ⭐ Home state" if c["home_state_badge"] else ""
                st.write(f"**{c['college']}** — {c['city']} (closing AIR {c['closing_rank']}){badge}")
        else:
            st.caption("No colleges in this bucket.")

    share_text = (
        f"I scored {score} in NEET ({category}, {state}). "
        f"Estimated AIR: {air}. "
        f"Check which colleges you can get:"
    )
    share_url = f"https://wa.me/?text={share_text}"
    st.markdown(
        f'<a href="{share_url}" target="_blank">'
        f'<button style="background-color:#25D366;color:white;padding:10px 20px;'
        f'border:none;border-radius:6px;cursor:pointer;font-size:15px;margin-top:10px;">'
        f'Share on WhatsApp</button></a>',
        unsafe_allow_html=True
    )

    st.caption(
        "The closing ranks shown are indicative estimates based on 2025 trends. "
        "Not official MCC data. Verify with official counselling sources before making decisions."
    )