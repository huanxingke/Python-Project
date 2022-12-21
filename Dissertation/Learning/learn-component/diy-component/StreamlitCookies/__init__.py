import os

import streamlit.components.v1 as components
import streamlit as st


_RELEASE = True

if not _RELEASE:
    cookie_func = components.declare_component(
        "my_component",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    cookie_func = components.declare_component("StreamlitCookies", path=build_dir)


def StreamlitCookies(name=None, act=None, value=None, key=None):
    response = cookie_func(name=name, value=value, act=act, key=key)
    return response


st.write(StreamlitCookies(name="name"))