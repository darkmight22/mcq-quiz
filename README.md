# MCQ Arena - Online Quiz & MCQ Practice Platform

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**A comprehensive online platform for practicing Multiple Choice Questions (MCQs) across various programming languages and technical subjects**

[Features](#features) • [Tech Stack](#tech-stack) • [Installation](#installation) • [Documentation](#documentation)

</div>

---

## 1. Project Title and Description

### What is MCQ Arena?

**MCQ Arena** is a full-stack web-based learning platform designed to help students and professionals practice Multiple Choice Questions (MCQs) across various programming languages and computer science topics. The platform provides an interactive, timed quiz experience with instant feedback, performance tracking, and comprehensive analytics.

### Purpose of the Platform

MCQ Arena serves as a comprehensive practice platform that enables users to:
- Prepare for technical interviews and certification exams
- Practice coding concepts through curated MCQ questions
- Build confidence in programming fundamentals
- Track their learning progress over time
- Access a diverse question bank across multiple programming domains

### Target Users

- **Students**: Preparing for academic exams, placements, and competitive programming
- **Professionals**: Brushing up technical skills and preparing for certifications
- **Interview Candidates**: Practicing coding and technical aptitude questions
- **Self-learners**: Independently learning programming concepts through practice

---

## 2. Features

### 🔐 User Authentication & Security
- **User Registration**: Secure signup with password hashing
- **Password Security**: Industry-standard password hashing using Werkzeug
- **Session Management**: Secure session handling and login persistence

### 👤 Profile Dashboard
- **User Statistics**: Track total attempts, best score, and average score
- **Quiz History**: View recent quiz attempts with timestamps
- **Performance Metrics**: Visual representation of user performance
- **Quick Access**: Easy navigation to quiz selection and coding challenges

### 📝 Quiz System
- **Multiple Programming Languages**: JavaScript, Python, Java, C++, C#, CSS, HTML, React, Node.js, Next.js, PHP, DSA, Operating Systems
- **Difficulty Levels**: Easy, Medium, Hard questions available
- **Randomized Questions**: Questions are shuffled for each attempt
- **Randomized Options**: Answer options are randomized to prevent memorization
- **Partial Attempts**: Users can save answers and revisit questions

### ⏱️ Timer Functionality
- **Configurable Duration**: Different time limits for different quiz types
- **Real-time Countdown**: Live timer display during quiz attempt
- **Auto-submission**: Automatic quiz submission when time expires
- **Visual Indicators**: Clear indication of remaining time

### 📊 Score Calculation & Analysis
- **Instant Scoring**: Automatic calculation of scores after submission
- **Detailed Breakdown**: Correct, Wrong, and Unanswered question count
- **Percentage Display**: Easy-to-understand score percentage
- **Performance Tracking**: Historical score tracking over multiple attempts

### 🎯 Result Analysis
- **Question Review**: Detailed review of each question with correct/incorrect status
- **Option Comparison**: See selected answer vs. correct answer
- **Visual Feedback**: Color-coded results for easy understanding
- **Download Results**: Export quiz results for personal records

### 💻 Coding Challenges
- **Hands-on Practice**: Practice coding problems across languages
- **Code Editor**: Online code submission interface
- **Challenge Database**: Curated coding challenges with varying difficulty

### 📱 Responsive Design
- **Mobile-Friendly**: Fully responsive UI that works on all devices
- **Cross-browser Support**: Compatible with all modern browsers

---

## 3. Tech Stack

### Frontend Technologies
| Technology | Purpose |
|-----------|---------|
| **HTML5** | Page structure and semantic markup |
| **CSS3** | Styling and responsive design |
| **JavaScript** | Client-side interactivity and DOM manipulation |
| **Jinja2** | Server-side templating for dynamic content rendering |

### Backend Technologies
| Technology | Purpose |
|-----------|---------|
| **Python 3.8+** | Core backend language |
| **Flask 2.0+** | Lightweight web framework |
| **Werkzeug** | WSGI utilities and security features |

### Database
| Technology | Purpose |
|-----------|---------|
| **SQLite 3** | Lightweight relational database |
| **SQL** | Database queries and operations |

### Additional Libraries
- `json` - Data serialization and loading quiz content
- `random` - Question and option randomization
- `datetime` - Timestamp handling for attempt tracking
- `copy` - Deep copying data structures

---

## 4. ER Diagram (Entity-Relationship Model)

### Entity-Relationship Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌──────────────────┐                ┌──────────────────────┐      │
│  │   USERS          │                │    ATTEMPTS          │      │
│  ├──────────────────┤                ├──────────────────────┤      │
│  │ id (PK)          │◄───────────────│ id (PK)              │      │
│  │ name             │       1:N      │ user_id (FK)         │      │
│  │ email (UNIQUE)   │                │ quiz_id              │      │
│  │ password_hash    │                │ score                │      │
│  │ created_at       │                │ started_at           │      │
│  │                  │                │ completed_at         │      │
│  │                  │                │ total_correct        │      │
│  │                  │                │ total_wrong          │      │
│  │                  │                │ total_unanswered     │      │
│  └──────────────────┘                └──────────────────────┘      │
│           ▲                                     │                  │
│           │                                     │ 1:N              │
│           │                            ┌────────▼─────────────┐   │
│           │                            │ ATTEMPT_ANSWERS      │   │
│           │                            ├──────────────────────┤   │
│           │                            │ id (PK)              │   │
│           │                            │ attempt_id (FK)      │   │
│           │                            │ quiz_id              │   │
│           │                            │ question_id          │   │
│           │                            │ selected_option_id   │   │
│           │                            │ is_correct           │   │
│           │                            └──────────────────────┘   │
│           │                                                        │
│  ┌────────┴─────────────────┐                                     │
│  │                          │                                     │
│  │  ┌──────────────────────────────┐  ┌─────────────────────┐    │
│  │  │ CODING_SUBMISSIONS           │  │ QUIZ (from JSON)    │    │
│  │  ├──────────────────────────────┤  ├─────────────────────┤    │
│  │  │ id (PK)                      │  │ quiz_id (PK)        │    │
│  └──│ user_id (FK)                 │  │ title               │    │
│     │ challenge_id                 │  │ duration_minutes    │    │
│     │ code (submitted code)        │  │ questions (array)   │    │
│     │ submitted_at                 │  │ language            │    │
│     └──────────────────────────────┘  │ level               │    │
│                                       └─────────────────────┘    │
│                                                                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Entity Descriptions

#### **USERS**
- **id**: Primary key, auto-incrementing integer
- **name**: User's full name
- **email**: Unique email address (used for login)
- **password_hash**: Hashed password for security
- **created_at**: Account creation timestamp

#### **ATTEMPTS**
- **id**: Primary key, auto-incrementing integer
- **user_id**: Foreign key referencing USERS table
- **quiz_id**: Identifier for the quiz taken
- **score**: Total score obtained
- **started_at**: Quiz start timestamp
- **completed_at**: Quiz completion timestamp
- **total_correct**: Count of correct answers
- **total_wrong**: Count of incorrect answers
- **total_unanswered**: Count of unanswered questions

#### **ATTEMPT_ANSWERS**
- **id**: Primary key, auto-incrementing integer
- **attempt_id**: Foreign key referencing ATTEMPTS table
- **quiz_id**: Quiz identifier (for reference)
- **question_id**: Question identifier
- **selected_option_id**: Selected answer option
- **is_correct**: Boolean flag indicating if answer is correct

#### **CODING_SUBMISSIONS**
- **id**: Primary key, auto-incrementing integer
- **user_id**: Foreign key referencing USERS table
- **challenge_id**: Identifier for the coding challenge
- **code**: User's submitted code
- **submitted_at**: Code submission timestamp

### Relationships

| Relationship | Type | Description |
|-------------|------|-------------|
| Users ↔ Attempts | 1:N | One user can have many quiz attempts |
| Attempts ↔ Attempt Answers | 1:N | One attempt can have many answers |
| Users ↔ Coding Submissions | 1:N | One user can have many code submissions |

---

## 5. Database Schema Explanation

### Complete Database Schema

```sql
-- Users Table: Stores user account information
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attempts Table: Stores quiz attempt records
CREATE TABLE attempts (
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
);

-- Attempt Answers Table: Stores individual question answers
CREATE TABLE attempt_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id INTEGER NOT NULL,
    quiz_id TEXT NOT NULL,
    question_id INTEGER NOT NULL,
    selected_option_id TEXT,
    is_correct INTEGER DEFAULT 0,
    FOREIGN KEY (attempt_id) REFERENCES attempts (id)
);

-- Coding Submissions Table: Stores code submissions for challenges
CREATE TABLE coding_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    challenge_id TEXT NOT NULL,
    code TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Schema Details

#### **users Table**
| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| id | INTEGER | PK, AUTO_INCREMENT | Unique user identifier |
| name | TEXT | NOT NULL | User's full name |
| email | TEXT | UNIQUE, NOT NULL | Email for login and communication |
| password_hash | TEXT | NOT NULL | Securely hashed password |
| created_at | TIMESTAMP | DEFAULT CURRENT | Registration timestamp |

#### **attempts Table**
| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| id | INTEGER | PK, AUTO_INCREMENT | Unique attempt identifier |
| user_id | INTEGER | FK → users.id | Reference to user |
| quiz_id | TEXT | NOT NULL | Quiz identifier |
| score | INTEGER | DEFAULT 0 | Final score |
| started_at | TIMESTAMP | DEFAULT CURRENT | Quiz start time |
| completed_at | TIMESTAMP | NULLABLE | Quiz completion time |
| total_correct | INTEGER | DEFAULT 0 | Count of correct answers |
| total_wrong | INTEGER | DEFAULT 0 | Count of wrong answers |
| total_unanswered | INTEGER | DEFAULT 0 | Count of unanswered questions |

#### **attempt_answers Table**
| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| id | INTEGER | PK, AUTO_INCREMENT | Unique answer record ID |
| attempt_id | INTEGER | FK → attempts.id | Reference to attempt |
| quiz_id | TEXT | NOT NULL | Quiz identifier |
| question_id | INTEGER | NOT NULL | Question identifier |
| selected_option_id | TEXT | NULLABLE | Selected answer option ID |
| is_correct | INTEGER | DEFAULT 0 | Correctness flag (0=wrong, 1=correct) |

#### **coding_submissions Table**
| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| id | INTEGER | PK, AUTO_INCREMENT | Unique submission ID |
| user_id | INTEGER | FK → users.id | Reference to user |
| challenge_id | TEXT | NOT NULL | Challenge identifier |
| code | TEXT | NULLABLE | Submitted source code |
| submitted_at | TIMESTAMP | DEFAULT CURRENT | Submission timestamp |

---

## 6. Connection Diagram (Architecture)

### System Architecture Overview

```
┌────────────────────────────────────────────────────────────────────┐
│                         CLIENT SIDE                                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Web Browser                               │  │
│  │  ┌───────────────┐  ┌─────────────┐  ┌───────────────────┐  │  │
│  │  │ HTML/CSS/JS   │  │  Templates  │  │   Static Assets   │  │  │
│  │  │               │  │  (Jinja2)   │  │  (CSS, Images)    │  │  │
│  │  └───────────────┘  └─────────────┘  └───────────────────┘  │  │
│  │         │                   │                  │              │  │
│  │         └───────────────────┼──────────────────┘              │  │
│  │                             │                                 │  │
│  │                    HTTP/HTTPS Requests                        │  │
│  └──────────────────────────────┬──────────────────────────────┘  │
└───────────────────────────────────┼────────────────────────────────┘
                                    │
                    ┌───────────────▼──────────────────┐
                    │   NETWORK COMMUNICATION          │
                    │   (TCP/IP, HTTP Protocol)        │
                    └───────────────┬──────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────┐
│                       BACKEND SERVER                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              Flask Application Server                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐  │  │
│  │  │ Route Layer  │  │ Logic Layer  │  │  Auth Handler     │  │  │
│  │  │              │  │              │  │  (OTP, Login)     │  │  │
│  │  │ /quiz        │  │ Quiz Engine  │  │                   │  │  │
│  │  │ /login       │  │ Timer Logic  │  │ Session Mgmt      │  │  │
│  │  │ /coding      │  │ Scoring      │  │                   │  │  │
│  │  │ /dashboard   │  │ randomize()  │  │ Email Service     │  │  │
│  │  │ /verify      │  │              │  │ (SMTP)            │  │  │
│  │  └──────┬───────┘  └──────┬───────┘  └────────┬──────────┘  │  │
│  │         │                 │                   │              │  │
│  │         └─────────────────┼───────────────────┘              │  │
│  │                           │                                  │  │
│  │                ┌──────────▼────────────┐                    │  │
│  │                │  Data Layer           │                    │  │
│  │                │  (data_loader.py)     │                    │  │
│  │                │  load_quiz()          │                    │  │
│  │                │  get_quiz_by_id()     │                    │  │
│  │                └──────────┬────────────┘                    │  │
│  └─────────────────────────────┼──────────────────────────────┘  │
│                                │                                  │
│                    Database Connections                          │
└────────────────────────────────┼──────────────────────────────────┘
                                 │
        ┌────────────────────────┴────────────────────────┐
        │                                                 │
        │                                                 │
┌───────▼──────────────────┐              ┌─────────────▼──────────┐
│   SQLite Database File   │              │   JSON Data Files      │
│   (codemcq.db)           │              │   (/data/mcq/)         │
│  ┌─────────────────────┐ │              │ ┌──────────────────┐   │
│  │ users               │ │              │ │ easy.json        │   │
│  │ attempts            │ │              │ │ medium.json      │   │
│  │ attempt_answers     │ │              │ │ hard.json        │   │
│  │ coding_submissions  │ │              │ │                  │   │
│  └─────────────────────┘ │              │ (Multiple langs)   │   │
└──────────────────────────┘              └──────────────────┘   │
                                          ┌──────────────────┐   │
                                          │ coding_          │   │
                                          │ challenges.json  │   │
                                          └──────────────────┘   │
                                                                 │
                                    Data Storage Layer
```

### How the System Works Together

1. **User Interaction** → Browser sends HTTP requests to Flask server
2. **Flask Routes** → Server receives requests and routes them to appropriate handlers
3. **Business Logic** → Handlers process requests using quiz engine and data loaders
4. **Database Operations** → Data is read/written to SQLite database
5. **JSON Data** → Quiz questions are loaded from JSON files
6. **Response Generation** → Templates render HTML with data
7. **Client Rendering** → Browser displays the rendered page to user

---

## 7. Workflow - User Journey

### Step-by-Step User Journey Flow

```
Signup → Email Verification → Login → Dashboard → Quiz Selection → 
Quiz Attempt → Answer Questions → Submit Quiz → View Results
```

**Detailed Workflow Stages:**

1. **Signup Process**: User registers with name, email, password
2. **Email Verification**: OTP sent to email, user verifies
3. **Login**: User logs in with email and password
4. **Dashboard**: User sees stats, recent attempts, quick access
5. **Quiz Selection**: Choose language and difficulty level
6. **Quiz Attempt**: Answer randomized questions with timer
7. **Submit Quiz**: Auto or manual submission
8. **View Results**: See score, breakdown, and question review

---

## 8. Working of the Project

### How Quiz Loading Works

When a user selects a quiz, the system:
1. Loads JSON file from `data/mcq/{language}/{level}.json`
2. Randomizes question order
3. Randomizes answer options for each question
4. Stores randomized data in Flask session
5. Displays questions one by one
6. Each attempt has unique randomization

### How Timer Works

- Quiz duration set from JSON metadata (typically 15 minutes)
- Server calculates remaining time on each page load
- JavaScript countdown updates every second
- Auto-submission when time reaches zero
- User cannot prevent automatic submission

### How Answers Are Stored

- User selects an answer option
- Answer immediately sent to server
- Database checks if answer already exists
- Updates existing or inserts new record
- Tracks selected option and correctness
- User can modify answers before submission

### How Score Is Calculated

```
For each question:
  ├─ If unanswered → increment unanswered count
  ├─ If correct answer → increment correct count
  └─ If wrong answer → increment wrong count

Final Score = Number of Correct Answers
Percentage = (Correct / Total) × 100
```

---

## 9. Profile Dashboard Explanation

The dashboard displays:

✅ **User Statistics**
- Total quiz attempts taken
- Best score achieved
- Average score across all attempts

✅ **Recent Quiz History**
- Last 5 quiz attempts
- Score for each attempt
- Date and time taken

✅ **Quick Navigation**
- Start new quiz button
- Browse coding challenges
- View complete history

✅ **Account Management**
- View profile info
- Logout option

---

## 10. Quiz Module Explanation

### Quiz Lifecycle

1. **Load Quiz**: Questions and options randomized
2. **Create Attempt**: Record created in database
3. **Display Question**: Show current question with timer
4. **Answer Selection**: User selects answer, saved to database
5. **Next Question**: Navigate to next or submit
6. **Calculate Results**: Score computed
7. **Display Results**: Show detailed feedback

### Timer Features

- Countdown in MM:SS format
- Color changes as time runs low (Green → Yellow → Red)
- Warnings at 5 minutes and 1 minute remaining
- Auto-submission when time expires

---

## 11. Installation Guide

### Prerequisites
- Python 3.8+
- pip
- Gmail account (for OTP email)

### Installation Steps

1. **Clone repository**
```bash
git clone https://github.com/yourusername/mcq-arena.git
cd mcq-arena
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure email settings** in `app.py`:
```python
EMAIL_USER = 'your-email@gmail.com'
EMAIL_PASSWORD = 'your-app-password'
```

5. **Run application**
```bash
python app.py
```

6. **Access at** `http://localhost:5011`

---

## 12. Folder Structure

```
mcq-arena/
├── README.md                    # Documentation
├── requirements.txt             # Dependencies
├── app.py                       # Main Flask app
├── data_loader.py               # Data loading functions
├── codemcq.db                   # SQLite database
│
├── templates/                   # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── quiz_select.html
│   ├── quiz_question.html
│   ├── result.html
│   └── ...
│
├── static/                      # Static files
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
│
└── data/                        # Quiz data
    ├── coding_challenges.json
    └── mcq/
        ├── python/{easy,medium,hard}.json
        ├── javascript/{easy,medium,hard}.json
        ├── java/{easy,medium,hard}.json
        └── ... (other languages)
```

---

## 13. Future Improvements

### Phase 1: UX Enhancements
- [ ] Dark/light mode toggle
- [ ] Bookmark favorite questions
- [ ] Create custom quizzes
- [ ] Discussion forums

### Phase 2: Analytics
- [ ] Performance graphs
- [ ] Topic-wise analysis
- [ ] Learning recommendations
- [ ] Weak area identification

### Phase 3: Gamification
- [ ] Leaderboards
- [ ] Achievement badges
- [ ] Points system
- [ ] Multiplayer quizzes

### Phase 4: Mobile App
- [ ] iOS app
- [ ] Android app
- [ ] Offline mode
- [ ] Push notifications

### Phase 5: Admin Panel
- [ ] User management
- [ ] Content management
- [ ] Analytics reports
- [ ] Question moderation

---

## 14. Screenshots

### Placeholder for UI Screenshots

**Landing Page** → **Signup** → **Dashboard** → **Quiz Selection** → 
**Quiz Question** → **Results** → **Quiz History**

---

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push: `git push origin feature/name`
5. Open Pull Request

---

## License

MIT License - See LICENSE file for details

---

## Support

- **Email**: support@mcqarena.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/mcq-arena/issues)
- **Documentation**: Check project files

---

## FAQ

**Q: Can I use commercially?**  
A: Yes, under MIT License with attribution.

**Q: How to add questions?**  
A: Add JSON files in `data/mcq/{language}/` folder.

**Q: Is it scalable?**  
A: SQLite for small deployments; upgrade to PostgreSQL for larger scale.

---

<div align="center">

**⭐ If helpful, please star this repository!**

Made with ❤️ for learners and developers

**Last Updated**: February 13, 2026  
**Version**: 1.0.0

</div>

# coding
