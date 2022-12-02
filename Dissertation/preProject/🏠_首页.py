import streamlit as st


# -------------------- 页眉 -------------------- #
# 页面设置
st.set_page_config(page_title="首页", page_icon="🏠")
if not st.session_state.get("user_config"):
    st.session_state.user_config = {}
# 页面标题
header = st.header("首页")
subheader = st.subheader("当前身份：游客🚶")
# 分割线
st.markdown("---")


# -------------------- 用户设置 -------------------- #
# 设置用户名
def setUsername():
    st.session_state.user_config["username"] = username_input


username = st.session_state.user_config.get("username")
if not username:
    username_input = st.text_input("请设置临时用户名以保存做题记录:", placeholder="请输入用户名", key="username_input")
    st.button(
        "确认用户名", key="save_user",
        on_click=setUsername
    )
    st.write("未设置用户名！")
else:
    username_input = st.text_input("您可以更改用户名:", placeholder="请输入用户名", key="username_change")
    st.button(
        "确认更改", key="change_user",
        on_click=setUsername
    )
    st.write(f"欢迎🎉 {username}")
    subheader.subheader(f"欢迎🎉 {username}")