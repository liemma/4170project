document.addEventListener("DOMContentLoaded", () => {
    const feedback = document.getElementById("feedback");
    const completion = document.getElementById("completion-options");
    const accuracySummary = document.getElementById("accuracy-summary");
    const song = document.getElementById("piano").dataset.song;
  
    const correctSequences = {
      mary_lamb: ["3", "2", "1", "2", "3", "3", "3", "2", "2", "2", "3", "5", "5",
        "3", "2", "1", "2", "3", "3", "3", "3", "2", "2", "3", "2", "1",
        "3", "2", "1", "2", "3", "3", "3", "2", "2", "2", "3", "5", "5",
        "3", "2", "1", "2", "3", "3", "3", "3", "2", "2", "3", "2", "1"
      ],
      happy_birthday: ["5", "5", "6", "5", "8", "7", "5", "5", "6", "5", "9", "8",
        "5", "5", "w", "0", "8", "7", "6", "q", "q", "0", "8", "9", "8"
      ]
    };
  
    const expected = correctSequences[song] || [];
    let index = 0;
    let total = expected.length;
    let mistakes = 0;
  
    const updateFeedback = (text, color) => {
      feedback.textContent = text;
      feedback.style.color = color;
    };
  
    const handleInput = (key) => {
      if (index >= total) return;
      if (key === expected[index]) {
        index++;
        updateFeedback("Correct!", "green");
        if (index === total) {
          updateFeedback("You played the whole song!", "green");
  
          const accuracy = (((total - mistakes) / total) * 100).toFixed(1);
          accuracySummary.innerHTML = `Accuracy: ${accuracy}%<br>Mistakes: ${mistakes}`;
          completion.classList.remove("d-none");
  
          // Save result to backend
          fetch('/store_practice_result', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              song: song,
              accuracy: accuracy,
              incorrect: mistakes
            })
          });
        }
      } else {
        mistakes++;
        updateFeedback("Try again!", "red");
      }
    };
  
    document.addEventListener("keydown", (e) => {
      if (/^[0-9qwerty]$/.test(e.key)) handleInput(e.key);
    });
  });
  