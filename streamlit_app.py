import streamlit as st
from deepseekv5 import process_in_batches, combine_results
import json

st.set_page_config(
    page_title="区块链交易分析工具",
    layout="wide",
    initial_sidebar_state="collapsed"
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
</style>
""", unsafe_allow_html=True)

st.title("区块链交易分析工具")

# 输入区域
input_data = st.text_area(
    "请在下面粘贴区块链数据：",
    height=200,
    help="将要分析的区块链数据粘贴在这里"
)

# 分析按钮
if st.button("分析数据", type="primary"):
    if not input_data.strip():
        st.error("请先输入数据")
    else:
        try:
            with st.spinner("正在分析数据..."):
                # 处理数据
                batch_results = process_in_batches(input_data, batch_size=2, max_tokens=8192)
                final_result = combine_results(batch_results)
                
                # 显示结果
                st.json(final_result)
                
                # 提供下载选项
                st.download_button(
                    label="下载分析结果",
                    data=json.dumps(final_result, ensure_ascii=False, indent=2),
                    file_name="analysis_result.json",
                    mime="application/json"
                )
        except Exception as e:
            st.error(f"分析过程中出现错误: {str(e)}")
