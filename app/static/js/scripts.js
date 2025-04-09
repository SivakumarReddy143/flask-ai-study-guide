document.addEventListener("DOMContentLoaded", function () {
    // Track score
    let totalQuestions = 0;
    let attempted = 0;
    let score = 0;

    const scoreBar = document.getElementById("score-bar");
    const questions = document.querySelectorAll(".question");
    totalQuestions = questions.length;

    questions.forEach(question => {
        const options = question.querySelectorAll(".option");
        const correctAnswer = question.querySelector(".answer-content").innerText.trim();
        let isAnswered = false;

        options.forEach(option => {
            option.addEventListener("click", function () {
                if (isAnswered) return;

                const selectedText = this.innerText.trim();

                // Mark the option
                if (selectedText === correctAnswer) {
                    this.classList.add("correct");
                    score++;
                } else {
                    this.classList.add("incorrect");
                    // Highlight correct one too
                    options.forEach(opt => {
                        if (opt.innerText.trim() === correctAnswer) {
                            opt.classList.add("correct");
                        }
                    });
                }

                // Disable further selection for this question
                options.forEach(opt => opt.classList.add("disabled"));

                attempted++;
                isAnswered = true;

                // Update score display
                if (scoreBar) {
                    scoreBar.textContent = `Attempted: ${attempted} / ${totalQuestions} | Score: ${score}`;
                }
            });
        });

        // Reveal answer button
        const revealBtn = question.querySelector(".reveal-btn");
        if (revealBtn) {
            revealBtn.addEventListener("click", function () {
                const answerSection = question.querySelector(".answer-section");
                if (answerSection) {
                    answerSection.style.display = "block";
                }
                this.disabled = true;
            });
        }
    });

    // Video resources page
    const videoLinks = document.querySelectorAll(".video-link");
    videoLinks.forEach(link => {
        link.addEventListener("click", function () {
            const videoId = this.dataset.videoId;
            const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
            window.open(videoUrl, "_blank");
        });
    });

    // Chatbot form (uncomment if needed)
    // const chatForm = document.getElementById("chat-form");
    // if (chatForm) {
    //     chatForm.addEventListener("submit", function (event) {
    //         event.preventDefault();
    //         const userInput = document.getElementById("user-input").value;
    //         alert("User input sent to chatbot: " + userInput);
    //     });
    // }
});
