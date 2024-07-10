import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from streamlit_option_menu import option_menu

from app.portfolio import portfolio_page
from app.home import home_page
from app.browse import browse_page
from app.monitoring import monitoring_page


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "display_recommendations" not in st.session_state:
    st.session_state.display_recommendations = False

if "display_recommendation_details" not in st.session_state:
    st.session_state.display_recommendation_details = False


# Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigate",
        options=["Home", "Portfolio", "Browse", "Monitoring"],
    )

    if selected == "Home":
        st.session_state.page = "Home"
    elif selected == "Portfolio":
        st.session_state.page = "Portfolio"
    elif selected == "Browse":
        st.session_state.page = "Browse"
    elif selected == "Monitoring":
        st.session_state.page = "Monitoring"
         
if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Portfolio":
    portfolio_page()
elif st.session_state.page == "Browse":
    browse_page() 
elif st.session_state.page == "Monitoring":
    monitoring_page()   
