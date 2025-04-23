document.addEventListener("DOMContentLoaded", function () {
    let currentQuestionIndex = 0;
    let quizData = [];

    function loadQuestion(index) {
        const questionContainer = document.getElementById("question");
        const imageContainer = document.getElementById("question-image");
        const choicesContainer = document.getElementById("choices");

        const question = quizData[index];
        questionContainer.textContent = question.question;
        imageContainer.src = "static/images/" + question.image;

        choicesContainer.innerHTML = "";
        question.choices.forEach(choice => {
            const button = document.createElement("button");
            button.textContent = choice;
            button.className = "choice-btn";
            button.addEventListener("click", () => {
                alert(choice === question.correct ? "Correct!" : "Try again!");
                if (currentQuestionIndex < quizData.length - 1) {
                    currentQuestionIndex++;
                    loadQuestion(currentQuestionIndex);
                } else {
                    alert("Quiz complete!");
                }
            });
            choicesContainer.appendChild(button);
        });
    }

    fetch("static/quiz_data.json")
        .then(response => response.json())
        .then(data => {
            quizData = data;
            loadQuestion(currentQuestionIndex);
        })
        .catch(error => {
            console.error("Failed to load quiz data:", error);
        });
});
