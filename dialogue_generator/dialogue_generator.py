from typing import Iterator

from zhipuai import ZhipuAI
from zhipuai.core import StreamResponse


def generate_role_play_dialogue(
    bot_name: str,
    bot_role: str,
    user_name: str,
    user_role: str,
    history: list[dict[str, str]],
    client: ZhipuAI,
) -> Iterator[str]:
    """根据给定的角色人设，交替生成他们之间的对话。

    Args:
        bot_name: 助手角色名。
        bot_role: 助手角色的人设描述。
        user_name: 用户角色名。
        user_role: 用户角色的人设描述。
        history: 历史对话记录。
        client: 智谱AI客户端。

    Returns:
        返回角色描述字符串。
    """
    response: StreamResponse = client.chat.completions.create(
        model="charglm-3",
        meta={
            "user_info": user_role,
            "bot_info": bot_role,
            "bot_name": bot_name,
            "user_name": user_name,
        },
        messages=history,
        stream=True,
    )
    for chunk in response:
        yield chunk.choices[0].delta.content
