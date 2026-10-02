/**
 * EduGenie - Frontend JavaScript
 * Handles feature switching, API calls, and dynamic content rendering.
 */

document.addEventListener('DOMContentLoaded', function () {

    // Feature Switching
    const featureBtns = document.querySelectorAll('.feature-btn');
    const featureSections = document.querySelectorAll('.feature-section');

    featureBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const feature = btn.dataset.feature;
            featureBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            featureSections.forEach(section => {
                section.classList.remove('active');
            });
            document.getElementById(`${feature}-section`).classList.add('active');
            hideError();
        });
    });

    // Helper Functions
    function showLoading() {
        document.getElementById('loading').classList.remove('hidden');
    }

    function hideLoading() {
        document.getElementById('loading').classList.add('hidden');
    }

    function showError(message) {
        const errorEl = document.getElementById('error-msg');
        errorEl.textContent = message;
        errorEl.classList.remove('hidden');
    }

    function hideError() {
        document.getElementById('error-msg').classList.add('hidden');
    }

    function showResult(containerId) {
        document.getElementById(containerId).classList.remove('hidden');
    }

    function hideResult(containerId) {
        document.getElementById(containerId).classList.add('hidden');
    }

    function setButtonLoading(btnId, loading) {
        const btn = document.getElementById(btnId);
        if (loading) {
            btn.disabled = true;
            btn.dataset.originalText = btn.textContent;
            btn.textContent = 'Loading...';
        } else {
            btn.disabled = false;
            btn.textContent = btn.dataset.originalText;
        }
    }

    // API Call Helper
    async function apiCall(endpoint, data) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.error || 'Request failed');
            }
            return result;
        } catch (error) {
            if (error.message === 'Failed to fetch') {
                throw new Error('Network error. Please check your connection.');
            }
            throw error;
        }
    }

    // Q&A Feature
    document.getElementById('qa-btn').addEventListener('click', async () => {
        const input = document.getElementById('qa-input').value.trim();
        if (!input) { showError('Please enter a question.'); return; }
        hideError();
        hideResult('qa-result');
        setButtonLoading('qa-btn', true);
        showLoading();
        try {
            const result = await apiCall('/qa', { question: input });
            document.getElementById('qa-output').textContent = result.answer;
            showResult('qa-result');
        } catch (error) {
            showError(error.message || 'Sorry, something went wrong. Please try again.');
        } finally {
            hideLoading();
            setButtonLoading('qa-btn', false);
        }
    });

    // Explain Feature
    document.getElementById('explain-btn').addEventListener('click', async () => {
        const input = document.getElementById('explain-input').value.trim();
        if (!input) { showError('Please enter a topic to explain.'); return; }
        hideError();
        hideResult('explain-result');
        setButtonLoading('explain-btn', true);
        showLoading();
        try {
            const result = await apiCall('/explain', { text: input });
            document.getElementById('explain-output').textContent = result.explanation;
            showResult('explain-result');
        } catch (error) {
            showError(error.message || 'Sorry, something went wrong. Please try again.');
        } finally {
            hideLoading();
            setButtonLoading('explain-btn', false);
        }
    });

    // Quiz Feature
    document.getElementById('quiz-btn').addEventListener('click', async () => {
        const input = document.getElementById('quiz-input').value.trim();
        if (!input) { showError('Please enter a topic or passage for the quiz.'); return; }
        hideError();
        hideResult('quiz-result');
        setButtonLoading('quiz-btn', true);
        showLoading();
        try {
            const result = await apiCall('/quiz', { text: input });
            if (result.error) { showError(result.error); return; }
            renderQuiz(result.quiz);
            showResult('quiz-result');
        } catch (error) {
            showError(error.message || 'Sorry, something went wrong. Please try again.');
        } finally {
            hideLoading();
            setButtonLoading('quiz-btn', false);
        }
    });

    function renderQuiz(quizData) {
        const container = document.getElementById('quiz-output');
        container.innerHTML = '';
        quizData.forEach((q, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'quiz-question';
            const questionTitle = document.createElement('h4');
            questionTitle.textContent = `Q${index + 1}: ${q.question}`;
            questionDiv.appendChild(questionTitle);
            const optionsDiv = document.createElement('div');
            optionsDiv.className = 'quiz-options';
            q.options.forEach((option, optIndex) => {
                const optionBtn = document.createElement('button');
                optionBtn.className = 'quiz-option';
                optionBtn.textContent = `${String.fromCharCode(65 + optIndex)}. ${option}`;
                optionBtn.dataset.option = option;
                optionBtn.dataset.correct = q.correct_answer;
                optionBtn.dataset.explanation = q.explanation;
                optionBtn.addEventListener('click', function () {
                    handleAnswerClick(this, optionsDiv);
                });
                optionsDiv.appendChild(optionBtn);
            });
            questionDiv.appendChild(optionsDiv);
            container.appendChild(questionDiv);
        });
    }

    function handleAnswerClick(selectedBtn, optionsContainer) {
        const allOptions = optionsContainer.querySelectorAll('.quiz-option');
        allOptions.forEach(opt => {
            opt.classList.remove('selected');
            opt.disabled = true;
        });
        selectedBtn.classList.add('selected');
        const selectedAnswer = selectedBtn.dataset.option;
        const correctAnswer = selectedBtn.dataset.correct;
        const explanation = selectedBtn.dataset.explanation;
        allOptions.forEach(opt => {
            if (opt.dataset.option === correctAnswer) {
                opt.classList.add('correct');
            } else if (opt === selectedBtn && selectedAnswer !== correctAnswer) {
                opt.classList.add('incorrect');
            }
        });
        const explanationDiv = document.createElement('div');
        explanationDiv.className = 'quiz-explanation';
        const isCorrect = selectedAnswer === correctAnswer;
        const icon = isCorrect ? '✓' : '✗';
        const status = isCorrect ? 'Correct!' : 'Incorrect!';
        explanationDiv.innerHTML = `
            <strong>${icon} ${status}</strong><br>
            <strong>Correct Answer:</strong> ${correctAnswer}<br>
            <strong>Explanation:</strong> ${explanation}
        `;
        selectedBtn.parentElement.parentElement.appendChild(explanationDiv);
    }

    // Summarize Feature
    document.getElementById('summarize-btn').addEventListener('click', async () => {
        const input = document.getElementById('summarize-input').value.trim();
        if (!input) { showError('Please enter text to summarize.'); return; }
        hideError();
        hideResult('summarize-result');
        setButtonLoading('summarize-btn', true);
        showLoading();
        try {
            const result = await apiCall('/summarize', { text: input });
            document.getElementById('summarize-output').textContent = result.summary;
            showResult('summarize-result');
        } catch (error) {
            showError(error.message || 'Sorry, something went wrong. Please try again.');
        } finally {
            hideLoading();
            setButtonLoading('summarize-btn', false);
        }
    });

    // Learning Path Feature
    document.getElementById('learn-btn').addEventListener('click', async () => {
        const input = document.getElementById('learn-input').value.trim();
        if (!input) { showError('Please enter a topic to create a learning path.'); return; }
        hideError();
        hideResult('learn-result');
        setButtonLoading('learn-btn', true);
        showLoading();
        try {
            const result = await apiCall('/learn/recommendations', { text: input });
            document.getElementById('learn-output').textContent = result.roadmap;
            showResult('learn-result');
        } catch (error) {
            showError(error.message || 'Sorry, something went wrong. Please try again.');
        } finally {
            hideLoading();
            setButtonLoading('learn-btn', false);
        }
    });

    // Enter Key Support
    document.getElementById('qa-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') document.getElementById('qa-btn').click();
    });
    document.getElementById('explain-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') document.getElementById('explain-btn').click();
    });
    document.getElementById('quiz-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') document.getElementById('quiz-btn').click();
    });
    document.getElementById('learn-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') document.getElementById('learn-btn').click();
    });
});
