import streamlit as st
import pandas as pd
import numpy as np

# ---------- 1、标题 --------- #
st.title("Uber pickups in NYC")

# ---------- 2、获取一些数据 ---------- #
# (1) 让我们首先编写一个函数来加载数据。将此代码添加到您的脚本中：
DATE_COLUMN = 'date/time'
DATA_URL = "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"


# 您会注意到这load_data是一个普通的旧函数，
# 它下载一些数据，将其放入 Pandas 数据框中，并将日期列从文本转换为日期时间。
# 该函数接受单个参数 ( nrows)，该参数指定要加载到数据框中的行数。
@st.cache
def load_data(nrows):
    u_data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    u_data.rename(lowercase, axis="columns", inplace=True)
    u_data[DATE_COLUMN] = pd.to_datetime(u_data[DATE_COLUMN])
    return u_data


# (2) 现在让我们测试函数并查看输出。在您的函数下方，添加以下行：
# Create a text element and let the reader know the data is loading.
data_load_state = st.text("Loading data...")
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Loading data...done!")

# 您会在应用程序的右上角看到几个按钮，询问您是否要重新运行该应用程序。
# 选择Always rerun，您将在每次保存时自动看到您的更改。
# 好吧，这是令人印象深刻的...
# 事实证明，下载数据需要很长时间
# 将 10,000 行加载到数据帧中，并将日期列转换为日期时间也不是一件容易的事。
# 您不希望每次更新应用程序时都重新加载数据——幸运的是 Streamlit 允许您缓存数据。

# ---------- 3、毫不费力的缓存 ---------- #
# 尝试@st.cache在load_data声明前添加：
# @st.cache
# def load_data(nrows):
# 然后保存脚本，Streamlit 将自动重新运行您的应用程序。
# 由于这是您第一次使用 运行脚本@st.cache，因此您不会看到任何变化。
# 让我们稍微调整一下您的文件，以便您可以看到缓存的强大功能。
# 将此行替换为data_load_state.text('Loading data...done!')：
# data_load_state.text("Done! (using st.cache)")
# 保存。看看您添加的行是如何立即出现的？
# 如果你退后一步，这实际上是相当惊人的。
# 幕后发生了一些神奇的事情，只需要一行代码就可以激活它。

# ---------- 4、检查原始数据 ---------- #
# 在开始使用原始数据之前，最好先查看一下您正在使用的原始数据。
# 让我们向应用程序添加一个子标题和原始数据的打印输出：
if st.checkbox('Show raw data'):
    st.subheader("Raw data")
    st.write(data)

# ---------- 5、绘制直方图 ---------- #
# (1) 首先，让我们在原始数据部分下方添加一个子标题：
st.subheader('Number of pickups by hour')
# (2) 使用 NumPy 生成一个直方图，该直方图按小时划分取件时间：
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24)
)[0]
# (3) 现在，让我们使用 Streamlit 的 st.bar_chart()方法来绘制这个直方图。
st.bar_chart(hist_values)
# (4) 保存你的脚本。此直方图应立即显示在您的应用程序中。快速查看后，最繁忙的时间是 17:00（下午 5 点）。

# ---------- 6、在地图上绘制数据 ---------- #
# 将直方图与 Uber 的数据集一起使用可以帮助我们确定什么时候最繁忙的接送时间，
# 但是如果我们想弄清楚整个城市的接送集中在哪里呢。
# 虽然您可以使用条形图来显示此数据，但除非您非常熟悉城市中的纬度和经度坐标，否则它并不容易解释。
# 为了显示拾取集中度，让我们使用 Streamlitst.map() 函数将数据叠加在纽约市地图上。
# (1) 为该部分添加一个子标题：
st.subheader("Map of all pickups")
# (2) 使用st.map()函数绘制数据：
st.map(data)
# (3) 保存你的脚本。该地图是完全互动的。通过平移或放大一点来尝试一下。
# (4) 绘制直方图后，您确定 Uber 上车最繁忙的时间是 17:00。
# (5) 让我们重新绘制地图以显示 17:00 的上车集中度。
# (6) 找到以下代码片段：
# st.subheader('Map of all pickups')
# st.map(data)
# (7) 将其替换为：
# hour_to_filter = 17
hour_to_filter = st.slider("hour", 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)
# (8) 您应该立即看到数据更新。

# ---------- 7、使用滑块过滤结果 ---------- #
# (1) 在上一节中，当您绘制地图时，用于筛选结果的时间被硬编码到脚本中，
# 但是如果我们想让读者实时动态筛选数据怎么办？
# 您可以使用 Streamlit 的小部件。st.slider()让我们使用该方法向应用程序添加一个滑块。
# (2) 找到hour_to_filter它并将其替换为以下代码片段：
# hour_to_filter = st.slider("hour", 0, 23, 17)  # min: 0h, max: 23h, default: 17h
# (3) 使用滑块并实时观看地图更新。

# ---------- 8、使用按钮切换数据 ---------- #
# (1) 滑块只是动态更改应用程序组成的一种方式。
# 让我们使用该st.checkbox函数向您的应用程序添加一个复选框。
# 我们将使用此复选框来显示/隐藏应用程序顶部的原始数据表。
# (2)找到这些行：
# st.subheader('Raw data')
# st.write(data)
# (3) 用以下代码替换这些行：
# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)
# (4) 我们确信您有自己的想法。完成本教程后，请查看我们的API 参考中 Streamlit 公开的所有小部件。