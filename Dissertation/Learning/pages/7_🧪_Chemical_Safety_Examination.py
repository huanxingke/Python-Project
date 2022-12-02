import random as rnd
import json
import time

import matplotlib.pyplot as plt
import matplotlib as mpl
import streamlit as st
import numpy as np
import requests


# 使 matplotlib 支持中文
mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False


# -------------------- 页眉 -------------------- #
# 页面设置
st.set_page_config(page_title="化工安全考试", page_icon="📃")
if not st.session_state.get("exam_config"):
    st.session_state.exam_config = {}
# 页面标题
header = st.header("化工安全考试（当前身份🚶 游客）")
# 分割线
st.markdown("---")


# -------------------- 用户登录侧边栏 -------------------- #
# 设置用户名
def setUsername():
    st.session_state.exam_config["username"] = username_input


username = st.session_state.exam_config.get("username")
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
    tiku_url = "https://raw.githubusercontent.com/huanxingke/Python-Project/master/Dissertation/Learning/pages/data/questions.json"
    questions = requests.get(url=tiku_url).json()
    return questions


# 重置试卷设置
def initConfig():
    st.session_state.exam_config["rnd_seed"] = time.time()
    st.session_state.exam_config["finished"] = False
    st.session_state.exam_config["answers"] = dict()


# 组卷
def makeATestPaper():
    with exam_empty_placeholder.container():
        with st.form("exam_paper"):
            user_answers = {
                "单选题": [],
                "多选题": [],
                "判断题": []
            }
            # 单选部分
            st.markdown("*一、单项选择题（共40分）*")
            single_choice_questions = rnd.sample(tiku["单选题"], 20)
            for single_choice_question_index, single_choice_question in enumerate(single_choice_questions):
                single_choice_question_content = single_choice_question["question_content"]
                single_choice_question_select = st.radio(
                    "【第%s题】" % (single_choice_question_index + 1) + single_choice_question_content[0],
                    single_choice_question_content[1:],
                    horizontal=False
                )
                user_answers["单选题"].append(single_choice_question_select[0])
            # 不定项部分
            st.markdown("*二、不定项选择题（共40分）*")
            multi_choice_questions = rnd.sample(tiku["多选题"], 10)
            for multi_choice_question_index, multi_choice_question in enumerate(multi_choice_questions):
                multi_choice_question_content = multi_choice_question["question_content"]
                multi_choice_question_select = st.multiselect(
                    "【第%s题】" % (multi_choice_question_index + 1) + multi_choice_question_content[0],
                    multi_choice_question_content[1:]
                )
                user_answers["多选题"].append([i[0] for i in sorted(multi_choice_question_select, key=lambda x: x[0])])
            # 判断题部分
            st.markdown("*三、判断题（共20分）*")
            judgmental_questions = rnd.sample(tiku["判断题"], 10)
            for judgmental_question_index, judgmental_question in enumerate(judgmental_questions):
                judgmental_question_content = judgmental_question["question_content"]
                judgmental_question_select = st.radio(
                    "【第%s题】" % (judgmental_question_index + 1) + judgmental_question_content[0],
                    ["对", "错"],
                    horizontal=False
                )
                user_answers["判断题"].append(judgmental_question_select)
            # 提交按钮
            submitted = st.form_submit_button("点击提交")
            # 提交后自动批改
            if submitted:
                st.session_state.exam_config["finished"] = True
                st.session_state.exam_config["answers"] = user_answers
                exam_empty_placeholder.empty()
                correctingTestPaper()


# 批改试卷
def correctingTestPaper():
    with exam_empty_placeholder.container():
        # 获取已做的答案
        answers = st.session_state.exam_config.get("answers")
        # 单选部分
        st.markdown("*一、单项选择题（共40分）*")
        single_choice_questions = rnd.sample(tiku["单选题"], 20)
        for single_choice_question_index, single_choice_question in enumerate(single_choice_questions):
            single_choice_question_content = single_choice_question["question_content"]
            st.radio(
                "【第%s题】" % (single_choice_question_index + 1) + single_choice_question_content[0],
                single_choice_question_content[1:],
                horizontal=False, disabled=True
            )
        # 不定项部分
        st.markdown("*二、不定项选择题（共40分）*")
        multi_choice_questions = rnd.sample(tiku["多选题"], 10)
        for multi_choice_question_index, multi_choice_question in enumerate(multi_choice_questions):
            multi_choice_question_content = multi_choice_question["question_content"]
            st.multiselect(
                "【第%s题】" % (multi_choice_question_index + 1) + multi_choice_question_content[0],
                multi_choice_question_content[1:], disabled=True
            )
        # 判断题部分
        st.markdown("*三、判断题（共20分）*")
        judgmental_questions = rnd.sample(tiku["判断题"], 10)
        for judgmental_question_index, judgmental_question in enumerate(judgmental_questions):
            judgmental_question_content = judgmental_question["question_content"]
            st.radio(
                "【第%s题】" % (judgmental_question_index + 1) + judgmental_question_content[0],
                ["对", "错"],
                horizontal=False, disabled=True
            )
        # 批改完后重置完成状态
        st.session_state.exam_config["finished"] = False
        st.session_state.exam_config["answers"] = dict()
        # 重做本卷按钮
        re_do_exam = st.button("重做本卷", key="re_do_exam")
        # 提交后自动批改
        if re_do_exam:
            exam_empty_placeholder.empty()


# 加载题库
with st.spinner("正在加载题库..."):
    tiku = getQuestions()
st.write(tiku)
st.markdown("> 【考试说明】本试卷共有40道题目，其中：单选题20×2分/题，不定项10×4分/题，判断题10×2分/题，共计100分。")
# 重置试卷设置按钮
st.button("重新组卷", key="make_a_test_paper", on_click=initConfig)
# 获取试卷设置
rnd_seed = st.session_state.exam_config.get("rnd_seed")
finished = st.session_state.exam_config.get("finished")
# 设置组卷随机值
if rnd_seed:
    rnd.seed(rnd_seed)
else:
    # 未设置则先设置
    initConfig()
# 如果是新组的卷子或者已经查看过答案的卷子
# 则进行组卷
# 初始化容器
exam_empty_placeholder = st.empty()
if not finished:
    makeATestPaper()
else:
    correctingTestPaper()
