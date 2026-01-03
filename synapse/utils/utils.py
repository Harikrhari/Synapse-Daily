from synapse.utils.logger import get_logger
logger = get_logger(__name__)


def load_prompt(prompt_name):
    logger.info(f"Loading prompt: {prompt_name}")
    with open(f"synapse/prompts/{prompt_name}.txt", 'r', encoding='utf-8') as f:
        prompt = f.read()
    logger.info(f"{prompt_name} Prompt loaded successfully")
    return prompt
