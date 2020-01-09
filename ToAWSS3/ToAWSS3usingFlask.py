#HTML FORM = file_upload_form.html
"""
<html>  
<head>  
    <title>upload</title>  
</head>  
<body>  
    <form action = "/success" method = "POST" enctype="multipart/form-data">  
        <input type="file" name="file" />  
        <input type = "submit" value="Upload">  
    </form>  
</body>  
</html>  
"""
	
from flask import *  
from werkzeug.utils import secure_filename

app = Flask(__name__)  
 
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['post'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        if f:
	        mimetype = f.content_type						#getting mime type
	        allowed_mime = ("application/ms-excel")			#allowed mime
	        if mimetype not in allowed_mime					#checking mime
	        	raise ValueError("Invalid mimetype")


	        file_name = secure_filename(f.filename) 		#securing filename
	        allowed_ext = ("xlsx","xls")					#extensions allowed
	        if file_name.split(".")[1] not in allowed_ext:	#checking ext
	        	raise NameError("Invalid extention")
	        print("Correct extention")


	        f.seek(0,os.SEEK_END)				#calcuating size
	        file_size = f.tell()				#size
	        limit_kb = 10						#MAX limit of uploaded file
	    	if file_size > limit_kb * 1024:		#checking file size
	        	raise ValueError("Max size of file is %s KB" % limit_kb) #raise Error if uploaded file size > required
	        print("Correct size. Saving file to s3")


			import boto3					
			S3 = boto3.client('s3')				# Create an S3 client
			SOURCE_FILENAME = 'filename'
			BUCKET_NAME = 'bucket-name'
			S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, SOURCE_FILENAME)	#upload file in aws s3

	        #f.save(f.filename)  
	        print("File saved")   
	    else:
	    	return redirect(url_for('upload'))


if __name__ == '__main__':  
    app.run(debug = True)  