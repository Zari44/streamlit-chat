from shared.chat_config import ChatConfig


def get_system_prompt(config: ChatConfig) -> str:
    audience_prompt = ""
    if config.bot_audience:
        audience_prompt = (
            f"You are a bot that is assistant for '{config.bot_audience}'. You are talking to '{config.bot_audience}'."
        )

    tone_prompt = ""
    if config.bot_tone:
        tone_prompt = f"Your general tone that you speak with is '{config.bot_tone}'."

    system_prompt = f"""
    {audience_prompt}
    {tone_prompt}
    Your aim and the way you MUST behave is {config.bot_aim}
    """
    return system_prompt
