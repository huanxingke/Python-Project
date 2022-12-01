import streamlit as st


content = """

---------------------------------------------------------------------------

一、运行多页面应用程序
运行多页应用程序与运行单页应用程序相同。运行多页应用程序的命令是：

streamlit run [entrypoint file]

“入口点文件”是应用程序将显示给用户的第一个页面。
将页面添加到应用程序后，入口点文件将显示为侧边栏中的最顶层页面。
您可以将入口点文件视为应用程序的“主页”。
例如，假设您的入口点文件是Home.py.
然后，要运行您的应用程序，您可以运行streamlit run Home.py.
 这将启动您的应用程序并执行Home.py.
 
---------------------------------------------------------------------------

二、添加页面
创建入口点文件后，您可以通过在与入口点文件相关.py的目录中创建文件来添加页面pages/。
例如，如果您的入口点文件是Home.py，那么您可以创建一个pages/About.py文件来定义“关于”页面。这是多页应用程序的有效目录结构：

Home.py # This is the file you run with "streamlit run"
└─── pages/
  └─── About.py # This is a page
  └─── 2_Page_two.py # This is another page
  └─── 3_😎_three.py # So is this

Tips:
将表情符号添加到文件名时，最好包含一个数字前缀，以便更轻松地在终端中自动完成。
终端自动完成可能会被 unicode（表情符号的表示方式）弄糊涂。

页面被定义为.py目录中的pages/文件。
页面的文件名根据以下部分中的规则转换为侧边栏中的页面名称。
例如，该About.py文件将在侧边栏中显示为“关于”，2_Page_two.py显示为“第二页”，3_😎_three.py显示为“😎三”。

只有.py目录中的pages/文件才会作为页面加载。Streamlit 忽略pages/目录和子目录中的所有其他文件。

---------------------------------------------------------------------------

三、如何在 UI 中标记和排序页面
侧边栏 UI 中的页面标签是从文件名生成的。
它们可能与设置的页面标题不同st.set_page_config。
让我们了解什么构成页面的有效文件名、页面如何显示在边栏中以及页面如何排序。

1、页面的有效文件名
文件名由四个不同的部分组成：
(1) A number— 如果文件以数字为前缀。
(2) 分隔符 — 可以是_, -, 空格或其任意组合。
(3) A label- 这是一切，但不包括，.py。
(4) 扩展名 — 始终是.py.

2、侧边栏中页面的显示方式
侧边栏显示的是label文件名的一部分：
(1) 如果没有label，Streamlit 会使用 the number作为标签。
(2) 在 UI 中，Streamlit通过用空格label替换来美化 _

3、侧边栏中的页面如何排序
排序将文件名中的数字视为实际数字（整数）：
(1) 带有 .的文件number出现在没有 . 的文件之前number。
(2) 文件根据number（如果有）排序，然后是title（如果有）。
(3) 对文件进行排序时，Streamlit 将其number视为实际数字而不是字符串。所以03是一样的3。

Tips:
表情符号可用于使您的页面名称更有趣！
例如，名为的文件🏠_Home.py将在侧边栏中创建一个标题为“🏠 Home”的页面。

---------------------------------------------------------------------------

四、在页面之间导航
页面会自动显示在应用程序侧边栏内漂亮的导航 UI 中。
当您单击侧边栏 UI 中的页面时，Streamlit 会导航到该页面而无需重新加载整个前端——使应用程序浏览速度非常快！

您还可以使用 URL 在页面之间导航。
页面有自己的 URL，由文件的label. 
当多个文件具有相同的label时，Streamlit 会选择第一个（基于上述顺序）。
用户可以通过访问页面的 URL 来查看特定页面。

如果用户尝试访问不存在的页面的 URL，
他们将看到如下所示的模式，
表示用户请求的页面在应用程序的 pages/ 目录中找不到。

---------------------------------------------------------------------------

五、笔记
1、页面支持魔术命令。
2、页面支持保存时运行。此外，当您保存页面时，这会导致当前正在查看该页面的用户重新运行。
3、添加或删除页面会导致 UI 立即更新。
4、更新侧边栏中的页面不会重新运行脚本。
5、st.set_page_config在页面级别工作。当您使用st.set_page_config设置标题或图标时，这仅适用于当前页面。

6、页面在全局范围内共享相同的 Python 模块：
# page1.py
import foo
foo.hello = 123

# page2.py
import foo
st.write(foo.hello)  # If page1 already executed, this should write 123

7、页面共享相同的st.session_state：
# page1.py
import streamlit as st
if "shared" not in st.session_state:
   st.session_state["shared"] = True

# page2.py
import streamlit as st
st.write(st.session_state["shared"])
# If page1 already executed, this should write True
"""
st.write(content)