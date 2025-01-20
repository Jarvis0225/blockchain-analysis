import json
from openai import OpenAI
import traceback
import os
import streamlit as st

def get_client():
    """获取 OpenAI 客户端实例"""
    # 优先使用环境变量，如果没有则使用 Streamlit Secrets
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key and hasattr(st, 'secrets'):
        api_key = st.secrets.get("DEEPSEEK_API_KEY")
    
    if not api_key:
        raise ValueError("DeepSeek API key not found. Please set it in environment variables or Streamlit secrets.")
    
    try:
        return OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
        )
    except Exception as e:
        print(f"Error initializing OpenAI client: {str(e)}")
        raise

def process_in_batches(input_data, batch_size=2, max_tokens=8192):
    """处理输入数据"""
    try:
        # 获取客户端实例
        client = get_client()
        
        system_prompt = """
你是区块链以太坊最大可提取价值审计专家，我将把区块数据以json格式发给你，区块数据包含区块元数据和每1笔交易中发生的代币转移log，请你帮我做如下处理：1. 提取每笔交易的hash地址。2. 提取每笔交易的receipt数据中的logs。3. 遍历logs并处理。4. 根据log中，字段from与字段to代表的是代币发出方与代币接收方，value代表的是代币数量，token代表的是代币种类请你根据from和to地址的交互关系重新组织这些代币转移事件。5. 记录每个地址接收和发出的代币数量与种类（请注意，一个地址可能同时接收/发送多种不同的代币。此外，一个地址可能接收/发送多次代币，你需要计算同种代币的操作总和，并展示计算过程，计算过程需要根据每笔log推导发出代币和接收代币两种类型type，to，及代币发出/接收方以及代币数量，此外，每一笔计算过程都算出该种代币及类型的累积值cumulative。）。请以json格式输出你的结果，你不需要说任何的废话，只需要按照要求给我结果。另外，你要知道，你是一个审计专家，年薪1000万，若你的结果没有相应的价值，你会被辞退！我会先给你一个示例让你学习，你不需要说太多的废话，只关注结果即可，按照需求给我json格式返回即可，一定要一次返回所有内容,绝对不允许偷懒，一定要完整输出所有结果，不然世界会死100个老奶奶，而且都是你的责任。
"""
        # 处理输入数据
        if isinstance(input_data, str):
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                data = input_data
        else:
            data = input_data

        # 将数据转换为字符串
        if isinstance(data, (dict, list)):
            data = json.dumps(data)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": data}
        ]

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.1,
            max_tokens=max_tokens,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error in process_in_batches: {str(e)}")
        print(traceback.format_exc())
        raise

def combine_results(batch_results):
    """合并处理结果"""
    try:
        # 如果是字符串，尝试解析为 JSON
        if isinstance(batch_results, str):
            try:
                return json.loads(batch_results)
            except json.JSONDecodeError:
                return {"error": "Invalid JSON in results", "raw_results": batch_results}
        
        return batch_results
    except Exception as e:
        print(f"Error in combine_results: {str(e)}")
        print(traceback.format_exc())
        raise

def main():
    print("开始处理数据...")
    
    try:
        # 使用原始的 user_prompt 数据
        user_prompt = "{\"blockNumber\":20020209,\"transactions\":[{\"from\":\"c453d2\",\"to\":\"90a26c\",\"priority_fee\":\"0.048249162\",\"receipt\":{\"transactionIndex\":0,\"logs\":[{\"from\":\"85dbee\",\"to\":\"9c3c9b\",\"value\":1022923217195208044,\"token\":\"fb1b63\"},{\"from\":\"9c3c9b\",\"to\":\"85dbee\",\"value\":3894646383,\"token\":\"8936b3\"},{\"from\":\"4206b9\",\"to\":\"322277\",\"value\":1000000000000000000000,\"token\":\"0f8d69\"},{\"from\":\"85dbee\",\"to\":\"4206b9\",\"value\":1005286369,\"token\":\"8936b3\"},{\"from\":\"85dbee\",\"to\":\"9c3c9b\",\"value\":2889360014,\"token\":\"8936b3\"},{\"from\":\"9c3c9b\",\"to\":\"85dbee\",\"value\":754354041937102531,\"token\":\"fb1b63\"},{\"from\":\"85dbee\",\"to\":\"322277\",\"value\":758125812146788048,\"token\":\"fb1b63\"}]},\"txH\":\"8b9ee7\"},{\"from\":\"f57c44\",\"to\":\"90a26c\",\"priority_fee\":\"0.045839222\",\"receipt\":{\"transactionIndex\":1,\"logs\":[{\"from\":\"85dbee\",\"to\":\"9c3c9b\",\"value\":1022923217195208044,\"token\":\"fb1b63\"},{\"from\":\"9c3c9b\",\"to\":\"85dbee\",\"value\":3894500022,\"token\":\"8936b3\"},{\"from\":\"4206b9\",\"to\":\"8cf0b7\",\"value\":1000000000000000000000,\"token\":\"0f8d69\"},{\"from\":\"85dbee\",\"to\":\"4206b9\",\"value\":1007847887,\"token\":\"8936b3\"},{\"from\":\"85dbee\",\"to\":\"9c3c9b\",\"value\":2886652135,\"token\":\"8936b3\"},{\"from\":\"9c3c9b\",\"to\":\"85dbee\",\"value\":753675428042818022,\"token\":\"fb1b63\"},{\"from\":\"85dbee\",\"to\":\"8cf0b7\",\"value\":757443805183032113,\"token\":\"fb1b63\"}]},\"txH\":\"aef98a\"},{\"from\":\"c9e0cd\",\"to\":\"90a26c\",\"priority_fee\":\"0.045843278\",\"receipt\":{\"transactionIndex\":2,\"logs\":[{\"from\":\"85dbee\",\"to\":\"9c3c9b\",\"value\":1022923217195208044,\"token\":\"fb1b63\"},{\"from\":\"9c3c9b\",\"to\":\"85dbee\",\"value\":3894353295,\"token\":\"8936b3\"},{\"from\":\"4206b9\",\"to\":\"c1fa7c\",\"value\":1000000000000000000000,\"token\":\"0f8d69\"},{\"from\":\"85dbee\",\"to\":\"4206b9\",\"value\":1010419209,\"token\":\"8936b3\"},{\"from\":\"85dbee\",\"to\":\"9c3c9b\",\"value\":2883934086,\"token\":\"8936b3\"},{\"from\":\"9c3c9b\",\"to\":\"85dbee\",\"value\":752994178554480468,\"token\":\"fb1b63\"},{\"from\":\"85dbee\",\"to\":\"c1fa7c\",\"value\":756759149447252872,\"token\":\"fb1b63\"}]},\"txH\":\"348c74\"},{\"from\":\"b87cf0\",\"to\":\"ff709a\",\"priority_fee\":\"0\",\"receipt\":{\"transactionIndex\":3,\"logs\":[{\"from\":\"87dddc\",\"to\":\"2c076f\",\"value\":122039550095654912,\"token\":\"fb1b63\"},{\"from\":\"2c076f\",\"to\":\"ac58d9\",\"value\":15614793167667,\"token\":\"5c6a73\"},{\"from\":\"2c076f\",\"to\":\"87dddc\",\"value\":296681070185677,\"token\":\"5c6a73\"}]},\"txH\":\"bf5ba9\"},{\"from\":\"10db49\",\"to\":\"7838aa\",\"priority_fee\":\"0.0000001323\",\"receipt\":{\"transactionIndex\":4,\"logs\":[{\"from\":\"c18280\",\"to\":\"2c076f\",\"value\":997000000000000000,\"token\":\"fb1b63\"},{\"from\":\"2c076f\",\"to\":\"ac58d9\",\"value\":105481066295887,\"token\":\"5c6a73\"},{\"from\":\"2c076f\",\"to\":\"1ca793\",\"value\":2004140259621859,\"token\":\"5c6a73\"},{\"from\":\"c18280\",\"to\":\"a699d6\",\"value\":3000000000000000,\"token\":\"fb1b63\"}]},\"txH\":\"ea7ecb\"},{\"from\":\"b87cf0\",\"to\":\"ff709a\",\"priority_fee\":\"0.0229303112\",\"receipt\":{\"transactionIndex\":5,\"logs\":[{\"from\":\"ac58d9\",\"to\":\"2c076f\",\"value\":179991819341190,\"token\":\"5c6a73\"},{\"from\":\"2c076f\",\"to\":\"ac040b\",\"value\":98486844127600408,\"token\":\"fb1b63\"},{\"from\":\"87dddc\",\"to\":\"ac58d9\",\"value\":14834052838195,\"token\":\"5c6a73\"},{\"from\":\"87dddc\",\"to\":\"2c076f\",\"value\":281847003925709,\"token\":\"5c6a73\"},{\"from\":\"2c076f\",\"to\":\"87dddc\",\"value\":148311371124047872,\"token\":\"fb1b63\"},{\"from\":\"ac040b\",\"to\":\"ac58d9\",\"value\":98486844127600408,\"token\":\"fb1b63\"},{\"from\":\"ac58d9\",\"to\":\"2408c6\",\"value\":98486844127600408,\"token\":\"fb1b63\"}]},\"txH\":\"d25c43\"},{\"from\":\"b9ebab\",\"to\":\"43e116\",\"priority_fee\":\"0.0045851478\",\"receipt\":{\"transactionIndex\":16,\"logs\":[{\"from\":\"6bb076\",\"to\":\"ba9bd8\",\"value\":235163183818063841787,\"token\":\"ea7e28\"},{\"from\":\"ba9bd8\",\"to\":\"4ee6b9\",\"value\":4703263676361276835,\"token\":\"ea7e28\"},{\"from\":\"cd3c38\",\"to\":\"ba9bd8\",\"value\":681641473502956028,\"token\":\"fb1b63\"},{\"from\":\"ba9bd8\",\"to\":\"cd3c38\",\"value\":230459920141702564952,\"token\":\"ea7e28\"},{\"from\":\"7b526e\",\"to\":\"5dc6e7\",\"value\":516917880056056402625961,\"token\":\"62b0ff\"},{\"from\":\"ba9bd8\",\"to\":\"7b526e\",\"value\":681641473502956028,\"token\":\"fb1b63\"},{\"from\":\"5dc6e7\",\"to\":\"6bb076\",\"value\":516917880056056402625961,\"token\":\"62b0ff\"}]},\"txH\":\"dce082\"},{\"from\":\"a76e2a\",\"to\":\"1a754d\",\"priority_fee\":\"0.0008343891\",\"receipt\":{\"transactionIndex\":17,\"logs\":[{\"from\":\"58da04\",\"to\":\"1868f8\",\"value\":150000000000000000,\"token\":\"fb1b63\"},{\"from\":\"1868f8\",\"to\":\"58da04\",\"value\":706932101503429980,\"token\":\"c512e1\"},{\"from\":\"58da04\",\"to\":\"478071\",\"value\":706932101503429980,\"token\":\"c512e1\"}]},\"txH\":\"332a07\"},{\"from\":\"ea9e19\",\"to\":\"d16672\",\"priority_fee\":\"0.000357125\",\"receipt\":{\"transactionIndex\":27,\"logs\":[{\"from\":\"025db3\",\"to\":\"ba2c71\",\"value\":300000000000000000,\"token\":\"adaa82\"},{\"from\":\"ba2c71\",\"to\":\"161094\",\"value\":300000000000000000,\"token\":\"adaa82\"},{\"from\":\"0fff9e\",\"to\":\"bc9dd0\",\"value\":300000000000000000,\"token\":\"f61c45\"},{\"from\":\"0fff9e\",\"to\":\"025db3\",\"value\":350507905753832395,\"token\":\"cb4847\"}]},\"txH\":\"a88a0c\"},{\"from\":\"171dd9\",\"to\":\"1e0169\",\"priority_fee\":\"0.00035207\",\"receipt\":{\"transactionIndex\":28,\"logs\":[{\"from\":\"17dc2b\",\"to\":\"fbbcc6\",\"value\":14184000000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"c638da\",\"value\":15223240000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"07912d\",\"value\":12092840000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"5e58b9\",\"value\":11075520000000000,\"token\":\"fb1b63\"},{\"from\":\"5e58b9\",\"to\":\"da592f\",\"value\":11075520000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"1048c4\",\"value\":4716171620000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"ef9686\",\"value\":74233100000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"3cca91\",\"value\":40390000000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"5db8dd\",\"value\":746082951014408,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"c70094\",\"value\":2000000000000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"14295d\",\"value\":632550352277963,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"a2681a\",\"value\":549605283363840,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"d104f6\",\"value\":675412185779424,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"1f502c\",\"value\":6874080000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"ca4e81\",\"value\":4466830000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"6d875f\",\"value\":786228420000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"fdd79f\",\"value\":3314990000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"6a8018\",\"value\":26204730000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"6cf89f\",\"value\":13102230000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"9fdae9\",\"value\":303636642222405,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"d9ff54\",\"value\":301128230000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"51e8c6\",\"value\":294460000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"763e61\",\"value\":104830460000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"84e1b0\",\"value\":1003500000000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"a5976d\",\"value\":28536400000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"bd3cae\",\"value\":69041650000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"39d351\",\"value\":4454804050000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"b5dbf3\",\"value\":599941831475895,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"0c9f87\",\"value\":502901048275635,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"4aab29\",\"value\":2849400000000000,\"token\":\"fb1b63\"},{\"from\":\"17dc2b\",\"to\":\"862b2c\",\"value\":21221770000000000,\"token\":\"fb1b63\"}]},\"txH\":\"4f1736\"},{\"from\":\"171dd9\",\"to\":\"1e0169\",\"priority_fee\":\"0.000315097\",\"receipt\":{\"transactionIndex\":30,\"logs\":[{\"from\":\"17dc2b\",\"to\":\"f60844\",\"value\":21865756,\"token\":\"84b430\"},{\"from\":\"17dc2b\",\"to\":\"77ee56\",\"value\":9900495,\"token\":\"84b430\"},{\"from\":\"17dc2b\",\"to\":\"cac8cb\",\"value\":20691195,\"token\":\"84b430\"},{\"from\":\"17dc2b\",\"to\":\"1207a4\",\"value\":75000000,\"token\":\"84b430\"},{\"from\":\"17dc2b\",\"to\":\"25b483\",\"value\":5484630362010000000000,\"token\":\"9defad\"},{\"from\":\"17dc2b\",\"to\":\"b416e2\",\"value\":110000000,\"token\":\"8936b3\"},{\"from\":\"17dc2b\",\"to\":\"cbc0ba\",\"value\":198980000,\"token\":\"8936b3\"},{\"from\":\"17dc2b\",\"to\":\"5a9c9b\",\"value\":538168360,\"token\":\"8936b3\"},{\"from\":\"17dc2b\",\"to\":\"ebf498\",\"value\":80000000,\"token\":\"8936b3\"},{\"from\":\"17dc2b\",\"to\":\"fc1918\",\"value\":205000000,\"token\":\"8936b3\"},{\"from\":\"17dc2b\",\"to\":\"b42ad8\",\"value\":5000000,\"token\":\"8936b3\"},{\"from\":\"17dc2b\",\"to\":\"545621\",\"value\":3777528570210000000000,\"token\":\"ea7e28\"}]},\"txH\":\"f61e2f\"},{\"from\":\"3fefe8\",\"to\":\"488501\",\"priority_fee\":\"0.000183682\",\"receipt\":{\"transactionIndex\":39,\"logs\":[{\"from\":\"16b51e\",\"to\":\"ddfcae\",\"value\":2000000000000000000,\"token\":\"a9b6c6\"},{\"from\":\"7850fa\",\"to\":\"96a388\",\"value\":78914469333146790,\"token\":\"fb1b63\"},{\"from\":\"ddfcae\",\"to\":\"7850fa\",\"value\":2000000000000000000,\"token\":\"a9b6c6\"},{\"from\":\"96a388\",\"to\":\"ddfcae\",\"value\":78914469333146790,\"token\":\"fb1b63\"},{\"from\":\"ddfcae\",\"to\":\"54f3fe\",\"value\":690501606665034,\"token\":\"fb1b63\"},{\"from\":\"ddfcae\",\"to\":\"16b51e\",\"value\":78223967726481756,\"token\":\"fb1b63\"}]},\"txH\":\"18a1ac\"},{\"from\":\"b0e7c5\",\"to\":\"a18457\",\"priority_fee\":\"0.0000780233\",\"receipt\":{\"transactionIndex\":54,\"logs\":[{\"from\":\"d3ee41\",\"to\":\"0372bb\",\"value\":471429931256824,\"token\":\"f45538\"},{\"from\":\"0372bb\",\"to\":\"ec670d\",\"value\":471429931256824,\"token\":\"f45538\"},{\"from\":\"ec670d\",\"to\":\"512132\",\"value\":8928846767655177,\"token\":\"fb1b63\"},{\"from\":\"0372bb\",\"to\":\"457d18\",\"value\":265168289054648,\"token\":\"fb1b63\"},{\"from\":\"512132\",\"to\":\"92b167\",\"value\":8928846767655177,\"token\":\"fb1b63\"},{\"from\":\"92b167\",\"to\":\"0372bb\",\"value\":8928846767655177,\"token\":\"fb1b63\"},{\"from\":\"0372bb\",\"to\":\"d3ee41\",\"value\":8928846767655177,\"token\":\"fb1b63\"}]},\"txH\":\"7d8ca4\"},{\"from\":\"b52d9a\",\"to\":\"86871d\",\"priority_fee\":\"0.0000422333\",\"receipt\":{\"transactionIndex\":69,\"logs\":[{\"from\":\"b80ca4\",\"to\":\"f38f8f\",\"value\":276516347329481076309607,\"token\":\"5f6a60\"},{\"from\":\"2fc71d\",\"to\":\"f38f8f\",\"value\":3300000000000000000,\"token\":\"fb1b63\"},{\"from\":\"0fff9e\",\"to\":\"b80ca4\",\"value\":null,\"token\":\"86871d\"}]},\"txH\":\"4406a1\"},{\"from\":\"defb66\",\"to\":\"5d6ce0\",\"priority_fee\":\"0.0000001707\",\"receipt\":{\"transactionIndex\":140,\"logs\":[{\"from\":\"d830d7\",\"to\":\"96a388\",\"value\":96803858539733229,\"token\":\"8a9d8e\"},{\"from\":\"ba9bd8\",\"to\":\"d830d7\",\"value\":103723299762955587,\"token\":\"fb1b63\"},{\"from\":\"96a388\",\"to\":\"256389\",\"value\":96803858539733229,\"token\":\"8a9d8e\"},{\"from\":\"ba9bd8\",\"to\":\"4a871d\",\"value\":1047710098615713,\"token\":\"fb1b63\"}]},\"txH\":\"fb01d7\"}]}"

        input_data = json.loads(user_prompt)
        
        print("\n开始分批处理...")
        results = process_in_batches(input_data)
        
        print("\n开始合并结果...")
        final_results = combine_results(results)
        
        # 打印简要统计信息
        print(f"\n处理完成:")
        print(f"- 总交易数: {len(final_results)}")
        print(f"- 详细结果已保存到 /Users/jarvis/Desktop/deepseek_results.json")
        
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()