from datetime import datetime, timedelta


def transform_to_custom_format(prompt, response):
    timestamp_prompt = datetime.now().isoformat()  # 获取当前时间的 ISO 格式
    timestamp_response = (
        datetime.now() + timedelta(seconds=3)
    ).isoformat()  # 假设 AI 回答在 3 秒后

    custom_format = [
        {
            "page_content": prompt,
            "metadata": {
                "sender": "Human",
                "receiver": "AI",
                "timestamp": timestamp_prompt,
                "type": "message",
            },
        },
        {
            "page_content": response,
            "metadata": {
                "sender": "AI",
                "receiver": "Human",
                "timestamp": timestamp_response,
                "type": "message",
            },
        },
    ]

    return custom_format


def transform_messages_to_streamlit_format(messages):
    transformed_messages = []

    for message in messages:
        # 检查 sender 字段，并据此设置 role
        if message["metadata"]["sender"] == "Human":
            role = "user"
        elif message["metadata"]["sender"] == "AI":
            role = "assistant"
        else:
            # 如果 sender 既不是 Human 也不是 AI，可以跳过或做其他处理
            continue

        # 获取 text 作为 content
        content = message["text"]

        # 将转换后的消息添加到列表中
        transformed_messages.append({"role": role, "content": content})

    return transformed_messages
