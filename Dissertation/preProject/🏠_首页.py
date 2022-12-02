import streamlit as st


# -------------------- 页眉 -------------------- #
# 页面设置
st.set_page_config(page_title="首页", page_icon="🏠")
# 页面标题
header = st.header("🏠 首页")
username = st.session_state.user_config.get("username") if st.session_state.get("user_config") else None
if username:
    subheader = st.subheader(f"欢迎🎉 {username}")
# 分割线
st.markdown("---")


# -------------------- 页眉 -------------------- #
st.markdown("""
### 关于本程序
- 学校：华南理工大学
- 学院：化学与化工学院
- 年级：2019级
- 专业：能源化学工程
- 毕设：化工类企业环境事故应急预案演练计算机模拟仿真系统开发（含知识考试和过程仿真）
- 姓名：李文韬
    - Github：https://github.com/huanxingke
    - 联系方式：201930191473@mail.scut.edu.cn
- 导师：方利国
    - Github：https://github.com/gzlgfang
    - 联系方式：lgfang@scut.edu.cn
""")