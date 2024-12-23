from google.generativeai.types import HarmCategory, HarmBlockThreshold


tele_token = ''


models_tokens = {
    'gemini': '',
    'chatgpt': '',
    'claude': ''
}


models = [
    'gemini-2.0-flash-exp',
    #'gpt-4o',
    #'claude-3-opus-20240229',
    'gemini-2.0-flash-thinking-exp'
    'gemini-1.5-pro-latest'
]

gemini_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}
