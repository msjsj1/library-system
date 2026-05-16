import streamlit as st
import random
import string
from pathlib import Path

# =========================
# 基础配置
# =========================

st.set_page_config(
    page_title="图书管理系统",
    page_icon="📚",
    layout="wide"
)

BASE_DIR = Path(__file__).parent


# =========================
# 页面美化 CSS
# =========================

st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }

    .sub-title {
        text-align: center;
        font-size: 16px;
        color: #7f8c8d;
        margin-bottom: 30px;
    }

    .captcha-box {
        background-color: #f1f5f9;
        border: 2px dashed #3b82f6;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        font-size: 26px;
        letter-spacing: 8px;
        font-weight: bold;
        color: #2563eb;
        margin-bottom: 10px;
    }

    .book-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 18px;
    }

    .book-title {
        font-size: 20px;
        font-weight: bold;
        color: #1f2937;
    }

    .book-info {
        color: #4b5563;
        line-height: 1.8;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# 初始化数据
# =========================

if "login_status" not in st.session_state:
    st.session_state.login_status = False

if "captcha" not in st.session_state:
    st.session_state.captcha = ""

if "books" not in st.session_state:
    st.session_state.books = [
        {
            "id": 1,
            "name": "Python快速入门",
            "author": "张三",
            "category": "编程",
            "price": 59.9,
            "stock": 20,
            "image": "1.jpg"
        },
        {
            "id": 2,
            "name": "人工智能基础",
            "author": "李四",
            "category": "人工智能",
            "price": 88.0,
            "stock": 15,
            "image": "2.jpg"
        }
    ]


# =========================
# 工具函数
# =========================

def generate_captcha():
    """生成验证码"""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.sample(chars, 4))


def show_image(image_name, width=140):
    """显示图片，如果图片不存在，不让程序报错"""
    image_path = BASE_DIR / image_name

    if image_path.exists():
        st.image(str(image_path), width=width)
    else:
        st.warning(f"图片不存在：{image_name}")


def get_next_id():
    """生成新的图书编号"""
    if len(st.session_state.books) == 0:
        return 1
    return max(book["id"] for book in st.session_state.books) + 1


def find_book_by_id(book_id):
    """根据编号查找图书"""
    for book in st.session_state.books:
        if book["id"] == book_id:
            return book
    return None


# =========================
# 登录页面
# =========================

def login_page():
    st.markdown('<div class="main-title">📚 图书管理系统</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">欢迎使用图书管理系统，请先登录</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        with st.container(border=True):
            st.subheader("用户登录")

            username = st.text_input("账号")
            password = st.text_input("密码", type="password")

            if st.session_state.captcha == "":
                st.session_state.captcha = generate_captcha()

            st.markdown(
                f'<div class="captcha-box">{st.session_state.captcha}</div>',
                unsafe_allow_html=True
            )

            col_a, col_b = st.columns([2, 1])

            with col_a:
                input_captcha = st.text_input("请输入验证码")

            with col_b:
                st.write("")
                st.write("")
                if st.button("刷新验证码"):
                    st.session_state.captcha = generate_captcha()
                    st.rerun()

            if st.button("登录", use_container_width=True):
                if username != "admin":
                    st.error("账号错误")
                elif password != "admin":
                    st.error("密码错误")
                elif input_captcha.upper() != st.session_state.captcha:
                    st.error("验证码错误")
                    st.session_state.captcha = generate_captcha()
                else:
                    st.session_state.login_status = True
                    st.success("登录成功")
                    st.rerun()

            st.info("默认账号：admin，默认密码：admin")


# =========================
# 首页
# =========================

def home_page():
    st.markdown('<div class="main-title">📚 图书管理系统</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">基础版图书增删改查系统</div>', unsafe_allow_html=True)

    total_books = len(st.session_state.books)
    total_stock = sum(book["stock"] for book in st.session_state.books)
    total_value = sum(book["price"] * book["stock"] for book in st.session_state.books)

    col1, col2, col3 = st.columns(3)

    col1.metric("图书种类", total_books)
    col2.metric("库存总量", total_stock)
    col3.metric("库存总价值", f"{total_value:.2f} 元")

    st.divider()

    st.subheader("图书列表")

    keyword = st.text_input("请输入书名、作者或分类进行查询")

    books = st.session_state.books

    if keyword:
        books = [
            book for book in books
            if keyword in book["name"]
            or keyword in book["author"]
            or keyword in book["category"]
        ]

    if len(books) == 0:
        st.warning("没有找到相关图书")
    else:
        for book in books:
            with st.container(border=True):
                col_img, col_info = st.columns([1, 4])

                with col_img:
                    show_image(book["image"])

                with col_info:
                    st.markdown(f"### {book['name']}")
                    st.write(f"**编号：** {book['id']}")
                    st.write(f"**作者：** {book['author']}")
                    st.write(f"**分类：** {book['category']}")
                    st.write(f"**价格：** {book['price']} 元")
                    st.write(f"**库存：** {book['stock']} 本")
                    st.write(f"**图片：** {book['image']}")


# =========================
# 添加图书
# =========================

def add_book_page():
    st.title("➕ 添加图书")

    with st.form("add_book_form"):
        name = st.text_input("图书名称")
        author = st.text_input("作者")
        category = st.selectbox("图书分类", ["编程", "人工智能", "文学", "历史", "经济", "其他"])
        price = st.number_input("价格", min_value=0.0, step=1.0)
        stock = st.number_input("库存", min_value=0, step=1)
        image = st.text_input("图片路径", value="1.jpg")

        submit = st.form_submit_button("添加图书")

        if submit:
            if name == "" or author == "":
                st.error("图书名称和作者不能为空")
            else:
                new_book = {
                    "id": get_next_id(),
                    "name": name,
                    "author": author,
                    "category": category,
                    "price": price,
                    "stock": stock,
                    "image": image
                }

                st.session_state.books.append(new_book)
                st.success("图书添加成功")


# =========================
# 修改图书
# =========================

def update_book_page():
    st.title("✏️ 修改图书")

    if len(st.session_state.books) == 0:
        st.warning("暂无图书可以修改")
        return

    book_options = {
        f"{book['id']} - {book['name']}": book["id"]
        for book in st.session_state.books
    }

    selected = st.selectbox("请选择要修改的图书", list(book_options.keys()))
    book_id = book_options[selected]
    book = find_book_by_id(book_id)

    if book:
        with st.form("update_book_form"):
            name = st.text_input("图书名称", value=book["name"])
            author = st.text_input("作者", value=book["author"])
            category = st.selectbox(
                "图书分类",
                ["编程", "人工智能", "文学", "历史", "经济", "其他"],
                index=["编程", "人工智能", "文学", "历史", "经济", "其他"].index(book["category"])
                if book["category"] in ["编程", "人工智能", "文学", "历史", "经济", "其他"] else 5
            )
            price = st.number_input("价格", min_value=0.0, step=1.0, value=float(book["price"]))
            stock = st.number_input("库存", min_value=0, step=1, value=int(book["stock"]))
            image = st.text_input("图片路径", value=book["image"])

            submit = st.form_submit_button("保存修改")

            if submit:
                book["name"] = name
                book["author"] = author
                book["category"] = category
                book["price"] = price
                book["stock"] = stock
                book["image"] = image

                st.success("图书修改成功")


# =========================
# 删除图书
# =========================

def delete_book_page():
    st.title("🗑️ 删除图书")

    if len(st.session_state.books) == 0:
        st.warning("暂无图书可以删除")
        return

    book_options = {
        f"{book['id']} - {book['name']}": book["id"]
        for book in st.session_state.books
    }

    selected = st.selectbox("请选择要删除的图书", list(book_options.keys()))
    book_id = book_options[selected]
    book = find_book_by_id(book_id)

    if book:
        st.warning("你即将删除以下图书：")

        col1, col2 = st.columns([1, 4])

        with col1:
            show_image(book["image"])

        with col2:
            st.write(f"**编号：** {book['id']}")
            st.write(f"**名称：** {book['name']}")
            st.write(f"**作者：** {book['author']}")
            st.write(f"**分类：** {book['category']}")
            st.write(f"**价格：** {book['price']} 元")
            st.write(f"**库存：** {book['stock']} 本")

        confirm = st.checkbox("确认删除")

        if st.button("删除图书"):
            if confirm:
                st.session_state.books = [
                    item for item in st.session_state.books
                    if item["id"] != book_id
                ]
                st.success("删除成功")
                st.rerun()
            else:
                st.error("请先勾选确认删除")


# =========================
# 查询图书
# =========================

def search_book_page():
    st.title("🔍 查询图书")

    keyword = st.text_input("请输入查询关键词")

    if keyword:
        result = [
            book for book in st.session_state.books
            if keyword in book["name"]
            or keyword in book["author"]
            or keyword in book["category"]
            or keyword == str(book["id"])
        ]

        if len(result) == 0:
            st.warning("没有查询到相关图书")
        else:
            st.success(f"查询到 {len(result)} 本图书")

            for book in result:
                with st.container(border=True):
                    col1, col2 = st.columns([1, 4])

                    with col1:
                        show_image(book["image"])

                    with col2:
                        st.write(f"**编号：** {book['id']}")
                        st.write(f"**名称：** {book['name']}")
                        st.write(f"**作者：** {book['author']}")
                        st.write(f"**分类：** {book['category']}")
                        st.write(f"**价格：** {book['price']} 元")
                        st.write(f"**库存：** {book['stock']} 本")
                        st.write(f"**图片：** {book['image']}")
    else:
        st.info("请输入关键词后开始查询")


# =========================
# 主程序
# =========================

if not st.session_state.login_status:
    login_page()
else:
    with st.sidebar:
        st.title("📚 管理菜单")
        st.write("当前用户：admin")

        menu = st.radio(
            "请选择功能",
            ["首页", "添加图书", "修改图书", "删除图书", "查询图书"]
        )

        st.divider()

        if st.button("退出登录", use_container_width=True):
            st.session_state.login_status = False
            st.session_state.captcha = generate_captcha()
            st.rerun()

    if menu == "首页":
        home_page()
    elif menu == "添加图书":
        add_book_page()
    elif menu == "修改图书":
        update_book_page()
    elif menu == "删除图书":
        delete_book_page()
    elif menu == "查询图书":
        search_book_page()