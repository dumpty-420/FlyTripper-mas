"""
✈️  FlyTripper — Streamlit UI for the multi-agent travel planner.

Run with:  uv run streamlit run streamlit_app.py
"""

import streamlit as st

from app.orchestrator import TravelOrchestrator

# ────────────────────────────── Page config ──────────────────────────
st.set_page_config(page_title="FlyTripper", page_icon="✈️", layout="centered")

st.title("✈️ FlyTripper")
st.caption("Plan your next adventure with a multi-agent AI pipeline 🚀")

# ────────────────────────────── Session state ────────────────────────
if "itinerary" not in st.session_state:
    st.session_state.itinerary = None
if "ics_bytes" not in st.session_state:
    st.session_state.ics_bytes = None

# ────────────────────────────── User inputs ──────────────────────────
destination = st.text_input("🌍 Where do you want to go?", placeholder="e.g. Tokyo")
num_days = st.number_input(
    "📅 How many days?", min_value=1, max_value=30, value=7
)
preferences = st.text_area(
    "💡 Preferences (optional)",
    placeholder="e.g. prefer museums over nightlife, budget-friendly",
)

# ────────────────────────────── Generate ─────────────────────────────
if st.button("🚀 Generate Itinerary", type="primary"):
    if not destination:
        st.warning("Please enter a destination.")
    else:
        # Status container to show pipeline progress
        status = st.status("Planning your trip with multi-agent AI…", expanded=True)

        def on_stage(stage_name: str) -> None:
            status.update(label=stage_name)

        orchestrator = TravelOrchestrator(on_stage=on_stage)
        result = orchestrator.run(
            destination=destination,
            num_days=num_days,
            preferences=preferences,
        )

        status.update(label="✅ Itinerary ready!", state="complete")

        st.session_state.itinerary = result.itinerary
        st.session_state.ics_bytes = result.ics_bytes

# ────────────────────────────── Display ──────────────────────────────
if st.session_state.itinerary:
    st.divider()
    st.subheader("Your Itinerary")
    st.markdown(st.session_state.itinerary)

    st.download_button(
        label="📅 Download Itinerary (.ics)",
        data=st.session_state.ics_bytes,
        file_name="travel_itinerary.ics",
        mime="text/calendar",
    )
