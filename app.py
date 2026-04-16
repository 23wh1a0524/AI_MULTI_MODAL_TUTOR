from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, ChatHistory
import os, json
from modules.ocr import extract_text_from_image
from modules.nlp_processor import preprocess_text, extract_topic
from modules.ai_model import get_explanation
from modules.quiz_generator import generate_quiz

app = Flask(__name__)
app.config['SECRET_KEY']          = 'tutor-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ── Auth routes ──

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('tutor'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        user     = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('tutor'))
        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email    = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
        elif User.query.filter_by(username=username).first():
            flash('Username already taken')
        else:
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('tutor'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ── Tutor route ──

@app.route('/tutor')
@login_required
def tutor():
    # Load last 10 history items
    history = ChatHistory.query.filter_by(user_id=current_user.id)\
                .order_by(ChatHistory.created_at.desc()).limit(10).all()
    history_data = [{
    'id':          h.id,
    'subject':     h.subject     or 'General',
    'question':    h.question    or '',
    'explanation': h.explanation or '',
    'quiz':        json.loads(h.quiz) if h.quiz else [],
    'topic':       h.topic       or '',
    'time':        h.created_at.strftime('%I:%M %p')
} for h in reversed(history)]
    return render_template('index.html',
                           username=current_user.username,
                           history=history_data)

# ── Ask route ──

@app.route('/ask', methods=['POST'])
@login_required
def ask():
    question = ''
    if request.form.get('text_question'):
        question = request.form.get('text_question')
    if 'image' in request.files and request.files['image'].filename:
        image = request.files['image']
        path  = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(path)
        extracted = extract_text_from_image(path)
        if extracted and len(extracted.strip()) > 5:
            question = extracted
        else:
            return jsonify({'error': 'No readable text found in image.'}), 400

    if not question:
        return jsonify({'error': 'No input provided'}), 400

    try:
        subject     = request.form.get('subject', 'General')
        explanation = get_explanation(question, subject=subject)
        topic       = extract_topic(question)
        quiz        = generate_quiz(topic, original_question=question, subject=subject)
        entry = ChatHistory(
            user_id=current_user.id,
            subject=subject,
            question=question[:500],
            explanation=explanation,
            quiz=json.dumps(quiz),
            topic=topic
        )
        db.session.add(entry)

        # Delete oldest if more than 10
        all_hist = ChatHistory.query.filter_by(user_id=current_user.id)\
                     .order_by(ChatHistory.created_at.asc()).all()
        if len(all_hist) > 10:
            for old in all_hist[:len(all_hist)-10]:
                db.session.delete(old)

        db.session.commit()

        return jsonify({
            'question':    question,
            'explanation': explanation,
            'quiz':        quiz,
            'topic':       topic
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)