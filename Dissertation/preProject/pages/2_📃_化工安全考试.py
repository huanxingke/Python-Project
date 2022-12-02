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
st.set_page_config(page_title="化工安全考试", page_icon="📃")
if not st.session_state.get("exam_config"):
    st.session_state.exam_config = {}
# 页面标题
header = st.header("📃 化工安全考试")
username = st.session_state.get("username")
if username:
    subheader = st.subheader(f"欢迎🎉 {username}")
# 分割线
st.markdown("---")


# -------------------- 试卷开始 -------------------- #
# 获取题库
@st.cache
def getQuestions():
    tiku_url = "https://raw.githubusercontent.com/huanxingke/Python-Project/master/Dissertation/preProject/data/questions.json"
    questions = requests.get(url=tiku_url).json(strict=False)
    return questions


# 重置试卷设置
def initExamConfig():
    st.session_state.exam_config["rnd_seed"] = int(time.time())
    st.session_state.exam_config["finished"] = False
    st.session_state.exam_config["answers"] = dict()


# 组卷
def makeATestPaper():
    # 设置随机种子
    rnd.seed(rnd_seed)
    with exam_empty_placeholder.container():
        with st.form("exam_paper"):
            user_answers = {
                "单选题": [],
                "多选题": [],
                "判断题": []
            }
            # 单选部分
            st.markdown("*一、单项选择题（共40分）*")
            with st.expander("展开单选题"):
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
            with st.expander("展开多选题"):
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
            with st.expander("展开判断题"):
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
    rnd.seed(rnd_seed)
    # 获取已做的答案
    answers = st.session_state.exam_config.get("answers")
    # 检索答案序号
    answer_index = lambda x: list(string.ascii_uppercase).index(x.upper())
    # 各部分得分
    scores = [0, 0, 0]
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
        # 保存本次做题结果
        if not st.session_state.get("history"):
            st.session_state.history = []
        history_rnd_seed = [i["rnd_seed"] for i in st.session_state.history]
        if rnd_seed not in history_rnd_seed:
            st.session_state.history.append({
                "rnd_seed": rnd_seed,
                "user_answer": answers,
                "scores": sum(scores)
            })
        else:
            # 或者更新
            st.session_state.history[history_rnd_seed.index(rnd_seed)] = {
                "rnd_seed": rnd_seed,
                "user_answer": answers,
                "scores": sum(scores)
            }
        # 批改完后重置完成状态
        st.session_state.exam_config["finished"] = False
        st.session_state.exam_config["answers"] = dict()
        # 重做本卷按钮
        re_do_exam = st.button("重做本卷", key="re_do_exam")
        if re_do_exam:
            exam_empty_placeholder.empty()


# 加载题库
with st.spinner("正在加载题库..."):
    tiku = getQuestions()
st.markdown("> 【考试说明】本试卷共有40道题目，其中：单选题20×2分/题，不定项10×4分/题，判断题10×2分/题，共计100分。")
# 获取试卷设置
rnd_seed = st.session_state.exam_config.get("rnd_seed")
finished = st.session_state.exam_config.get("finished")
# 设置组卷随机值
if not rnd_seed:
    initExamConfig()
# 重置试卷设置按钮
st.button("重新组卷", key="make_a_test_paper", on_click=initExamConfig)
# 题库随机数显示
st.write("【题库随机数：%s】" % st.session_state.exam_config.get("rnd_seed"))
# 如果是新组的卷子或者已经查看过答案的卷子
# 则进行组卷
# 初始化容器
exam_empty_placeholder = st.empty()
if not finished:
    makeATestPaper()
else:
    correctingTestPaper()
