from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER_COVERS'] = 'static/covers'
app.config['UPLOAD_FOLDER_VIDEOS'] = 'static/videos'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB максимум

# Створюємо папки якщо їх нема
os.makedirs(app.config['UPLOAD_FOLDER_COVERS'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_VIDEOS'], exist_ok=True)

# Каталог відео
series_list = [
    {"id": 1, "title": "Я секретар гільдії, але я не люблю понаднормову роботу", "cover": "covers/anime1.png", "folder": "anime1", "episodes": ["1", "2"], "type": "anime"},
    {"id": 2, "title": "Ласкаво просимо до Японії, пані", "cover": "covers/anime2.png", "folder": "anime2", "episodes": ["1"], "type": "anime"},
    {"id": 3, "title": "Дні Сакамото", "cover": "covers/anime3.png", "folder": "anime3", "episodes": ["1"], "type": "anime"},
    {"id": 4, "title": "Життя сорокарічного чоловіка в іншому світі", "cover": "covers/anime4.png", "folder": "anime4", "episodes": ["1", "2"], "type": "anime"},
    {"id": 5, "title": "Найгірша робота «оцінювача» виявилася найсильнішою", "cover": "covers/anime5.png", "folder": "anime5", "episodes": ["1"], "type": "anime"},
    {"id": 6, "title": "Гра в кальмара 2", "cover": "covers/serial1.png", "folder": "serial1", "episodes": ["1", "2"], "type": "series"},
    {"id": 7, "title": "Дюна: Пророцтво", "cover": "covers/serial2.png", "folder": "serial2", "episodes": ["1"], "type": "series"},
    {"id": 8, "title": "Безкоштовний сир", "cover": "covers/serial3.png", "folder": "serial3", "episodes": ["1"], "type": "series"},
    {"id": 9, "title": "Профі", "cover": "covers/film1.png", "folder": "film1", "episodes": ["1"], "type": "film"},
    {"id": 10, "title": "Майнкрафт в кіно", "cover": "covers/film2.png", "folder": "film2", "episodes": ["1"], "type": "film"},
    {"id": 11, "title": "Аніме-новина", "cover": "covers/news1.png", "folder": "news1", "episodes": ["1"], "type": "news"},
]

@app.route('/')
def index():
    return render_template("index.html", series=series_list)

@app.route('/watch/<int:series_id>')
def watch(series_id):
    episode = request.args.get("episode", "1")
    selected = next((s for s in series_list if s["id"] == series_id), None)
    if selected is None:
        return "Серіал не знайдено", 404

    video_path = f"videos/{selected['folder']}/episode{episode}.mp4"
    return render_template("watch.html", series=selected, episode=episode, video_path=video_path)

@app.route('/add', methods=['POST'])
def add_content():
    title = request.form.get('title')
    content_type = request.form.get('type')
    cover_file = request.files.get('cover')
    episode_file = request.files.get('episode')

    if not all([title, content_type, cover_file, episode_file]):
        return "Помилка: всі поля обов'язкові!", 400

    # Зберігаємо файли
    cover_filename = secure_filename(cover_file.filename)
    episode_filename = secure_filename(episode_file.filename)

    # Створюємо папку для відео
    folder_name = cover_filename.split('.')[0]
    video_folder = os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], folder_name)
    os.makedirs(video_folder, exist_ok=True)

    # Зберігаємо обкладинку
    cover_path = os.path.join(app.config['UPLOAD_FOLDER_COVERS'], cover_filename)
    cover_file.save(cover_path)

    # Зберігаємо відео
    video_path = os.path.join(video_folder, f"episode1.mp4")
    episode_file.save(video_path)

    # Додаємо в список
    new_id = max(s["id"] for s in series_list) + 1
    new_item = {
        "id": new_id,
        "title": title,
        "cover": f"covers/{cover_filename}",
        "folder": folder_name,
        "episodes": ["1"],
        "type": content_type
    }
    series_list.append(new_item)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
