from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import sqlite3
import os
import random
import copy
import secrets
from datetime import datetime, timedelta
from data_loader import (
    LANGUAGES,
    LEVELS,
    LANGUAGE_LABELS,
    load_quiz,
    load_quiz_catalog,
    get_quiz_by_id,
    get_question_by_index,
    get_challenges_by_language_and_level,
    get_challenge,
    get_language_label,
    get_randomized_quiz,
    get_randomized_quiz_by_id,
    shuffle_options,
)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['DATABASE'] = os.getenv('DATABASE', 'codemcq.db')

# Email configuration for password reset
EMAIL_USER = os.getenv('EMAIL_USER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
PASSWORD_RESET_EXPIRY_MINUTES = int(os.getenv('PASSWORD_RESET_EXPIRY_MINUTES', '15'))


@app.context_processor
def inject_language_labels():
    return {
        'language_labels': LANGUAGE_LABELS,
        'get_language_label': get_language_label
    }

# Initialize database
def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        reset_token TEXT,
        reset_token_expires TIMESTAMP
    )''')
    
    # Add reset_token columns if they don't exist (migration)
    try:
        c.execute('PRAGMA table_info(users)')
        columns = [column[1] for column in c.fetchall()]
        if 'reset_token' not in columns:
            c.execute('ALTER TABLE users ADD COLUMN reset_token TEXT')
        if 'reset_token_expires' not in columns:
            c.execute('ALTER TABLE users ADD COLUMN reset_token_expires TIMESTAMP')
    except Exception as e:
        print(f"Migration warning: {e}")
    
    # Attempts table
    c.execute('''CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        quiz_id TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        total_correct INTEGER DEFAULT 0,
        total_wrong INTEGER DEFAULT 0,
        total_unanswered INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Attempt answers table
    c.execute('''CREATE TABLE IF NOT EXISTS attempt_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt_id INTEGER NOT NULL,
        quiz_id TEXT NOT NULL,
        question_id INTEGER NOT NULL,
        selected_option_id TEXT,
        is_correct INTEGER DEFAULT 0,
        FOREIGN KEY (attempt_id) REFERENCES attempts (id)
    )''')
    
    # Coding submissions table
    c.execute('''CREATE TABLE IF NOT EXISTS coding_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        challenge_id TEXT NOT NULL,
        code TEXT,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def set_user_session(user):
    """Log the user into the current session."""
    session['user_id'] = user['id']
    session['user_name'] = user['name']
    session['user_email'] = user['email']


def parse_db_timestamp(value):
    """Best-effort conversion from SQLite stored timestamp to datetime"""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    return None


def parse_quiz_identifier(quiz_id):
    """Return (language, level) tuple from quiz identifier."""
    if not quiz_id or '_' not in quiz_id:
        return None, None
    return quiz_id.rsplit('_', 1)

def require_login(f):
    """Decorator to require login"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes
@app.route('/')
def index():
    """Landing page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not name or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('signup.html', name=name, email=email)
        
        if len(password) <= 8:
            flash('Password must be at least 8 or long characters long.', 'error')
            return render_template('signup.html', name=name, email=email)
        
        conn = get_db()
        c = conn.cursor()
        
        # Check if email already exists
        c.execute('SELECT id FROM users WHERE email = ?', (email,))
        if c.fetchone():
            conn.close()
            flash('Email already registered. Please login.', 'error')
            return render_template('signup.html', name=name, email=email)
        
        # Create new user with email automatically verified
        password_hash = generate_password_hash(password)
        c.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
                  (name, email, password_hash))
        user_id = c.lastrowid
        conn.commit()
        conn.close()
        
        # Fetch the newly created user and log them in
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, name, email FROM users WHERE id = ?', (user_id,))
        user = c.fetchone()
        conn.close()
        
        set_user_session(user)
        flash('Account created successfully! You are now logged in.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html', email=email)
        
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, name, email, password_hash FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            set_user_session(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return render_template('login.html', email=email)
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password - user enters email to get reset link"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Email is required.', 'error')
            return render_template('forgot_password.html')
        
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, name, email FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        
        if user:
            # Generate a secure token
            reset_token = secrets.token_urlsafe(32)
            reset_expiry = datetime.now() + timedelta(minutes=PASSWORD_RESET_EXPIRY_MINUTES)
            
            c.execute('UPDATE users SET reset_token = ?, reset_token_expires = ? WHERE id = ?',
                     (reset_token, reset_expiry.isoformat(), user['id']))
            conn.commit()
            conn.close()
            
            # Redirect to reset password page with token
            flash('Password reset link has been sent. Enter your new password below.', 'success')
            return redirect(url_for('reset_password', token=reset_token))
        else:
            # Don't reveal whether email exists for security
            flash('If an account exists with that email, you will receive a reset link.', 'info')
            conn.close()
            return render_template('forgot_password.html')
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password using token"""
    if request.method == 'GET':
        # Validate token exists and is not expired
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, email FROM users WHERE reset_token = ? AND reset_token_expires > ?',
                 (token, datetime.now().isoformat()))
        user = c.fetchone()
        conn.close()
        
        if not user:
            flash('Invalid or expired reset link.', 'error')
            return redirect(url_for('login'))
        
        return render_template('reset_password.html', token=token)
    
    elif request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not password or not confirm_password:
            flash('Both password fields are required.', 'error')
            return render_template('reset_password.html', token=token)
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html', token=token)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('reset_password.html', token=token)
        
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, email FROM users WHERE reset_token = ? AND reset_token_expires > ?',
                 (token, datetime.now().isoformat()))
        user = c.fetchone()
        
        if not user:
            flash('Invalid or expired reset link.', 'error')
            conn.close()
            return redirect(url_for('login'))
        
        # Update password and clear reset token
        password_hash = generate_password_hash(password)
        c.execute('UPDATE users SET password_hash = ?, reset_token = NULL, reset_token_expires = NULL WHERE id = ?',
                 (password_hash, user['id']))
        conn.commit()
        conn.close()
        
        flash('Password has been reset successfully! Please login with your new password.', 'success')
        return redirect(url_for('login'))

@app.route('/dashboard')
@require_login
def dashboard():
    """User dashboard"""
    conn = get_db()
    c = conn.cursor()
    
    # Get user stats
    c.execute('''
        SELECT 
            COUNT(*) as total_attempts,
            MAX(score) as best_score,
            AVG(score) as avg_score
        FROM attempts
        WHERE user_id = ?
    ''', (session['user_id'],))
    stats = c.fetchone()
    
    # Get recent attempts
    c.execute('''
        SELECT a.*
        FROM attempts a
        WHERE a.user_id = ?
        ORDER BY COALESCE(a.completed_at, a.started_at) DESC
        LIMIT 5
    ''', (session['user_id'],))
    recent_attempts = c.fetchall()
    
    conn.close()
    
    # Get quiz titles from JSON
    quiz_catalog = load_quiz_catalog()
    quiz_titles = {q['id']: q['title'] for q in quiz_catalog}
    
    # Update recent attempts with proper titles
    attempts_list = []
    for attempt in recent_attempts:
        attempt_dict = dict(attempt)
        attempt_dict['quiz_title'] = quiz_titles.get(attempt_dict['quiz_id'], attempt_dict['quiz_id'])
        attempts_list.append(attempt_dict)
    
    return render_template('dashboard.html',
                         stats=stats,
                         recent_attempts=attempts_list,
                         user_name=session['user_name'],
                         quiz_catalog=quiz_catalog)

@app.route('/quiz/list')
@require_login
def quiz_list():
    """Legacy route - redirect to new selection page"""
    return redirect(url_for('quiz_select'))


@app.route('/quiz/select', methods=['GET', 'POST'])
@require_login
def quiz_select():
    """Interactive quiz selection by language and level."""
    if request.method == 'POST':
        language = request.form.get('language', '').lower()
        level = request.form.get('level', '').lower()
        if language not in LANGUAGES or level not in LEVELS:
            flash('Please choose a valid language and level.', 'error')
            return redirect(url_for('quiz_select'))
        return redirect(url_for('quiz_start', language=language, level=level))

    selected_language = request.args.get('language', '').lower()
    if selected_language and selected_language not in LANGUAGES:
        selected_language = ''

    selected_level = request.args.get('level', '').lower()
    if selected_level and selected_level not in LEVELS:
        selected_level = ''

    selected_quiz = None
    if selected_language and selected_level:
        selected_quiz = load_quiz(selected_language, selected_level)
    quiz_catalog = load_quiz_catalog()

    return render_template(
        'quiz_select.html',
        languages=LANGUAGES,
        levels=LEVELS,
        selected_language=selected_language,
        selected_level=selected_level,
        selected_quiz=selected_quiz,
        quiz_catalog=quiz_catalog
    )

@app.route('/quiz/start/<language>/<level>')
@require_login
def quiz_start(language, level):
    """Start a quiz - create attempt with randomized questions"""
    language = language.lower()
    level = level.lower()
    if language not in LANGUAGES or level not in LEVELS:
        flash('Invalid quiz selection.', 'error')
        return redirect(url_for('quiz_select'))

    # Load quiz with randomized questions and options
    quiz = get_randomized_quiz(language, level)
    if not quiz:
        flash(f'Quiz not found for {language} - {level}. Please check available options.', 'error')
        return redirect(url_for('quiz_select'))

    # Use quiz_id from loaded quiz (e.g., 'js_easy' from JSON)
    quiz_id = quiz.get('quiz_id')
    if not quiz_id:
        flash('Invalid quiz configuration.', 'error')
        return redirect(url_for('quiz_select'))
    
    conn = get_db()
    c = conn.cursor()
    
    # Create new attempt with randomized questions
    # Store the randomized quiz in session for the duration of this attempt
    session[f'quiz_attempt_questions_{quiz_id}'] = quiz.get('questions', [])
    
    # Create new attempt record
    c.execute('''
        INSERT INTO attempts (user_id, quiz_id, started_at)
        VALUES (?, ?, ?)
    ''', (session['user_id'], quiz_id, datetime.now()))
    attempt_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return redirect(url_for('quiz_question', attempt_id=attempt_id, q_no=0))

@app.route('/quiz/question/<int:attempt_id>/<int:q_no>', methods=['GET', 'POST'])
@require_login
def quiz_question(attempt_id, q_no):
    """Display and handle quiz question with randomized options"""
    conn = get_db()
    c = conn.cursor()
    
    # Verify attempt belongs to user
    c.execute('SELECT * FROM attempts WHERE id = ? AND user_id = ?', (attempt_id, session['user_id']))
    attempt = c.fetchone()
    if not attempt:
        conn.close()
        flash('Attempt not found.', 'error')
        return redirect(url_for('quiz_select'))
    
    # Get non-randomized quiz for metadata and to fetch questions if needed
    # Use quiz_id from attempt which could be 'js_easy' or 'javascript_easy'
    quiz_id = attempt['quiz_id']
    quiz_orig = get_quiz_by_id(quiz_id)
    if not quiz_orig:
        conn.close()
        flash(f'Quiz not found for {quiz_id}.', 'error')
        return redirect(url_for('quiz_select'))
    
    quiz_identifier = quiz_orig.get('quiz_id') or attempt['quiz_id']
    
    # Try to get randomized questions from session
    session_key = f'quiz_attempt_questions_{attempt["quiz_id"]}'
    if session_key in session:
        questions = session[session_key]
    else:
        # Fallback: reload and randomize if session was lost
        quiz_randomized = get_randomized_quiz_by_id(attempt['quiz_id'])
        if quiz_randomized:
            questions = quiz_randomized.get('questions', [])
            session[session_key] = questions
        else:
            questions = quiz_orig.get('questions', [])
    
    total_questions = len(questions)
    
    if q_no < 0 or q_no >= total_questions:
        conn.close()
        return redirect(url_for('quiz_submit', attempt_id=attempt_id))
    
    question = questions[q_no] if q_no < len(questions) else None
    if not question:
        conn.close()
        return redirect(url_for('quiz_submit', attempt_id=attempt_id))
    
    # Handle POST (save answer)
    if request.method == 'POST':
        selected_option = request.form.get('option')
        
        # Check if answer already exists
        c.execute('''
            SELECT id FROM attempt_answers
            WHERE attempt_id = ? AND question_id = ?
        ''', (attempt_id, question['id']))
        existing = c.fetchone()
        
        # Find correct option
        correct_option = None
        for opt in question['options']:
            if opt['is_correct']:
                correct_option = opt['id']
                break
        
        is_correct = 1 if selected_option == correct_option else 0
        
        if existing:
            # Update existing answer
            c.execute('''
                UPDATE attempt_answers
                SET selected_option_id = ?, is_correct = ?
                WHERE attempt_id = ? AND question_id = ?
            ''', (selected_option, is_correct, attempt_id, question['id']))
        else:
            # Insert new answer
            c.execute('''
                INSERT INTO attempt_answers (attempt_id, quiz_id, question_id, selected_option_id, is_correct)
                VALUES (?, ?, ?, ?, ?)
            ''', (attempt_id, quiz_identifier, question['id'], selected_option, is_correct))
        
        conn.commit()
        
        # Redirect to next question or submit
        if q_no + 1 < total_questions:
            conn.close()
            return redirect(url_for('quiz_question', attempt_id=attempt_id, q_no=q_no + 1))
        else:
            conn.close()
            return redirect(url_for('quiz_submit', attempt_id=attempt_id))
    
    # Get saved answer for this question
    c.execute('''
        SELECT selected_option_id FROM attempt_answers
        WHERE attempt_id = ? AND question_id = ?
    ''', (attempt_id, question['id']))
    saved_answer = c.fetchone()
    selected_option = saved_answer['selected_option_id'] if saved_answer else None
    
    # Calculate time remaining
    duration = timedelta(minutes=quiz_orig.get('duration_minutes', 15))
    started_at = datetime.fromisoformat(attempt['started_at']) if isinstance(attempt['started_at'], str) else attempt['started_at']
    elapsed = datetime.now() - started_at
    remaining = duration - elapsed
    seconds_remaining = max(0, int(remaining.total_seconds()))
    
    conn.close()
    
    # Prepare quiz object with randomized questions for template
    quiz_display = copy.deepcopy(quiz_orig)
    quiz_display['questions'] = questions
    
    return render_template('quiz_question.html',
                         quiz=quiz_display,
                         question=question,
                         q_no=q_no,
                         total_questions=total_questions,
                         attempt_id=attempt_id,
                         selected_option=selected_option,
                         seconds_remaining=seconds_remaining)

@app.route('/quiz/submit/<int:attempt_id>')
@require_login
def quiz_submit(attempt_id):
    """Submit quiz and calculate results"""
    conn = get_db()
    c = conn.cursor()
    
    # Verify attempt
    c.execute('SELECT * FROM attempts WHERE id = ? AND user_id = ?', (attempt_id, session['user_id']))
    attempt = c.fetchone()
    if not attempt:
        conn.close()
        flash('Attempt not found.', 'error')
        return redirect(url_for('quiz_select'))
    
    # If already completed, redirect to results
    if attempt['completed_at']:
        conn.close()
        return redirect(url_for('result', attempt_id=attempt_id))
    
    # Get randomized questions from session
    quiz_orig = get_quiz_by_id(attempt['quiz_id'])
    if not quiz_orig:
        conn.close()
        flash('Quiz not found.', 'error')
        return redirect(url_for('quiz_select'))
    
    session_key = f'quiz_attempt_questions_{attempt["quiz_id"]}'
    if session_key in session:
        questions = session[session_key]
    else:
        # Fallback: use original questions
        questions = quiz_orig.get('questions', [])
    
    # Calculate score
    total_questions = len(questions)
    correct = 0
    wrong = 0
    unanswered = 0
    
    for question in questions:
        c.execute('''
            SELECT selected_option_id, is_correct FROM attempt_answers
            WHERE attempt_id = ? AND question_id = ?
        ''', (attempt_id, question['id']))
        answer = c.fetchone()
        
        if not answer or not answer['selected_option_id']:
            unanswered += 1
        elif answer['is_correct']:
            correct += 1
        else:
            wrong += 1
    
    score = correct
    total_correct = correct
    total_wrong = wrong
    total_unanswered = unanswered
    
    # Update attempt
    c.execute('''
        UPDATE attempts
        SET score = ?, completed_at = ?, total_correct = ?, total_wrong = ?, total_unanswered = ?
        WHERE id = ?
    ''', (score, datetime.now(), total_correct, total_wrong, total_unanswered, attempt_id))
    
    conn.commit()
    conn.close()
    
    # Clean up session data for this attempt
    session.pop(session_key, None)
    
    return redirect(url_for('result', attempt_id=attempt_id))

@app.route('/result/<int:attempt_id>')
@require_login
def result(attempt_id):
    """Display quiz results"""
    conn = get_db()
    c = conn.cursor()
    
    # Get attempt
    c.execute('SELECT * FROM attempts WHERE id = ? AND user_id = ?', (attempt_id, session['user_id']))
    attempt = c.fetchone()
    if not attempt:
        conn.close()
        flash('Attempt not found.', 'error')
        return redirect(url_for('quiz_select'))
    
    quiz = get_quiz_by_id(attempt['quiz_id'])
    if not quiz:
        conn.close()
        flash('Quiz not found.', 'error')
        return redirect(url_for('quiz_select'))
    
    # Try to get randomized questions from session
    session_key = f'quiz_attempt_questions_{attempt["quiz_id"]}'
    if session_key in session:
        questions = session[session_key]
    else:
        # Fallback: use original questions (session may have expired)
        questions = quiz.get('questions', [])
    
    # Get all answers
    results = []
    
    for question in questions:
        c.execute('''
            SELECT selected_option_id, is_correct FROM attempt_answers
            WHERE attempt_id = ? AND question_id = ?
        ''', (attempt_id, question['id']))
        answer = c.fetchone()
        
        selected_option_id = answer['selected_option_id'] if answer else None
        selected_option_text = None
        correct_option_id = None
        correct_option_text = None
        
        # Find option text for selected and correct answers
        for opt in question['options']:
            if opt['id'] == selected_option_id:
                selected_option_text = opt.get('text', '')
            if opt['is_correct']:
                correct_option_id = opt['id']
                correct_option_text = opt.get('text', '')
        
        results.append({
            'question': question,
            'selected_option_id': selected_option_id,
            'selected_option_text': selected_option_text,
            'correct_option_id': correct_option_id,
            'correct_option_text': correct_option_text,
            'is_correct': answer['is_correct'] if answer else False
        })
    
    conn.close()
    
    # Prepare quiz object with randomized questions
    quiz_display = copy.deepcopy(quiz)
    quiz_display['questions'] = questions
    
    return render_template('result.html',
                         attempt=dict(attempt),
                         quiz=quiz_display,
                         results=results)

@app.route('/coding/list')
@require_login
def coding_list():
    """List coding challenges with language/level filters"""
    selected_language = request.args.get('language', '').lower() or None
    if selected_language and selected_language not in LANGUAGES:
        selected_language = None

    selected_level = request.args.get('level', '').lower() or None
    if selected_level and selected_level not in LEVELS:
        selected_level = None

    challenges = get_challenges_by_language_and_level(selected_language, selected_level)

    return render_template(
        'coding_list.html',
        challenges=challenges,
        languages=LANGUAGES,
        levels=LEVELS,
        selected_language=selected_language,
        selected_level=selected_level
    )

@app.route('/coding/start/<challenge_id>')
@require_login
def coding_start(challenge_id):
    """Start a coding challenge"""
    challenge = get_challenge(challenge_id)
    if not challenge:
        flash('Challenge not found.', 'error')
        return redirect(url_for('coding_list'))
    
    return render_template('coding_challenge.html', challenge=challenge)

@app.route('/coding/submit', methods=['POST'])
@require_login
def coding_submit():
    """Submit coding challenge solution"""
    challenge_id = request.form.get('challenge_id')
    code = request.form.get('code', '')
    
    if not challenge_id:
        return jsonify({'error': 'Challenge ID required'}), 400
    
    challenge = get_challenge(challenge_id)
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
    
    # Save submission
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO coding_submissions (user_id, challenge_id, code)
        VALUES (?, ?, ?)
    ''', (session['user_id'], challenge_id, code))
    conn.commit()
    conn.close()
    
    # Note: Actual code execution/evaluation would be implemented here
    # For now, we just save the submission
    
    return jsonify({'message': 'Submission saved successfully!'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5011)

