#HTML FORM
"""
<html>
<body>
   <form enctype = "multipart/form-data"
                     action = "file_upload_validator.py" method = "post">
   <p>File: <input type = "file" name = "filename" /></p>
   <p><input type = "submit" value = "Upload" /></p>
   </form>
</body>
</html>
"""



from upload_validator import FileTypeValidator
from django.core.exceptions import ValidationError
import os
import oletools.oleid 		#to check malware
import uuid					#to generate unique id
import cgi 					

form = cgi.FieldStorage()

File = form['filename']    	#reading filename from html form
uploadedFile = open(File) 	#reading a file

type_validator = FileTypeValidator(
	allowed_types=['application/vnd.ms-excel'], 		#to check MIME-type
	allowed_extensions=['.xlsx','.xls','xlt','xla'])	#to check extentions

def validate_size(File):
    file_size = os.path.getsize(File)	#to get size of the file
    limit_kb = 10						#MAX limit of uploaded file
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb) #raise Error if uploaded file size > required

type_validator(uploadedFile)  	#to validate file type
print("Correct Type")
validate_size(File)				#to validate file size
print("Correct Size")

oid = oletools.oleid.OleID(File)	# checking malware
indicators = oid.check()
MalwareFlag = 0
for i in indicators:
	if i.value == True:			#Malware present if value = true
		raise ValidationError("Malware found")

print("No Malware found. Changing name of the file and storing")
newName = str(uuid.uuid4())		#generate unique name
os.rename(File,newName)			#rename the uploaded file
print("Name Changed. Unique name assigned.")

import boto3					
S3 = boto3.client('s3')			# Create an S3 client

SOURCE_FILENAME = 'filename'
BUCKET_NAME = 'bucket-name'
S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, SOURCE_FILENAME)	#upload file in aws s3
