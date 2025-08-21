from flask import Flask, render_template_string, request

app = Flask(__name__)

# 🧠 Coding-related Questions
questions = [
    {
        "id": 1,
        "question": "What is the output of print(2 ** 3 ** 2)?",
        "options": ["64", "512", "256", "8"],
        "answer": "512"
    },
    {
        "id": 2,
        "question": "Which of the following data structures uses LIFO?",
        "options": ["Queue", "List", "Stack", "Dictionary"],
        "answer": "Stack"
    },
    {
        "id": 3,
        "question": "What is the time complexity of binary search?",
        "options": ["O(n)", "O(n log n)", "O(log n)", "O(1)"],
        "answer": "O(log n)"
    },
    {
        "id": 4,
        "question": "Which keyword is used to create a generator in Python?",
        "options": ["yield", "return", "generator", "defgen"],
        "answer": "yield"
    },
    {
        "id": 5,
        "question": "Which sorting algorithm is the fastest in the average case?",
        "options": ["Bubble Sort", "Merge Sort", "Selection Sort", "Quick Sort"],
        "answer": "Quick Sort"
    }
]

# HTML Template
exam_page = """
<!DOCTYPE html>
<html>
<head><title>Python Coding Exam</title></head>
<body>
    <h2>Python & Programming Concepts Exam</h2>
    <form method="post" action="/submit">
        {% for q in questions %}
            <p><strong>{{ q.id }}. {{ q.question }}</strong></p>
            {% for opt in q.options %}
                <input type="radio" name="q{{ q.id }}" value="{{ opt }}" required> {{ opt }}<br>
            {% endfor %}
        {% endfor %}
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# Result Template
result_page = """
<!DOCTYPE html>
<html>
<head><title>Results</title></head>
<body>
    <h2>Results</h2>
    <p>You scored {{ score }}/{{ total }}</p>
    <ul>
    {% for item in feedback %}
        <li>Q{{ item['id'] }} - Your answer: {{ item['your_answer'] }} | Correct: {{ item['correct_answer'] }}</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def exam():
    return render_template_string(exam_page, questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    total = len(questions)
    feedback = []

    for q in questions:
        selected = request.form.get(f"q{q['id']}")
        if selected == q["answer"]:
            score += 1
        feedback.append({
            "id": q["id"],
            "your_answer": selected,
            "correct_answer": q["answer"]
        })

    return render_template_string(result_page, score=score, total=total, feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)
