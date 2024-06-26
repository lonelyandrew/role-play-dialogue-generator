from typing import Iterable

from loguru import logger
from zhipuai import ZhipuAI
from zhipuai.core import StreamResponse


def generate_role_description(role_name: str, text: str, client: ZhipuAI, model_name: str = "glm-4") -> Iterable[str]:
    """根据给定文本生成角色描述。

    Args:
        role_name: 角色名称。
        text: 输入文本，1000个字符以内。
        client: 智谱AI客户端。
        model_name: 使用模型名称。

    Returns:
        返回角色描述字符串。
    """
    truncated_text = text[:1000]
    logger.info("用户输入文本: {}", truncated_text)
    system_message: str = f"""
        你是一个角色生成器，请根据用户提供的文本提炼文中{role_name}的人物性格，生成该角色的角色人设，性格描述及角色相关情况的简要概述。
    """
    try:
        response: StreamResponse = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "system", "content": system_message}, {"role": "user", "content": truncated_text}],
            stream=True,
        )
        for chunk in response:
            yield chunk.choices[0].delta.content

    except Exception as e:
        raise Exception(f"发生了未知错误：{e}")
