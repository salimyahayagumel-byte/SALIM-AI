# SALIM AI V6.0 — Cloud + Android (Termux)

An gina wannan a matsayin mataki na gaba bisa SALIM AI V5.1, ba ya maye gurbin V5.1. Cloud app ɗin yanzu yana amfani da `webapp.py`, `database.py`, da `ai_client.py` kamar V5.1. `android_agent.py` shi ne sabon agent na Android.

## Render
Ci gaba da amfani da service ɗin V5.1 har sai an yi gwajin V6 a sabon service. Kada ka maye gurbin production deployment kai tsaye. `GEMINI_API_KEY` da `GEMINI_MODEL` su kasance a Render Environment.

## Iyaka ta yanzu
Agent ɗin yana da damar aiwatar da allowlisted tasks idan API queue ɗin ya kasance an haɗa shi. Wannan archive bai ƙara task queue endpoints a `webapp.py` ba tukuna, don haka mataki na farko shi ne a duba tsarin agent da Termux. Ba cikakken phone-control release ba ne tukuna. Dole ne a kammala task queue, approval UI, login/auth, da persistent task storage kafin amfani na yau da kullum.

## Tsaro
- Kada ka saka API keys a HTML/JavaScript ko GitHub.
- Kada ka buɗe agent ɗin ga jama'a ba tare da authentication ba.
- Kada ka ba agent unrestricted shell execution.
- Tabbatar da ayyukan da za su iya aika bayanai, kashe kuɗi ko share fayiloli.
