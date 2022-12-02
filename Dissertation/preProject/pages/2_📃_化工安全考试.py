import random as rnd
import string
import json
import time
import io

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import matplotlib as mpl
import streamlit as st
from PIL import Image
import numpy as np
import requests
import jieba


# 使 matplotlib 支持中文
mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False


# -------------------- 页眉 -------------------- #
# 页面设置
st.set_page_config(page_title="化工安全考试", page_icon="📃")
if not st.session_state.get("exam_config"):
    st.session_state.exam_config = {}
# 页面标题
header = st.header("化工安全考试")
username = st.session_state.user_config.get("username") if st.session_state.get("user_config") else None
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
def initConfig():
    st.session_state.exam_config["rnd_seed"] = time.time()
    st.session_state.exam_config["finished"] = False
    st.session_state.exam_config["answers"] = dict()


# 组卷
def makeATestPaper():
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


def drawWordcloud(text, filepath, add_stop_words):
    """生成词云图

    :param str text: 文本
    :param str filepath: 图片保存路径
    :param list add_stop_words: 额外的停用词
    """
    # 图片模板
    wordcloud_png = np.array(Image.open("./data/wordcloud.jpg"))
    # 分词后空格拼接
    text = " ".join(jieba.lcut(text))
    stop_words = set(STOPWORDS)
    with open("./data/stopwords.txt", encoding="gbk") as fp:
        for stop_word in fp.readlines():
            stop_words.add(stop_word.replace("\n", ""))
    for stop_word in add_stop_words:
        stop_words.add(stop_word)
    # 设置词云参数
    wordcloud = WordCloud(
        height=400,
        background_color="white",
        mask=wordcloud_png,
        stopwords=stop_words,
        min_font_size=10
    )
    # 生成词云图
    wordcloud.generate(text)
    # 保存至文件
    wordcloud.to_file(filepath)


# 批改试卷
def correctingTestPaper():
    rnd.seed(rnd_seed)
    # 获取已做的答案
    answers = st.session_state.exam_config.get("answers")
    # 检索答案序号
    answer_index = lambda x: list(string.ascii_uppercase).index(x.upper())
    # 各部分得分
    scores = [0, 0, 0]
    # 错题词云数据
    mistakes = ["", "", ""]
    # 评估并显示错题
    with exam_empty_placeholder.container():
        # 单选部分
        st.markdown("*一、单项选择题（共40分）*")
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
            st.info("正确答案：{}".format(single_choice_question_answer))
            if single_choice_question_user_answer == single_choice_question_answer:
                st.success("您的答案：{}".format(single_choice_question_user_answer))
                scores[0] += 2
            else:
                st.error("您的答案：{}".format(single_choice_question_user_answer))
                mistakes[0] += "".join(single_choice_question_content)
        # 不定项部分
        st.markdown("*二、不定项选择题（共40分）*")
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
            st.info("正确答案：{}".format(multi_choice_question_answer))
            if multi_choice_question_user_answer == multi_choice_question_answer:
                st.success("您的答案：{}".format(multi_choice_question_user_answer))
                scores[1] += 4
            else:
                st.error("您的答案：{}".format(multi_choice_question_user_answer))
                mistakes[1] += "".join(multi_choice_question_content)
        # 判断题部分
        st.markdown("*三、判断题（共20分）*")
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
            st.info("正确答案：{}".format(judgmental_question_answer))
            if judgmental_question_user_answer == judgmental_question_answer:
                st.success("您的答案：{}".format(judgmental_question_user_answer))
                scores[2] += 2
            else:
                st.error("您的答案：{}".format(judgmental_question_user_answer))
                mistakes[2] += "".join(judgmental_question_content)
        # 开始生成图表
        # 得分饼图
        score_fig_data = plot_pie(
            projects=["单选题", "多选题", "判断题"],
            counts=np.array([40, 40, 20]) - np.array(scores),
            title="题型失分情况（总得分：%s 分）" % sum(scores)
        )
        st.image(score_fig_data, width=350)
        # 如设置了用户, 则保存本次做题结果
        if username:
            if not st.session_state.user_config.get("history"):
                st.session_state.user_config.history = []
            st.session_state.user_config.history.append({
                "rnd_seed": rnd_seed,
                "user_answer": answers,
                "scores": sum(scores)
            })
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
# 重置试卷设置按钮
st.button("重新组卷", key="make_a_test_paper", on_click=initConfig)
# 获取试卷设置
rnd_seed = st.session_state.exam_config.get("rnd_seed")
finished = st.session_state.exam_config.get("finished")
# 设置组卷随机值
if not rnd_seed:
    initConfig()
# 如果是新组的卷子或者已经查看过答案的卷子
# 则进行组卷
# 初始化容器
exam_empty_placeholder = st.empty()
if not finished:
    makeATestPaper()
else:
    correctingTestPaper()
