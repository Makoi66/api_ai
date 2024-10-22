from google.generativeai.types import HarmCategory, HarmBlockThreshold

whitelist = [
    474066447
]

tele_token = '7032308631:AAHT2LCpKNJ4ckInsmHoFTOzULY5HB5FnzE'


models_tokens = {
    'gemini': 'AIzaSyA8jzw_5Uv1G2ECbOYaxfQvct7j1TFmi_s',
    'chatgpt': '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',
    'claude': ''
}


models = [
    'gemini-1.5-pro-002',
    #'gpt-4o',
    #'claude-3-opus-20240229',
    'gemini-pro-vision'
]

gemini_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}