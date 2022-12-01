import json
import time

import matplotlib.pyplot as plt
import matplotlib as mpl
import streamlit as st
import random as rnd
import numpy as np
import requests


# 使 matplotlib 支持中文
mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False


# -------------------- 页眉 -------------------- #
# 页面设置
st.set_page_config(page_title="化工安全考试", page_icon="📃")
# 页面标题
header = st.header("化工安全考试（当前身份🚶 游客）")
# 分割线
st.markdown("---")


# -------------------- 用户登录侧边栏 -------------------- #
# 设置用户名
def setUsername():
    st.session_state.username = username_input


username = st.session_state.get("username")
if not username:
    username_input = st.sidebar.text_input("请设置临时用户名以保存做题记录:", placeholder="请输入用户名", key="username_input")
    st.sidebar.button(
        "确认用户名", key="save_user",
        on_click=setUsername
    )
    st.sidebar.write("未设置用户名！")
else:
    username_input = st.sidebar.text_input("您可以更改用户名:", placeholder="请输入用户名", key="username_change")
    st.sidebar.button(
        "确认更改", key="change_user",
        on_click=setUsername
    )
    st.sidebar.write(f"欢迎🎉 {username}")
    header.header(f"化工安全考试（欢迎🎉 {username}）")


# -------------------- 试卷开始 -------------------- #
# 获取题库
@st.cache
def getQuestions():
    url = "https://raw.githubusercontent.com/huanxingke/Python-Project/master/Dissertation/Learning/pages/data/questions.json"
    questions = requests.get(url=url).json()
    return questions


with st.spinner("正在加载题库..."):
    tiku = getQuestions()

st.markdown("> 【考试说明】本试卷共有40道题目，其中：单选题20×2分/题，不定项10×4分/题，判断题10×2分/题，共计100分。")
if st.button("开始组卷", key="make_a_test_paper"):
    st.markdown("*一、单项选择题（共40分）*")
    user_answers = {
        "单选题": [],
        "多选题": [],
        "判断题": []
    }
    single_choice_questions = rnd.sample(tiku["单选题"], 20)
    for single_choice_question_index, single_choice_question in enumerate(single_choice_questions):
        single_choice_question_content = single_choice_question["question_content"]
        single_choice_question_select = st.radio(
            "【第%s题】" % (single_choice_question_index + 1) + single_choice_question_content[0],
            single_choice_question_content[1:],
            vertical=True
        )
        user_answers["单选题"].append(single_choice_question_select)
    st.markdown("*二、不定项选择题（共40分）*")
    st.markdown("*三、判断题（共20分）*")


