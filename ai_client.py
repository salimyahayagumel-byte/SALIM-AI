"""Local rule-based responses. No external AI service or API key is used."""
import re
import random

HAUSA_RULES = [
    (r"\b(sannu|salamu alaikum|assalamu alaikum|ina kwana|ina wuni|ina yini)\b",
     ["Wa alaikumus salam! Ina nan, zan taimaka maka. Me kake son sani?",
      "Sannu! SALIM AI yana sauraronka. Wace tambaya kake da ita?"]),
    (r"\b(ya kake|yaya kake|lafiya|kana lafiya)\b",
     ["Lafiya lau, na gode. Kai fa, ya kake?",
      "Ina lafiya. Me zan taimaka maka da shi yau?"]),
    (r"\b(wane ne kai|kai wanene|menene sunanka|sunanka)\b",
     ["Ni SALIM AI TERMINAL ne. Ina amfani da amsoshin cikin gida, kuma ba na buƙatar AI API key a wannan sigar."]),
    (r"\b(na gode|nagode|thanks|thank you)\b",
     ["Ba komai! Ina nan idan kana buƙatar taimako.",
      "Babu komai. Ka tambaye ni duk abin da tsarin gida na zai iya amsawa."]),
    (r"\b(sai anjima|sai gobe|bye|goodbye)\b",
     ["Sai anjima! Ka dawo duk lokacin da kake buƙatar taimako."]),
    (r"\b(lokaci|time)\b",
     ["Ba ni da damar duba ainihin agogon na'urarka a wannan sigar. Ka duba agogon wayarka don samun lokaci na yanzu."]),
    (r"\b(taimako|help|me za ka iya|me zaka iya)\b",
     ["Zan iya amsa gaisuwa, taimakawa da umarnin wannan dashboard, da amsa wasu tambayoyin yau da kullum da aka tsara. Ba na samun sabon ilimin intanet kuma ba cikakken AI ba ne."]),
    (r"\b(api key|apikey|gemini|openai)\b",
     ["Wannan sigar SALIM AI tana amfani da amsoshin cikin gida kuma ba ta buƙatar Gemini, OpenAI, ko wani AI API key."]),
    (r"\b(hausa|turanci|english|language)\b",
     ["Za ka iya yin magana da Hausa ko Turanci. Daga maɓallin zaɓin harshe, zaɓi yaren da browser ɗinka zai yi ƙoƙarin gane shi."]),
    (r"\b(waya|termux|render|github|dashboard)\b",
     ["Idan kana gyara aikin SALIM AI, ka fara duba Logs a Render da git status a Termux. Wannan sigar tana ba da amsoshin gida ne kawai; ba ta iya shiga ko sarrafa asusunka kai tsaye."]),
    (r"\b(wanene|menene|me ake nufi)\b",
     ["Zan yi ƙoƙarin taimakawa, amma wannan sigar tana da iyakantaccen ilimi na cikin gida. Ka sake faɗin tambayar a sauƙaƙe ko ka tambaye ni game da amfani da SALIM AI."]),
]

ENGLISH_RULES = [
    (r"\b(hello|hi|hey|good morning|good afternoon|good evening)\b",
     ["Hello! I'm SALIM AI. What can I help you with?",
      "Hi there! I'm listening. Ask me a question."]),
    (r"\b(how are you|are you okay)\b",
     ["I'm running and ready to help. How can I assist you?"]),
    (r"\b(who are you|your name|what are you)\b",
     ["I'm SALIM AI TERMINAL, a local-response assistant. This version does not need an AI API key."]),
    (r"\b(thank you|thanks)\b",
     ["You're welcome!"]),
    (r"\b(help|what can you do)\b",
     ["I can respond to common greetings and a limited set of built-in topics. I do not use an AI API and cannot answer every question or fetch live internet information."]),
    (r"\b(api key|gemini|openai)\b",
     ["This version uses local built-in responses. It does not call Gemini, OpenAI, or another AI API."]),
    (r"\b(bye|goodbye)\b",
     ["Goodbye! Come back whenever you need help."]),
]

def local_reply(message: str, language: str = "ha") -> str:
    clean = re.sub(r"\s+", " ", message.strip().lower())
    if not clean:
        return "Ban ji tambayarka ba. Ka sake magana."
    rules = ENGLISH_RULES + HAUSA_RULES if language.startswith("en") else HAUSA_RULES + ENGLISH_RULES
    for pattern, replies in rules:
        if re.search(pattern, clean, flags=re.IGNORECASE):
            return random.choice(replies)
    if language.startswith("en"):
        return ("I heard you, but I don't have a built-in answer for that yet. "
                "This no-API version uses local rules, not a full AI model. "
                "Try asking for help or asking a common question.")
    return ("Na ji maganarka, amma ba ni da amsar wannan tambayar a cikin amsoshin gida tukuna. "
            "Wannan sigar ba ta amfani da AI API, don haka ba ta iya amsa kowace tambaya. "
            "Ka ce 'taimako' don sanin abubuwan da zan iya yi.")
