import time

import streamlit as st
import pandas as pd
import numpy as np


# ---------- 0、启动 --------- #
# streamlit run starting.py

# ---------- 1、st.write() --------- #
# st.write()是 Streamlit 的“瑞士军刀”。
# 您几乎可以将任何内容传递给st.write()：文本、数据、Matplotlib 图形、Altair 图表等。
# 别担心，Streamlit 会弄明白并以正确的方式呈现事物。
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    "first column": [1, 2, 3, 4],
    "second column": [10, 20, 30, 40]
}))

# ---------- 2、魔术方法 --------- #
# 您还可以在不调用任何 Streamlit 方法的情况下写入您的应用程序。
# Streamlit 支持“魔术命令”，这意味着您根本不必使用 st.write()！
# 要查看实际效果，请尝试以下代码片段：
df = pd.DataFrame({
    "first column": [1, 2, 3, 4],
    "second column": [10, 20, 30, 40]
})
# 魔术方法的运行机制很简单。
# 任何时候当Streamlit看到一个变量或字面量，它 就会自动调用st.write()来输出。
df

# ---------- 3、交互式表格的样式设置 --------- #
# 使用 PandasStyler对象突出显示交互式表格中的一些元素。
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=("col %d" % i for i in range(20))
)
st.dataframe(dataframe.style.highlight_max(color="blue"))

# ---------- 4、静态表格 --------- #
# Streamlit 也有静态表生成的方法：st.table().
st.table(dataframe)

# ---------- 5、绘制地图 --------- #
# 使用st.map()你可以在地图上显示数据点。
# 让我们使用Numpy来生成一些样本数据，然后在旧金山的地图上把这些点画出来：
# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=["lat", "lon"])
# st.map(map_data)

# ---------- 6、绘制折线图 --------- #
# st.checkbox()接收单一参数作为复选框的标签。
# 在下面的示例代码中，使用复选框来切换条件语句：
# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=["a", "b", "c"]
# )
# st.line_chart(chart_data)

# ---------- 7、滑块小部件 --------- #
x = st.slider("x")
st.write(x, "squared is", x * x)

# ---------- 8、复选框 --------- #
# 复选框的一个用例是隐藏或显示应用程序中的特定图表或部分。
# st.checkbox()接受一个参数，即小部件标签。在此示例中，复选框用于切换条件语句。
if st.checkbox("Show dataframe"):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=["a", "b", "c"])
    chart_data

# ---------- 9、选择列表 --------- #
# 使用st.selectbox来从序列中进行选择。
# 你可以写入任何需要的选项，或者传入一个数据或数据帧列。
option = st.selectbox(
    "Which number do you like best?",
    df["first column"],
    key="inner"
)
"You selected: ", option

# ---------- 10、侧边栏 --------- #
# Streamlit 使用 st.sidebar. 
# 传递给的每个元素 st.sidebar都固定在左侧，
# 使用户可以专注于应用程序中的内容，同时仍然可以访问 UI 控件。
# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"),
    key="add_selectbox"
)
"You selected in siderbar add_selectbox: ", add_selectbox
# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    "Select a range of values",
    0.0, 100.0, (25.0, 75.0)
)
"You selected in siderbar add_slider: ", add_slider

# ---------- 11、st.columns并排布局 --------- #
# 除了侧边栏之外，Streamlit 还提供了几种其他方式来控制应用程序的布局。
# st.columns让您并排放置小部件，
# st.expander让您通过隐藏大内容来节省空间。
left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button("Press me!")
# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        "Sorting hat",
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")
    )
    st.write(f"You are in {chosen} house!")


# ---------- 12、显示进度 --------- #
# 如果应用中有长时间的计算，你可以使用st.progress()来实时显示进度状态。
# 首先，让我们引入time包。我们将使用time.sleep()方法来模拟长时间的计算：
# "Starting a long computation..."
# # Add a placeholder
# latest_iteration = st.empty()
# bar = st.progress(0)
# for i in range(100):
#     # Update the progress bar with each iteration.
#     latest_iteration.text(f"Iteration {i + 1}")
#     bar.progress(i + 1)
#     time.sleep(0.1)
# "...and now we\'re done!"

# ---------- 13、显示进度 --------- #
# Streamlit 缓存使您的应用程序即使在从 Web 加载数据、处理大型数据集或执行昂贵的计算时也能快速执行。
# 要使用缓存，请使用 @st.cache装饰器包装函数：
@st.cache
def my_slow_function(num1, num2):
    # Do something really slow in here!
    return num1 ** num2


func_slider = st.slider(
    "Select a range of values",
    0, 10, (3, 7),
    key="func_slider"
)
st.write(my_slow_function(func_slider[0], func_slider[1]))


# ---------- 14、页数 --------- #
# 随着应用程序变得越来越大，将它们组织成多个页面变得很有用。
# 这使得应用程序更容易作为开发人员进行管理，并且更易于作为用户进行导航。
# Streamlit 提供了一种创建多页应用程序的顺畅方式。
# 我们设计此功能是为了让构建多页应用程序与构建单页应用程序一样简单！
# 只需将更多页面添加到现有应用程序，如下所示：
# 在包含主脚本的文件夹中，创建一个新pages文件夹。假设您的主脚本名为main_page.py.
# 在文件夹中添加新.py文件以pages向您的应用程序添加更多页面。
# streamlit run main_page.py照常运行。
# 该main_page.py脚本现在将对应于您应用程序的主页。
# 您会pages在边栏页面选择器中看到该文件夹中的其他脚本。例如：
# st.markdown("# Main page 🎈")
# st.sidebar.markdown("# Main page 🎈")
