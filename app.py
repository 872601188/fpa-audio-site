import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fpa-audio-site-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///instance/fpa_audio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 确保 instance 目录存在
os.makedirs('instance', exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录以访问此页面'

# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

# 音频文件模型
class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    part_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    oss_url = db.Column(db.String(500), nullable=False)
    file_size_mb = db.Column(db.Float)
    duration_minutes = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 初始化数据库和默认用户
@app.before_request
def create_tables():
    db.create_all()
    # 创建默认管理员账号
    if not User.query.filter_by(username='Admin').first():
        admin = User(
            username='Admin',
            password_hash=generate_password_hash('Admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ 默认管理员账号已创建: Admin / Admin123")
    
    # 初始化音频数据（如果不存在）
    if AudioFile.query.count() == 0:
        audio_files = [
            AudioFile(
                title='Part 1 - 开场白',
                part_number=1,
                description='功能点审核培训开场介绍',
                oss_url='http://meetingweike.oss-cn-beijing.aliyuncs.com/tts/fpa_training_intro_20260401_211938.mp3',
                file_size_mb=1.4,
                duration_minutes=1.5
            ),
            AudioFile(
                title='Part 2 - 基本概念与总体审核原则',
                part_number=2,
                description='功能点基本概念、审核三大原则（规范性、优先级、一致性）',
                oss_url='http://meetingweike.oss-cn-beijing.aliyuncs.com/tts/FPA_Part2_%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5%E4%B8%8E%E6%80%BB%E4%BD%93%E5%AE%A1%E6%A0%B8%E5%8E%9F%E5%88%99_20260401_213743.mp3',
                file_size_mb=4.8,
                duration_minutes=5.0
            ),
            AudioFile(
                title='Part 3 - 事务功能审核规则',
                part_number=3,
                description='事务功能定义、审核规则、常见错误案例分析',
                oss_url='http://meetingweike.oss-cn-beijing.aliyuncs.com/tts/FPA_Part3_%E4%BA%8B%E5%8A%A1%E5%8A%9F%E8%83%BD%E5%AE%A1%E6%A0%B8%E8%A7%84%E5%88%99_20260401_213743.mp3',
                file_size_mb=12.0,
                duration_minutes=12.0
            ),
            AudioFile(
                title='Part 4 - 数据功能审核规则',
                part_number=4,
                description='数据功能定义、ILF/EIF审核规则、复杂程度判断',
                oss_url='http://meetingweike.oss-cn-beijing.aliyuncs.com/tts/FPA_Part4_%E6%95%B0%E6%8D%AE%E5%8A%9F%E8%83%BD%E5%AE%A1%E6%A0%B8%E8%A7%84%E5%88%99_20260401_213743.mp3',
                file_size_mb=7.1,
                duration_minutes=7.0
            ),
            AudioFile(
                title='Part 5 - 典型案例与常见问题',
                part_number=5,
                description='功能点审核典型案例分析、常见问题解答',
                oss_url='http://meetingweike.oss-cn-beijing.aliyuncs.com/tts/FPA_Part5_%E5%85%B8%E5%9E%8B%E6%A1%88%E4%BE%8B%E4%B8%8E%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98_20260401_213743.mp3',
                file_size_mb=15.1,
                duration_minutes=15.0
            )
        ]
        for audio in audio_files:
            db.session.add(audio)
        db.session.commit()
        print("✅ 音频数据已初始化")

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash('登录成功！', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('login.html')

# 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('login'))

# 首页（音频列表）
@app.route('/')
@login_required
def index():
    audio_files = AudioFile.query.order_by(AudioFile.part_number).all()
    return render_template('index.html', audio_files=audio_files)

# 音频播放页面
@app.route('/play/<int:audio_id>')
@login_required
def play(audio_id):
    audio = AudioFile.query.get_or_404(audio_id)
    return render_template('player.html', audio=audio)

# 下载音频（代理下载）
@app.route('/download/<int:audio_id>')
@login_required
def download(audio_id):
    audio = AudioFile.query.get_or_404(audio_id)
    try:
        # 从OSS下载并返回
        response = requests.get(audio.oss_url, stream=True)
        return Response(
            response.iter_content(chunk_size=8192),
            headers={
                'Content-Type': 'audio/mpeg',
                'Content-Disposition': f'attachment; filename="{audio.title}.mp3"'
            }
        )
    except Exception as e:
        flash(f'下载失败: {str(e)}', 'danger')
        return redirect(url_for('index'))

# 获取音频流（用于播放器）
@app.route('/stream/<int:audio_id>')
@login_required
def stream(audio_id):
    audio = AudioFile.query.get_or_404(audio_id)
    return redirect(audio.oss_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
