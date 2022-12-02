import streamlit as st


# -------------------- 页眉 -------------------- #
# 页面设置
st.set_page_config(page_title="用户设置", page_icon="👤")
# 页面标题
header = st.header("👤 用户设置")
subheader = st.subheader("当前身份：游客🚶")
# 分割线
st.markdown("---")


# -------------------- 用户设置 -------------------- #
# 设置用户名
def setUsername():
    st.session_state.username = username_input


username = st.session_state.get("username")
if not username:
    username_input = st.text_input("您可以设置临时用户名【刷新网页后将不会保存】:", placeholder="请输入用户名", key="username_input")
    st.button(
        "确认用户名", key="save_user",
        on_click=setUsername
    )
    st.write("未设置用户名！")
else:
    username_input = st.text_input("您可以更改用户名【刷新网页后将不会保存】:", placeholder="请输入用户名", key="username_change")
    st.button(
        "确认更改", key="change_user",
        on_click=setUsername
    )
    st.write(f"欢迎🎉 {username}")
    subheader.subheader(f"欢迎🎉 {username}")