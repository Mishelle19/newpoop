from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
  return " <html><head></head> <body> To add: /net. </body></html>"

from flask import render_template
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lem7C0bAAAAAFb0mjCJ-JvSZOIAJFQ4ZhVnYxDd'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lem7C0bAAAAAHPlZJAjMJdrhuN8twMTBf0ilGIg'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
class NetForm(FlaskForm):
  openid = StringField('Насколько повернуть(в градусах).', validators = [DataRequired()])
  upload = FileField('Загрузка изображения', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
  recaptcha = RecaptchaField()
  submit = SubmitField('send')
 from werkzeug.utils import secure_filename
 import os
 import numpy as np
 from PIL import Image
 import matplotlib.pyplot as plt
 import seaborn as sns

def draw(filename,openid):
  print(filename)
  imag= Image.open(filename)
  openid=int(openid)

  #график
  fig = plt.figure(figsize=(6, 4))
  ax = fig.add_subplot()
  data = np.random.randint(0, 255, (100, 100))
  ax.imshow(imag, cmap='plasma')
  b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
  fig.colorbar(b, ax=ax)
  gr_path = "./static/newgr.png"
  sns.displot(data)
  plt.savefig(gr_path)
  plt.close()
  
  img=img.rotate(openid)
  output_filename = filename
  img.save(output_filename)
  
  
  
return output_filename,gr_path

@app.route("/net",methods=['GET', 'POST'])
def net():
  form = NetForm()
  filename=None
  newfilename=None
  grname=None
  if form.validate_on_submit():
    filename = os.path.join('./static', secure_filename(form.upload.data.filename))
    ch=form.openid.data
    form.upload.data.save(filename)
    newfilename,grname = draw(filename,ch)
return render_template('net.html',form=form,image_name=newfilename,gr_name=grname)

if __name__ == "__main__":
  app.run(host='127.0.0.1',port=5000)
