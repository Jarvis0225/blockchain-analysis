import streamlit as st
from deepseekv5 import process_in_batches, combine_results
import json

# 配置页面
st.set_page_config(
    page_title="区块链交易分析工具",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': '区块链交易分析工具 v1.0'
    }
)

# 设置页面样式
st.markdown("""
<style>
    .stTextInput > div > div > input {
        font-family: monospace;
    }
    .stTextArea > div > textarea {
        font-family: monospace;
    }
    pre {
        white-space: pre-wrap;
    }
    .stAlert > div {
        word-wrap: break-word;
    }
    .streamlit-expanderHeader {
        font-size: 1em;
    }
    div[data-testid="stStatusWidget"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.title("区块链交易分析工具")

# 检查是否有API密钥
try:
    if not st.secrets.get("DEEPSEEK_API_KEY"):
        st.error("请在 Streamlit Cloud 中设置 DEEPSEEK_API_KEY")
        st.stop()
except Exception as e:
    st.error("请在 Streamlit Cloud 中设置 DEEPSEEK_API_KEY")
    st.stop()

# 输入区域
with st.form("analysis_form"):
    input_data = st.text_area(
        "请在下面粘贴区块链数据：",
        height=200,
        help="将要分析的区块链数据粘贴在这里",
        placeholder="在此粘贴 JSON 格式的区块链数据..."
    )
    
    submitted = st.form_submit_button("分析数据", type="primary")

if submitted:
    if not input_data.strip():
        st.error("请先输入数据")
    else:
        try:
            # 创建进度条和状态文本
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 处理数据
            status_text.text("开始分析数据...")
            batch_results = process_in_batches(
                input_data, 
                progress_bar=progress_bar,
                status_text=status_text,
                batch_size=2, 
                max_tokens=8192
            )
            
            # 合并结果
            final_result = combine_results(batch_results)
            
            # 清理进度显示
            progress_bar.empty()
            status_text.empty()
            
            # 显示结果
            with st.expander("查看分析结果", expanded=True):
                st.json(final_result)
            
            # 提供下载选项
            st.download_button(
                label="下载分析结果",
                data=json.dumps(final_result, ensure_ascii=False, indent=2),
                file_name="analysis_result.json",
                mime="application/json",
                help="点击下载 JSON 格式的分析结果"
            )
        except Exception as e:
            # 清理进度显示
            if 'progress_bar' in locals():
                progress_bar.empty()
            if 'status_text' in locals():
                status_text.empty()
            
            st.error(f"分析过程中出现错误: {str(e)}")
            st.error("请确保输入数据格式正确，并且已正确设置 DeepSeek API 密钥")
