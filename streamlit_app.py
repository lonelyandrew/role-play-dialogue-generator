from typing import Iterable

import streamlit as st
from zhipuai import ZhipuAI

from config import Config
from dialogue_generator.dialogue_generator import generate_role_play_dialogue
from dialogue_generator.role_generator import generate_role_description

config: Config = Config()

client: ZhipuAI = ZhipuAI(api_key=config.api_key)
st.set_page_config(page_title="对话数据生成工具")
st.title("对话数据生成工具")

role_generator_tab, dialogue_generator_tab = st.tabs(["角色人设生成", "对话生成"])


with role_generator_tab:
    role_name: str | None = st.text_input("请输入角色名", max_chars=10)
    text: str | None = st.text_area("请输入角色文本", height=300, help="最大有效长度为100个字符")
    model_name: str = st.selectbox(
        "请选择模型",
        options=["glm-4-0520", "glm-4", "glm-4-air", "glm-4-airx", "glm-4-flash", "glm-3-turbo"],
        index=0,
    )

    if st.button("生成角色人设"):
        if not role_name:
            st.error("请输入角色名")
            st.stop()
        if not text:
            st.error("请输入角色文本")
            st.stop()
        with st.container(border=True):
            role_description_iterator: Iterable[str] = generate_role_description(role_name, text, client, model_name)
            st.write_stream(role_description_iterator)


with dialogue_generator_tab:
    name_x: str = st.text_input("请输入角色1的名称", max_chars=10)
    role_x: str = st.text_area("请输入角色1的人设", height=100)
    name_y: str = st.text_input("请输入角色2的名称", max_chars=10)
    role_y: str = st.text_area("请输入角色2的人设", height=100)
    round_num: int = st.number_input("请输入对话轮数", max_value=20, min_value=1, value=10)

    if st.button("生成对话"):
        if not name_x:
            st.error("请输入角色1的名称")
        if not name_y:
            st.error("请输入角色2的名称")
        if not role_x:
            st.error("请输入角色1的人设")
        if not role_y:
            st.error("请输入角色2的人设")
        if not name_x or not name_y or not role_x or not role_y:
            st.stop()

        with st.container(border=True):
            history: list[dict[str, str]] = [
                {"role": name_x, "content": f"我是{name_x}"},
                {"role": name_y, "content": f"你好{name_x}, 我是{name_y}"},
            ]
            for message in history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            for _ in range(round_num):
                current_user: str = name_x if history[-1]["role"] == name_x else name_y
                current_bot: str = name_x if history[-1]["role"] != name_x else name_y
                current_history: list[dict[str, str]] = [
                    {"role": "user" if current_user == x["role"] else "assistant", "content": x["content"]}
                    for x in history
                ]
                with st.chat_message(current_bot):
                    response_message: Iterable[str] = generate_role_play_dialogue(
                        current_bot,
                        role_x if current_bot == name_x else role_y,
                        current_user,
                        role_x if current_user == name_x else role_y,
                        current_history,
                        client,
                    )
                    response = st.write_stream(response_message)
                    role_message: dict[str, str] = {
                        "role": current_bot,
                        "content": response,
                    }
                    history.append(role_message)
