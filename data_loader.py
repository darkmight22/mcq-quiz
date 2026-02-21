"""
JSON Data Loader Module
Handles loading quizzes and coding challenges from JSON files.
"""

import json
import os
import random
import copy
from functools import lru_cache
from typing import Dict, List, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
MCQ_DIR = os.path.join(DATA_DIR, 'mcq')
CHALLENGES_FILE = os.path.join(DATA_DIR, 'coding_challenges.json')

LANGUAGES = [
    'html',
    'css',
    'javascript',
    'java',
    'php',
    'dsa',
    'python',
    'nextjs',
    'nodejs',
    'react',
    'c',
    'cpp',
    'csharp',
    'operating_system'
]
LEVELS = ['easy', 'medium', 'hard']

LANGUAGE_LABELS = {
    'html': 'HTML',
    'css': 'CSS',
    'javascript': 'JavaScript',
    'java': 'Java',
    'php': 'PHP',
    'dsa': 'DSA',
    'python': 'Python',
    'nextjs': 'Next.js',
    'nodejs': 'Node.js',
    'react': 'React',
    'c': 'C',
    'cpp': 'C++',
    'csharp': 'C#',
    'operating_system': 'Operating System'
}


def normalise(value: str) -> str:
    return value.strip().lower()


def get_language_label(language: Optional[str]) -> str:
    if not language:
        return ''
    key = normalise(language)
    return LANGUAGE_LABELS.get(key, key.replace('_', ' ').title())


def get_mcq_file_path(language: str, level: str) -> str:
    """Return the absolute path to the MCQ file for a language/level combo."""
    lang = normalise(language)
    lvl = normalise(level)
    return os.path.join(MCQ_DIR, lang, f'{lvl}.json')


def _load_json_file(path: str) -> Optional[Dict]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def load_quiz(language: str, level: str) -> Optional[Dict]:
    """Load a quiz for the provided language and level."""
    file_path = get_mcq_file_path(language, level)
    return _load_json_file(file_path)


def get_quiz_by_id(quiz_id: str) -> Optional[Dict]:
    """Load quiz data using combined quiz_id format <language>_<level> or shorthand like js_easy.
    Handles both 'javascript_easy' and 'js_easy' formats.
    """
    if not quiz_id or '_' not in quiz_id:
        return None
    
    # Split by last underscore to get language and level
    language, level = quiz_id.rsplit('_', 1)
    language = normalise(language)
    level = normalise(level)
    
    # Try to load with the provided language name first
    quiz = load_quiz(language, level)
    if quiz:
        return quiz
    
    # If not found and language is short (like 'js'), expand it
    # by finding the full language name that contains this as a prefix or matches it
    expanded_languages = {
        'js': 'javascript',
        'py': 'python',
        'cpp': 'cpp',
        'cs': 'csharp',
        'c#': 'csharp',
    }
    
    if language in expanded_languages:
        full_language = expanded_languages[language]
        quiz = load_quiz(full_language, level)
        if quiz:
            return quiz
    
    # Try fuzzy matching with full language list
    for full_lang in LANGUAGES:
        if full_lang.startswith(language) or language.startswith(full_lang[:2]):
            quiz = load_quiz(full_lang, level)
            if quiz:
                return quiz
    
    return None


def get_question_by_index(quiz_data: Dict, index: int) -> Optional[Dict]:
    """Return a question dict by index from already loaded quiz data."""
    if not quiz_data:
        return None
    questions = quiz_data.get('questions', [])
    if 0 <= index < len(questions):
        return questions[index]
    return None


def load_quiz_catalog() -> List[Dict]:
    """
    Load lightweight metadata for all quizzes.
    Useful for dashboard stats, selection menus, etc.
    """
    catalog = []
    for language in LANGUAGES:
        for level in LEVELS:
            quiz = load_quiz(language, level)
            if quiz:
                catalog.append({
                    'id': quiz.get('quiz_id') or f'{language}_{level}',
                    'language': language,
                    'level': level,
                    'title': quiz.get('title', f'{language.title()} {level.title()} Quiz'),
                    'description': quiz.get('description', ''),
                    'duration_minutes': quiz.get('duration_minutes', 15),
                    'difficulty': quiz.get('difficulty', level),
                    'questions_count': len(quiz.get('questions', []))
                })
    return catalog


@lru_cache(maxsize=1)
def load_coding_challenges() -> List[Dict]:
    """Load all coding challenges from coding_challenges.json"""
    data = _load_json_file(CHALLENGES_FILE)
    return data.get('challenges', []) if data else []


def get_challenges_by_language_and_level(language: Optional[str] = None,
                                         level: Optional[str] = None) -> List[Dict]:
    """Filter coding challenges by language and level."""
    challenges = load_coding_challenges()
    language = normalise(language) if language else None
    level = normalise(level) if level else None

    def matches(ch):
        if language and normalise(ch.get('language', '')) != language:
            return False
        if level and normalise(ch.get('level', '')) != level:
            return False
        return True

    return [ch for ch in challenges if matches(ch)]


def get_challenge(challenge_id: str) -> Optional[Dict]:
    """Get a specific coding challenge by its ID"""
    for challenge in load_coding_challenges():
        if challenge.get('id') == challenge_id:
            return challenge
    return None


def shuffle_options(question: Dict) -> Dict:
    """
    Create a copy of a question with shuffled options.
    Maintains correct answer mapping after shuffling.
    Does NOT modify the original question.
    """
    question_copy = copy.deepcopy(question)
    options = question_copy.get('options', [])
    
    if options:
        # Create a copy of options list and shuffle it
        options_copy = copy.deepcopy(options)
        random.shuffle(options_copy)
        question_copy['options'] = options_copy
    
    return question_copy


def shuffle_quiz_questions(quiz: Dict) -> Dict:
    """
    Create a copy of a quiz with shuffled questions and shuffled options.
    Maintains question and answer integrity.
    Does NOT modify the original quiz.
    """
    quiz_copy = copy.deepcopy(quiz)
    questions = quiz_copy.get('questions', [])
    
    if questions:
        # Shuffle questions
        shuffled_questions = copy.deepcopy(questions)
        random.shuffle(shuffled_questions)
        
        # Also shuffle options within each question
        shuffled_questions = [shuffle_options(q) for q in shuffled_questions]
        quiz_copy['questions'] = shuffled_questions
    
    return quiz_copy


def get_randomized_quiz(language: str, level: str) -> Optional[Dict]:
    """
    Load a quiz and return it with randomized questions and options.
    Each call returns a new randomized version.
    """
    quiz = load_quiz(language, level)
    if quiz:
        return shuffle_quiz_questions(quiz)
    return None


def get_randomized_quiz_by_id(quiz_id: str) -> Optional[Dict]:
    """Load quiz data using combined quiz_id format and return randomized version."""
    if not quiz_id or '_' not in quiz_id:
        return None
    language, level = quiz_id.rsplit('_', 1)
    return get_randomized_quiz(language, level)


# Backwards-compatible helper names (if templates/legacy code expect them)
def load_quizzes():
    return load_quiz_catalog()


def get_question(quiz_id, question_index):
    quiz = get_quiz_by_id(quiz_id)
    return get_question_by_index(quiz, question_index) if quiz else None

