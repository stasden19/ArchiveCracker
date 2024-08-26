import os
import re
from pathlib import Path
from flask import Flask, render_template, request, redirect, make_response, session, url_for, abort, jsonify
from flask_uploads import IMAGES, UploadSet, configure_uploads
from werkzeug.utils import secure_filename
from john_cmd import zip, zip7, rar
import asyncio
import threading
import secrets

app = Flask(__name__)
resulted = None


@app.route('/result/<filename1>', methods=['POST', 'GET'])
def result(filename1):
    def zip_file(filename):
        global resulted
        resulted = None
        # выполняем функцию zip в отдельном потоке
        if os.path.splitext(filename1)[-1] == '.zip':
            resulted = zip(f'./static/files/{filename}', passlist='passlist.txt')
        elif os.path.splitext(filename1)[-1] == '.7z':
            resulted = zip7(f'./static/files/{filename}', passlist='passlist.txt')
        elif os.path.splitext(filename1)[-1] == '.rar':
            resulted = rar(f'./static/files/{filename}', passlist='passlist.txt')
        try:
            resulted = re.findall(r'\n(.*?) \n', resulted)[0] if resulted else 'Не тот формат файла'
        except:
            resulted = 'Пароль не найден.'
        # resulted = re.findall(r'\n(.*?) \n', resulted)if resulted else 'Не тот формат файла'
        print(resulted)
        os.system(f'rm ./static/files/{filename}')
        os.system(f'rm ./static/hashes/{filename.split(".")[0]}.hashes')
        # записываем результат в файл

        # создаем отдельный поток для выполнения функции zip

    thread = threading.Thread(target=zip_file, args=(filename1,))
    thread.start()

    # возвращаем страницу с сообщением "Обработка..."
    return render_template('result.html', filename=filename1)


@app.route('/task_status')
def task_status():
    # return '1'
    global resulted
    if resulted is None:
        return jsonify({"status": "running"})
    else:
        return jsonify({"status": "done", "result": resulted})


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html"), 200
    # return redirect(url_for("result")), 302


@app.route('/upload', methods=['PUT'])
def upload_chunk():
    file = request.files["file"]
    file_uuid = request.form["dzuuid"]
    # Generate a unique filename to avoid overwriting using 8 chars of uuid before filename.
    filename = f"{file_uuid[:8]}"
    try:
        int(filename, 16)
    except:
        return render_template('index.html')

    save_path = Path("static", "files", filename + os.path.splitext(file.filename)[-1])
    # if
    # print(save_path)
    current_chunk = int(request.form["dzchunkindex"])
    chunk_size = int(request.form["dzchunksize"])
    total_chunks = int(request.form["dztotalchunkcount"])
    if chunk_size * total_chunks > 1.5e10:
        abort(400)

    if os.path.splitext(file.filename)[-1] in ['.zip', '.rar', '.7z']:
        with open(save_path, "ab") as f:
            f.write(file.stream.read())
    else:
        return 'Not access file format', 400

    if current_chunk + 1 == total_chunks:
        # This was the last chunk, the file should be complete and the size we expect
        if os.path.getsize(save_path) != int(request.form["dztotalfilesize"]):
            print(os.path.getsize(save_path), int(request.form["dztotalfilesize"]))
            return "Size mismatch.", 500
        # jsonify({'redirect': url_for('result')}), 200
        return jsonify({'redirect': f"/result/{file_uuid[:8]}{os.path.splitext(file.filename)[-1]}"}), 200
    return 'Success', 200
    # print(request.form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
