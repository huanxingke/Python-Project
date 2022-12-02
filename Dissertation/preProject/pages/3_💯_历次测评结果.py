import random as rnd
import string
import json
import time
import io

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
st.set_page_config(page_title="💯 历次测评结果", page_icon="💯")
if not st.session_state.get("analyse_config"):
    st.session_state.analyse_config = {}
# 页面标题
header = st.header("历次测评结果")
username = st.session_state.get("username")
if username:
    subheader = st.subheader(f"欢迎🎉 {username}")
# 分割线
st.markdown("---")


# -------------------- 评估开始 -------------------- #
# 获取题库
@st.cache
def getQuestions():
    tiku_url = "https://raw.githubusercontent.com/huanxingke/Python-Project/master/Dissertation/preProject/data/questions.json"
    questions = requests.get(url=tiku_url).json(strict=False)
    return questions


# 重置评估设置
def initAnalyseConfig():
    st.session_state.analyse_config["expanded_seed"] = None
    st.session_state.analyse_config["answers"] = dict()


# 删除单条记录
def deleteSingleHistory(seed_list=None, delete_selected=False):
    if delete_selected:
        seed_list = history_selected[:]
    for seed in seed_list:
        history_seed = [i["rnd_seed"] for i in st.session_state.history][:]
        if seed in history_seed:
            del st.session_state.history[history_seed.index(seed)]
    initAnalyseConfig()


# plt 转二进制流
def fig2BytesIO(fig):
    canvas = fig.canvas
    with io.BytesIO() as buffer:
        canvas.print_png(buffer)
        data = buffer.getvalue()
    return data


# 饼图数据格式
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return "{v:d}".format(v=val)
    return my_format


# 饼图
def plot_pie(projects, counts, title):
    fig = plt.figure(figsize=(4, 4))
    plt.pie(counts, labels=projects, autopct=autopct_format(counts), counterclock=False, startangle=90)
    plt.title(title)
    plt.tight_layout()
    data = fig2BytesIO(fig=fig)
    return data


# 批改试卷
def correctingTestPaper():
    # 设置随机种子
    rnd.seed(expanded_seed)
    # 检索答案序号
    answer_index = lambda x: list(string.ascii_uppercase).index(x.upper())
    # 各部分得分
    scores = [0, 0, 0]
    # 错题词云数据
    mistakes = ["", "", ""]
    # 评估并显示错题
    with exam_empty_placeholder.container():
        # 单选部分
        single_tip = st.markdown("*一、单项选择题（共40分）*")
        with st.expander("展开单选题详情"):
            single_choice_questions = rnd.sample(tiku["单选题"], 20)
            for single_choice_question_index, single_choice_question in enumerate(single_choice_questions):
                # 问题内容、答案、用户答案
                single_choice_question_content = single_choice_question["question_content"]
                single_choice_question_answer = single_choice_question["answer"][0]
                single_choice_question_user_answer = answers["单选题"][single_choice_question_index]
                st.radio(
                    "【第%s题】" % (single_choice_question_index + 1) + single_choice_question_content[0],
                    single_choice_question_content[1:],
                    index=answer_index(single_choice_question_user_answer),
                    horizontal=False, disabled=True
                )
                # 判断对错
                if single_choice_question_user_answer == single_choice_question_answer:
                    st.success("正确答案：{}".format(single_choice_question_user_answer))
                    scores[0] += 2
                else:
                    st.info("正确答案：{}".format(single_choice_question_answer))
                    st.error("您的答案：{}".format(single_choice_question_user_answer))
                    mistakes[0] += "".join(single_choice_question_content)
        # 不定项部分
        multiple_tip = st.markdown("*二、不定项选择题（共40分）*")
        with st.expander("展开多选题详情"):
            multi_choice_questions = rnd.sample(tiku["多选题"], 10)
            for multi_choice_question_index, multi_choice_question in enumerate(multi_choice_questions):
                # 问题内容、答案、用户答案
                multi_choice_question_content = multi_choice_question["question_content"]
                multi_choice_question_answer = "".join(sorted(multi_choice_question["answer"]))
                multi_choice_question_user_answer = "".join(sorted(answers["多选题"][multi_choice_question_index]))
                st.multiselect(
                    "【第%s题】" % (multi_choice_question_index + 1) + multi_choice_question_content[0],
                    multi_choice_question_content[1:],
                    default=multi_choice_question_content[1:],
                    disabled=True
                )
                # 判断对错
                if multi_choice_question_user_answer == multi_choice_question_answer:
                    st.success("正确答案：{}".format(multi_choice_question_user_answer))
                    scores[1] += 4
                else:
                    st.info("正确答案：{}".format(multi_choice_question_answer))
                    st.error("您的答案：{}".format(multi_choice_question_user_answer))
                    mistakes[1] += "".join(multi_choice_question_content)
        # 判断题部分
        judgmental_tip = st.markdown("*三、判断题（共20分）*")
        with st.expander("展开判断题详情"):
            judgmental_questions = rnd.sample(tiku["判断题"], 10)
            for judgmental_question_index, judgmental_question in enumerate(judgmental_questions):
                # 问题内容、答案、用户答案
                judgmental_question_content = judgmental_question["question_content"]
                judgmental_question_answer = judgmental_question["answer"][0]
                judgmental_question_user_answer = answers["判断题"][judgmental_question_index]
                st.radio(
                    "【第%s题】" % (judgmental_question_index + 1) + judgmental_question_content[0],
                    ["对", "错"],
                    index=["对", "错"].index(judgmental_question_user_answer),
                    horizontal=False, disabled=True
                )
                # 判断对错
                if judgmental_question_user_answer == judgmental_question_answer:
                    st.success("正确答案：{}".format(judgmental_question_user_answer))
                    scores[2] += 2
                else:
                    st.info("正确答案：{}".format(judgmental_question_answer))
                    st.error("您的答案：{}".format(judgmental_question_user_answer))
                    mistakes[2] += "".join(judgmental_question_content)
        # 更改提示
        single_tip.markdown("*一、单项选择题（得分：{}/40）*".format(scores[0]))
        multiple_tip.markdown("*二、不定项选择题（得分：{}/40）*".format(scores[1]))
        judgmental_tip.markdown("*三、判断题（得分：{}/20）*".format(scores[2]))
        # 失分情况
        lost_scores = np.array([40, 40, 20]) - np.array(scores)
        projects = ["单选题", "多选题", "判断题"]
        # 答对率 %
        correct_rate = sum(np.array(scores) / [20, 10, 10]) / 40 * 100
        # 失分最多的题型
        most_lost_projects = projects[list(lost_scores).index(int(max(lost_scores)))]
        # 开始生成图表
        # 得分饼图
        score_fig_data = plot_pie(
            projects=["Single", "Multiple", "Judgmental"],
            counts=lost_scores,
            title="Score Loss of Each Question Type\n[Total score: %s points]" % sum(scores)
        )
        # 绘制
        st.image(score_fig_data, width=390)
        # 文字评估
        st.markdown("#### 本次考试答对率为: {:.2f} %".format(correct_rate))
        st.markdown("#### 失分最多的题型为: {}".format(most_lost_projects))
        if sum(scores) >= 90:
            st.markdown("### 总评：化工安全安全意识非常高！")
        elif sum(scores) >= 60:
            st.markdown("### 总评：成绩不错！再接再厉！")
        elif sum(scores) < 60:
            st.markdown("### 总评：化工安全意识有待提高呀！")
        # 重置设置
        initAnalyseConfig()


# 设置需要展开的试卷
def setExpanded(seed, answer):
    st.session_state.analyse_config["expanded_seed"] = seed
    st.session_state.analyse_config["answers"] = answer


# 获取做题历史
history = st.session_state.get("history")
if not history:
    st.markdown("### 您还没有考试记录哦！")
else:
    # 加载题库
    with st.spinner("正在加载题库..."):
        tiku = getQuestions()
    # 选中的历史记录
    history_selected = []
    # 表头
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("#### 题库随机数")
    with col2:
        st.markdown("#### 分数")
    with col3:
        st.markdown("#### 详情")
    with col4:
        st.markdown("#### 删除")
    with col5:
        st.button(
            "删除选中", key="delete_selected",
            on_click=deleteSingleHistory, kwargs={"delete_selected": True}
        )
    # 遍历
    for single_history in history:
        history_rnd_seed = single_history["rnd_seed"]
        history_user_answer = single_history["user_answer"]
        history_scores = single_history["scores"]
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(history_rnd_seed)
        with col2:
            st.text(history_scores)
        with col3:
            st.button(
                "展开详情", key="expanded_%s" % history_rnd_seed,
                on_click=setExpanded, kwargs={
                    "seed": history_rnd_seed,
                    "answer": history_user_answer
                }
            )
        with col4:
            st.button(
                "删除", key="delete_%s" % history_rnd_seed,
                on_click=deleteSingleHistory, kwargs={
                    "seed_list": [history_rnd_seed]
                }
            )
        with col5:
            selected = st.checkbox("选中", key="select_%s" % history_rnd_seed)
            if selected:
                history_selected.append(history_rnd_seed)
    # 获取评估设置
    expanded_seed = st.session_state.analyse_config.get("expanded_seed")
    answers = st.session_state.analyse_config.get("answers")
    # 显示评估结果
    if expanded_seed:
        # 重置评估设置按钮
        st.button("关闭详情", key="collapsed_details", on_click=initAnalyseConfig)
        # 题库随机数显示
        st.write("【题库随机数：%s】" % expanded_seed)
        # 初始化容器
        exam_empty_placeholder = st.empty()
        correctingTestPaper()