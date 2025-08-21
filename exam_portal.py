import threading
from flask import Flask, render_template_string, request, redirect, session
from facemonitor import start_exam_monitoring
from monitor_flag import MonitorFlags

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Registered users
users = {'siri': '123', 'varsha': '1234'}

# Questions data
questions = [
    {"id": 1, "question": "What is the output of print(2 ** 3 ** 2)?", "options": ["64", "512", "256", "8"], "answer": "512"},
    {"id": 2, "question": "Which of the following data structures uses LIFO?", "options": ["Queue", "List", "Stack", "Dictionary"], "answer": "Stack"},
    {"id": 3, "question": "What is the time complexity of binary search?", "options": ["O(n)", "O(n log n)", "O(log n)", "O(1)"], "answer": "O(log n)"},
    {"id": 4, "question": "Which keyword is used to create a generator in Python?", "options": ["yield", "return", "generator", "defgen"], "answer": "yield"},
    {"id": 5, "question": "Which sorting algorithm is the fastest in the average case?", "options": ["Bubble Sort", "Merge Sort", "Selection Sort", "Quick Sort"], "answer": "Quick Sort"}
]

# ---------------- Templates ----------------

login_page = """
<!DOCTYPE html><html><head><title>Login</title></head><body>
<h2>Student Login</h2>
<form method="post" action="/login">
Username: <input type="text" name="username" required><br><br>
Password: <input type="password" name="password" required><br><br>
<input type="submit" value="Login">
</form>
{% if error %}<p style="color: red;">{{ error }}</p>{% endif %}
</body></html>
"""

exam_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Coding Exam</title>
    <script>
    document.addEventListener("visibilitychange", function () {
        if (document.hidden) {
            alert("⚠️ Exam terminated: Tab switch or window minimized.");
            window.location.href = "/terminated";
        }
    });
    </script>
</head>
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

result_page = """
<!DOCTYPE html><html><head><title>Results</title></head><body>
<h2>Results for {{ username }}</h2>
<p>You scored {{ score }}/{{ total }}</p>
<ul>
{% for item in feedback %}
<li>Q{{ item['id'] }} - Your answer: {{ item['your_answer'] }} | Correct: {{ item['correct_answer'] }}</li>
{% endfor %}
</ul>
</body></html>
"""

# ---------------- Routes ----------------

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname] == pwd:
            session['user'] = uname
            MonitorFlags.terminate_exam = False
            print(f"✅ {uname} logged in. Monitoring flag reset.")
            return redirect('/exam')
        else:
            error = 'Invalid credentials'
    return render_template_string(login_page, error=error)

@app.route('/exam')
def exam():
    if 'user' not in session:
        return redirect('/login')

    MonitorFlags.terminate_exam = False
    print(f"🧠 [Flask] Starting exam for {session['user']}...")

    def safe_monitor():
        try:
            print("🎯 [Thread] Calling start_exam_monitoring()")
            start_exam_monitoring()
            print("✅ [Thread] Monitoring thread ended.")
        except Exception as e:
            print(f"💥 [Thread Error] {e}")

    threading.Thread(target=safe_monitor, daemon=True).start()
    return render_template_string(exam_page, questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    if 'user' not in session:
        return redirect('/login')

    if MonitorFlags.terminate_exam:
        print("🚨 Submission blocked due to violation.")
        return redirect('/terminated')

    score = 0
    feedback = []
    for q in questions:
        selected = request.form.get(f"q{q['id']}")
        if selected == q['answer']:
            score += 1
        feedback.append({
            "id": q['id'],
            "your_answer": selected,
            "correct_answer": q['answer']
        })

    print(f"✅ {session['user']} completed exam. Score: {score}/{len(questions)}")
    return render_template_string(result_page, username=session['user'], score=score, total=len(questions), feedback=feedback)

@app.route('/terminated')
def terminated():
    print("❌ Exam terminated due to violation.")
    MonitorFlags.terminate_exam = False
    return "<h2>🚫 Exam terminated: Policy violation detected (multiple faces or tab switch).</h2>"

# ---------------- Launch App ----------------

if __name__ == '__main__':
    app.run(debug=True)
