# 区块链交易分析工具

这是一个基于 Streamlit 和 DeepSeek API 的区块链交易分析工具。

## 功能特点

- 分析区块链交易数据
- 提取交易哈希地址
- 分析代币转移事件
- 计算地址间的代币流动
- 生成详细的分析报告

## 使用方法

1. 将区块链数据粘贴到输入框
2. 点击"分析数据"按钮
3. 查看分析结果
4. 可选择下载分析报告（JSON格式）

## 环境变量

需要设置以下环境变量：
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥

## 部署

本应用已部署在 Streamlit Cloud 上，可以直接访问：[应用链接]

## 本地运行

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
