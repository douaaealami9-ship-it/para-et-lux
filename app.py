from flask import Flask, render_template, request, redirect, session
import json, os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.secret_key = 'douaa-meknes-2026'

# Hna fin ghadi tsajel tsawer - tari9a s7i7a
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
FICHIER = os.path.join(BASE_DIR, 'produits.json')

def get_produits():
    if not os.path.exists(FICHIER):
        with open(FICHIER,'w',encoding='utf-8') as f:
            json.dump([
                {"id":1, "nom":"Sérum Vitamine C", "prix":149, "cat":"visage", "img":"https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500"},
                {"id":2, "nom":"Collagène Marin", "prix":250, "cat":"vitamines", "img":"https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500"}
            ],f,ensure_ascii=False)
    with open(FICHIER,'r',encoding='utf-8') as f:
        return json.load(f)

def save_produits(prods):
    with open(FICHIER,'w',encoding='utf-8') as f:
        json.dump(prods,f,ensure_ascii=False,indent=2)

@app.route('/')
def home():
    return render_template('index.html', produits=get_produits())

@app.route('/admin', methods=['GET','POST'])
def admin():
    if session.get('admin') != True:
        if request.method=='POST' and request.form.get('pass')=='Dou@@e1234':
            session['admin']=True
        else:
            return '''<div style="text-align:center;margin-top:80px;font-family:Arial"><h2>Para Douaa</h2><form method="POST"><input type="password" name="pass" placeholder="1234" style="padding:12px;border-radius:10px"><br><br><button style="padding:12px 30px;background:#0a7a42;color:white;border:none;border-radius:10px">Dkhol</button></form></div>'''

    produits = get_produits()
    if request.method=='POST' and 'nom' in request.form:
        file = request.files.get('photo')
        img_path = ""
        if file and file.filename!='':
            filename = secure_filename(file.filename)
            filename = str(int(time.time()))+"_"+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path = f"/static/uploads/{filename}"

        if img_path:
            nouveau = {"id": max([p['id'] for p in produits], default=0)+1, "nom": request.form['nom'], "prix": int(request.form['prix']), "cat": request.form['cat'], "img": img_path}
            produits.append(nouveau)
            save_produits(produits)
        return redirect('/admin')

    if request.args.get('del'):
        produits = [p for p in produits if p['id']!=int(request.args.get('del'))]
        save_produits(produits)
        return redirect('/admin')
    return render_template('admin.html', produits=produits)