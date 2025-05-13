document.addEventListener("DOMContentLoaded", function () {
    const piano = document.getElementById("piano");
    if (!piano) return;
  
    const whiteKeys = [
      { note: 'C4', key: '1' },
      { note: 'D4', key: '2' },
      { note: 'E4', key: '3' },
      { note: 'F4', key: '4' },
      { note: 'G4', key: '5' },
      { note: 'A4', key: '6' },
      { note: 'B4', key: '7' },
      { note: 'C5', key: '8' },
      { note: 'D5', key: '9' },
      { note: 'E5', key: '0' },
      { note: 'F5', key: 'q' },
      { note: 'G5', key: 'w' }
    ];
  
    const blackKeyMap = {
      0: 'C#',
      1: 'D#',
      3: 'F#',
      4: 'G#',
      5: 'A#',
      7: 'C#',
      8: 'D#',
      10: 'F#'
    };
  
    const keyWidth = 40;
  
    whiteKeys.forEach(({ note, key }, index) => {
      const whiteKey = document.createElement("div");
      whiteKey.className = "white-key";
      whiteKey.dataset.note = note;
      whiteKey.dataset.key = key;
      whiteKey.innerHTML = `${note[0]}<br><small>${key}</small>`;
      whiteKey.addEventListener("click", () => {
        playNote(note);
        whiteKey.classList.add("pressed");
        setTimeout(() => whiteKey.classList.remove("pressed"), 150);

        // 🔥 Quiz feedback
        const checkAnswer = window.checkAnswer;
        if (typeof checkAnswer === "function") {
          checkAnswer(note);  // send the clicked note to the quiz function
        }
      });
      piano.appendChild(whiteKey);
  
      if (blackKeyMap[index] !== undefined) {
        const blackKey = document.createElement("div");
        blackKey.className = "black-key";
        blackKey.style.left = `${index * keyWidth + keyWidth - 12.5}px`;
        piano.appendChild(blackKey);
      }
    });
  
    const keyMap = Object.fromEntries(whiteKeys.map(k => [k.key, k.note]));
    const whiteKeyEls = document.querySelectorAll(".white-key");
  
    function playNote(note) {
      const audio = new Audio(`/static/sounds/${note}.mp3`);
      audio.play();
    }
  
    document.addEventListener("keydown", (e) => {
      const note = keyMap[e.key];
      const keyEl = Array.from(whiteKeyEls).find(el => el.dataset.key === e.key);
      if (note && keyEl) {
        playNote(note);
        keyEl.classList.add("pressed");
        setTimeout(() => keyEl.classList.remove("pressed"), 150);
      }
    });
  });
  