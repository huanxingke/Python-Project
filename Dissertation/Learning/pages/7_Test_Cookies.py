from StreamlitCookies import StreamlitCookies
import streamlit as st


with st.form("cookie_manager"):
    name_input = st.text_input("Cookie Name:", key="name_input")
    value_input = st.text_input("Cookie Value:", key="value_input")
    act_input = st.text_input("Action:", key="act_input")
    if st.form_submit_button("Start"):
        cookie_response = StreamlitCookies(name=name_input, value=value_input, act=act_input)
        st.session_state.CookieManager = cookie_response

if st.session_state.get("CookieManager"):
    st.write(st.session_state.CookieManager)
    del st.session_state.CookieManager

cookie_response = StreamlitCookies(name="name", value="Streamlit", act="add")
cookie_response