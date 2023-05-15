from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import File
from . import db
from . import Cryptographer
from . import Decoder
import os
import shutil
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
  return render_template("home.html", user=current_user)


@views.route('/decoding-new', methods=['GET', 'POST'])
@login_required
def decoding():
  if request.method == 'POST':
    file = request.form.get('file')
    current_cipher = str(request.form.get('cipher'))
    offset = int(request.form.get('offset'))
    new_file = File(data=file, user_id=current_user.id)
    db.session.add(new_file)
    db.session.commit()
    file_id = new_file.id
    path = "src/files/" + str(file_id) + "/"
    os.mkdir(path)
    path_source = path + "SOURCE.txt"
    path_key = path + "KEY.txt"
    path_output = path + "OUTPUT.txt"
    s = open(path_source, "w")
    k = open(path_key, "w")
    o = open(path_output, "w")
    s.write(str(request.form.get('file')))
    s.close()
    k.close()
    o.close()
    db.session.delete(new_file)
    db.session.commit()
    if current_cipher == "Caesar":
      if (offset == 0):
        with open(path_source, "r") as inp:
          for string in inp:
            Decoder.DecoderCaesarCipherWithoutKey(path_source, path_output)
      else:
        with open(path_source, "r") as inp:
          for string in inp:
            Decoder.DecoderCaesarCipherWithKey(path_source, offset, path_output)
      output_str = ""
      with open(path_output, "r") as inp:
        for string in inp:
          output_str += string
      new_file = File(data=output_str, user_id=current_user.id)
    elif current_cipher == "Vigenere":
      with open(path_source, "r") as inp:
        for string in inp:
          Cryptographer.VigenereCipher(string, path_key, path_output)
      output_str = ""
      with open(path_output, "r") as inp:
        for string in inp:
          output_str += string
      new_file = File(data=output_str, user_id=current_user.id)
    elif current_cipher == "Vernam":
      with open(path_source, "r") as inp:
        for string in inp:
          Cryptographer.VernamCipher(string, path_key, path_output)
      output_str = ""
      with open(path_output, "r") as inp:
        for string in inp:
          output_str += string
      new_file = File(data=output_str, user_id=current_user.id)
    else:
      with open(path_source, "r") as inp:
        for string in inp:
          Cryptographer.ColumnarCipher(string, path_key, path_output)
      output_str = ""
      with open(path_output, "r") as inp:
        for string in inp:
          output_str += string
      new_file = File(data=output_str, user_id=current_user.id)
    db.session.add(new_file)
    db.session.commit()

    flash('File added!', category='success')
  return render_template('encryption.html', user=current_user)


@views.route('/encryption', methods=['GET', 'POST'])
@login_required
def encryption():
  if request.method == 'POST':
    file = request.form.get('file')
    current_cipher = str(request.form.get('cipher'))
    offset = int(request.form.get('offset'))
    new_file = File(data=file, user_id=current_user.id)
    db.session.add(new_file)
    db.session.commit()
    file_id = new_file.id
    path = "src/files/" + str(file_id) + "/"
    os.mkdir(path)
    path_source = path + "SOURCE.txt"
    path_key = path + "KEY.txt"
    path_output = path + "OUTPUT.txt"
    s = open(path_source, "w")
    k = open(path_key, "w")
    o = open(path_output, "w")
    s.write(str(request.form.get('file')))
    s.close()
    k.close()
    o.close()
    db.session.delete(new_file)
    db.session.commit()
    if current_cipher == "Caesar":
      with open(path_source, "r") as inp:
        for string in inp:
          Cryptographer.CaesarCipher(string, offset, path_output)
      output_str = ""
      with open(path_output, "r") as inp:
        for string in inp:
          output_str += string
      new_file = File(data=output_str, user_id=current_user.id)
    elif current_cipher == "Vigenere":
      with open(path_source, "r") as inp:
        for string in inp:
          Cryptographer.VigenereCipher(string, path_key, path_output)
      output_str = ""
      with open(path_output, "r") as inp:
        for string in inp:
          output_str += string
      new_file = File(data=output_str, user_id=current_user.id)
    elif current_cipher == "Vernam":
      with open(path_source, "r") as inp:
        for string in inp:
          Cryptographer.VernamCipher(string, path_key, path_output)
      output_str = ""
      with open(path_output, "r") as inp:
        for string in inp:
          output_str += string
      new_file = File(data=output_str, user_id=current_user.id)
    else:
      with open(path_source, "r") as inp:
        for string in inp:
          Cryptographer.ColumnarCipher(string, path_key, path_output)
      output_str = ""
      with open(path_output, "r") as inp:
        for string in inp:
          output_str += string
      new_file = File(data=output_str, user_id=current_user.id)
    db.session.add(new_file)
    db.session.commit()

    flash('File added!', category='success')
  return render_template('encryption.html', user=current_user)


@views.route('/delete-file', methods=['POST'])
def delete_file():
  file = json.loads(request.data)
  file_id = file['file_id']
  file = File.query.get(file_id)
  if file:
    if file.user_id == current_user.id:
      db.session.delete(file)
      db.session.commit()
      path = "src/files/" + str(file_id) + "/"
      shutil.rmtree(path)

  return jsonify({})

