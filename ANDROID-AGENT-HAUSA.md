# SALIM AI V6.0 Android Agent (Termux)

Wannan agent yana aiki a matsayin gwajin haɗin cloud da Android. Ba ya sarrafa dukkan waya, kuma ba ya aika saƙonni da kansa. Yana karɓar ayyukan da aka saka cikin queue ta authenticated API. Yana da allowlist: `open_url`, `list_files`, `read_file`, `write_file`, `run_python`. Duk fayiloli suna cikin `SALIM_WORKSPACE` kawai. Kada a gudanar da code daga wanda ba ka yarda da shi ba.

## Shigarwa
1. Ka kiyaye V5.1; wannan sabon folder/repo ne.
2. A Termux:

```sh
pkg update -y
pkg install python termux-api git -y
termux-setup-storage
mkdir -p ~/salim-ai-v6
```

3. Kwafi `android_agent.py` zuwa `~/salim-ai-v6/`, sannan:

```sh
cd ~/salim-ai-v6
python -m pip install requests python-dotenv
cp .env.agent.example .env
nano .env
```

4. Saka URL na Render da `SALIM_AGENT_TOKEN` iri ɗaya da na Render. Kada ka tura `.env` zuwa GitHub.
5. Gudanarwa:

```sh
python android_agent.py
```

## Mahimmanci
Wannan build yana samar da Android agent, amma chat UI na V5.1 bai riga ya haɗa da maɓallan queue na agent ba. Don haka kada ka ɗauka cewa rubuta umarni a chat zai riga ya gudanar da aikin waya. Mataki na gaba shi ne ƙara authenticated task queue da approval UI a cloud sannan a gwada shi. Don persistence na tasks, yi amfani da managed database ko persistent disk; `/tmp` na iya ɓacewa bayan restart.
