from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename				#for securing filenames
from io import BytesIO						#to convert BLOB to Bytes
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATATBASE_URI'] = 'sqlite:///eg.db'	#name of db
db = SQLAlchemy(app)								#initialise db

class FileContents(db.Model):							
	id = db.Column(db.Integer, primary_key=True)	#each file has unique id
	name = db.Column(db.String(300))				#filename	
	data = db.Column(db.LargeBinary)				#data stored as BLOB

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/upload", methods=["POST"])					#when upload button is clicked
def upload():
	file = request.files['inputfile']					#request for selected file
	if file:
		mimetype = file.content_type
		print(mimetype)					#getting mime type
        allowed_mime = ("application/ms-excel","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")			#allowed mime
        if mimetype not in allowed_mime:				#checking mime
        	raise ValueError("Invalid mimetype")


        file_name = secure_filename(file.filename) 		#securing filename
        allowed_ext = ("xlsx","xls")					#extensions allowed
        if file_name.split(".")[1] not in allowed_ext:	#checking ext
        	raise NameError("Invalid extention")
        print("Correct extention")


        file.seek(0,os.SEEK_END)			#calcuating size
        file_size = file.tell()				#size
        limit_kb = 10						#MAX limit of uploaded file
    	if file_size > limit_kb * 1024:		#checking file size
        	raise ValueError("Max size of file is %s KB" % limit_kb) #raise Error if uploaded file size > required
        print("Correct size. Saving file to database")

        newFile = FileContents(name=file.filename,data=file.read())
        db.session.add(newFile)				#inserting file into db
        db.session.commit()					#commit changes
        return 'Saved' + file.filename + 'to the database'

@app.route("/download",methods=['POST'])
def download():								#when download button is clicked
	file_data = FileContents.query.filter_by(id=1).first()	
	#we can filter by the login id of the company
	return send_file(BytesIO(file_data.data), attachment_filename='UploadedExcel.xlsx',as_attachment=True)
	#data is in BLOB format. It is converted to Bytes and sent as an attachment wiht name UploadedExcel

if __name__ == '__main__':
	app.run(debug=True)
