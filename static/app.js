(() => {
  const micButton = document.getElementById("mic");
  const stopButton = document.getElementById("stop");
  const micLabel = document.getElementById("mic-label");
  const status = document.getElementById("status");
  const statusLabel = document.getElementById("status-label");
  const statusDot = document.getElementById("status-dot");
  const replyBox = document.getElementById("reply");
  const heardBox = document.getElementById("heard");
  const languageSelect = document.getElementById("language");
  const radar = document.getElementById("radar");

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  let recognition = null;
  let busy = false;

  function setStatus(message, label = "READY", color = "#36d6a0") {
    status.textContent = message;
    statusLabel.textContent = label;
    statusDot.style.background = color;
    statusDot.style.boxShadow = `0 0 12px ${color}`;
  }

  function speak(text) {
    if (!("speechSynthesis" in window)) {
      setStatus("Browser ɗinka ba ya goyon bayan karanta amsa da murya.", "TEXT MODE", "#ffbd68");
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const lang = languageSelect.value;
    utterance.lang = lang;
    utterance.rate = 0.94;
    utterance.pitch = 1;
    utterance.onstart = () => setStatus("SALIM AI yana magana.", "SPEAKING", "#55e8f6");
    utterance.onend = () => setStatus("Na gama amsa. Za ka iya sake magana.", "READY");
    utterance.onerror = () => setStatus("An nuna amsar rubutu; karanta murya bai yiwu ba a wannan browser.", "TEXT MODE", "#ffbd68");
    window.speechSynthesis.speak(utterance);
  }

  async function askLocal(message) {
    busy = true;
    setStatus("Ina shirya amsar cikin gida...", "THINKING", "#55e8f6");
    replyBox.textContent = "Ina tunani...";
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          message,
          language: languageSelect.value.startsWith("en") ? "en" : "ha"
        })
      });
      const data = await response.json();
      if (!response.ok || !data.reply) throw new Error(data.error || "Ba a samu amsa ba.");
      replyBox.textContent = data.reply;
      speak(data.reply);
    } catch (error) {
      const fallback = "Na ji maganarka, amma na kasa samun amsar server. Ka duba haɗin intanet sannan ka sake gwadawa.";
      replyBox.textContent = fallback;
      setStatus("An samu matsalar haɗi da server.", "CONNECTION ERROR", "#ff7474");
      speak(fallback);
    } finally {
      busy = false;
    }
  }

  function startListening() {
    if (!SpeechRecognition) {
      const msg = "Browser ɗinka bai goyi bayan gane magana ba. Ka gwada Chrome na Android, ka tabbatar kana amfani da HTTPS, sannan ka ba shi izinin microphone.";
      replyBox.textContent = msg;
      setStatus("Speech recognition ba ya samuwa a wannan browser.", "NOT SUPPORTED", "#ffbd68");
      return;
    }
    if (busy) return;
    if (!recognition) {
      recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.maxAlternatives = 1;
      recognition.onstart = () => {
        micButton.classList.add("listening");
        micLabel.textContent = "INA SAURARO...";
        stopButton.hidden = false;
        heardBox.hidden = false;
        heardBox.textContent = "Ina sauraronka...";
        setStatus("Yi magana yanzu. Idan ka gama, dakata kaɗan.", "LISTENING", "#ffbd68");
      };
      recognition.onresult = (event) => {
        let interim = "";
        let finalText = "";
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) finalText += transcript;
          else interim += transcript;
        }
        heardBox.textContent = finalText || interim || "Ina sauraro...";
        if (finalText.trim()) {
          recognition._submitted = true;
          askLocal(finalText.trim());
        }
      };
      recognition.onerror = (event) => {
        const messages = {
          "not-allowed": "Ba a ba browser izinin microphone ba. Duba Site settings > Microphone.",
          "service-not-allowed": "An hana speech service. Duba izinin microphone da saitunan browser.",
          "no-speech": "Ban ji magana ba. Ka matsa microphone ka sake magana.",
          "network": "Gane magana ya samu matsalar network; wasu browser suna buƙatar sabis na intanet.",
          "audio-capture": "Ba a sami microphone ba. Rufe sauran apps da ke amfani da shi."
        };
        const message = messages[event.error] || `Matsalar microphone: ${event.error}. Ka sake gwadawa.`;
        replyBox.textContent = message;
        setStatus(message, "MIC ERROR", "#ff7474");
      };
      recognition.onend = () => {
        micButton.classList.remove("listening");
        micLabel.textContent = "TABA KA YI MAGANA";
        stopButton.hidden = true;
        if (!busy && statusLabel.textContent === "LISTENING") {
          setStatus("Sauraro ya tsaya. Taɓa microphone ka sake gwadawa.", "READY");
        }
      };
    }
    try {
      recognition.lang = languageSelect.value;
      recognition._submitted = false;
      recognition.start();
    } catch (_error) {
      setStatus("An riga an fara sauraro. Jira kaɗan ka sake gwadawa.", "WAIT", "#ffbd68");
    }
  }

  micButton.addEventListener("click", startListening);
  stopButton.addEventListener("click", () => {
    if (recognition) recognition.stop();
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden && recognition) {
      try { recognition.stop(); } catch (_) {}
    }
  });

  fetch("/health").then(r => r.json()).then(data => {
    if (data.status === "healthy") setStatus("Tsarin gida yana shirye. Babu buƙatar API key.", "READY");
  }).catch(() => setStatus("Ba a iya haɗawa da server ba.", "OFFLINE", "#ff7474"));
})();
