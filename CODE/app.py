from flask import Flask, render_template, request, Response, stream_with_context, Response, flash, redirect, url_for, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import shutil
import cv2
import math
import os
import smtplib
import json
import re
import time
import subprocess
import random
import pymongo
import socket
import argparse

import sys
#sys.path.insert(0, 'pythonfiles/')
#import own_model
from utils import emails
from utils import own_model_new

app = Flask(__name__)
app.secret_key = b"asdfasdfasdfasdfasdf" #key to hash the password

# @app.errorhandler(404)
# def pagenotfound(e):
#     return render_template("404.html")

# @app.errorhandler(500)
# def badgateway(e):
#     return render_template("404.html")


# @app.errorhandler(502)
# def badgateway1(e):
#     return render_template("404.html")


@app.route("/")
def index():
    if "user_email" in session:
        return redirect(url_for("welcome"))
    else:
        return render_template("index.html")


@app.route("/welcome",methods=["GET","POST"])
def welcome():
    if "user_email" in session:
        email=session["user_email"]
        email1=email.split("@")
        return render_template("welcome.html",email=email1[0],user_email_id=email)
    else:
        return redirect(url_for("index"))


@app.route("/welcome/logout")
def logout():
    if "user_email" in session:
        email=session["user_email"]
        x=False
        try:
            emailQuery={"email":email}
            for i in mongoCollectionDetails.find(emailQuery):
                if i["email"]==email:
                    x=True
                else:
                    success=False
                    error="User not registered"
                    return jsonify(status=success,error=error)
        except:
            success=False
            message="MongoDB server error"
            return jsonify(status=success,message=message)

        if x==True:
            session.pop("user_email", None)
            try:
                dataCollectionDetailsQuery={ 
                    "email": email 
                }
                dataCollectionDetailsNewValues={ 
                    "$set": { 
                        "user_state": False
                    } 
                }
                mongoCollectionDetails.update_one(dataCollectionDetailsQuery,dataCollectionDetailsNewValues)
            except:
                success=False
                error="MongoDB server error!"
                return jsonify(status=success,error=error)
        else:
            session.pop("user_email", None)
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/registration",methods=["POST","GET"])
def registration():
    if request.method == "POST":
        print("In Registration")
        #Data
        email=request.form["user_email"]
        password=request.form["user_password"]
        password=generate_password_hash(password)
        pin=random.randint(100000,999999)
        verification=False
        user_state=False
        x=True

        #Database Interaction
        try:
            emailQuery={"email":email}
            for i in mongoCollectionDetails.find(emailQuery):
                if i["email"]==email:
                    success=False
                    error="User already registered!"
                    x=False
                    return jsonify(status=success,error=error)
        except:
            success=False
            error="MongoDB server error"
            return jsonify(status=success,error=error)

        if x==True:
            try:
                dataCollectionDetailsInsertValues={
                    "email":email,
                    "password":password,
                    "pin":pin,
                    "verification":verification,
                    "user_state":user_state
                }
                dataCollectionHistoryInsertValues={
                    "email" : email,
                    "history" : []
                }
                resultCollectionDetails=mongoCollectionDetails.insert_one(dataCollectionDetailsInsertValues)
                resultCollectionHistory=mongoCollectionHistory.insert_one(dataCollectionHistoryInsertValues)
                print(resultCollectionDetails)
                print(resultCollectionHistory)
                if resultCollectionDetails.inserted_id is not None:
                    if resultCollectionHistory.inserted_id is not None:
                        #Verification Email
                        emailhash=generate_password_hash(email)
                        link="http://"+host_ip+":80/emailverification/"+emailhash+"/"+email
                        subject="Account Verification"
                        body="""
                        <html>
                            <head>
                            </head>
                            <body style="background-color: #349FEE; color: #FFFFFF; width: 100%; height: 100%;max-width: 900px; padding-bottom:10px;">
                                <center><h1 style="padding: 10px">Anti-Smokify Team</h1></center>
                                <h4 style="padding: 10px;">Please <a href="""+link+""">Click Here</a> to verify email and account for anti-smokify</h4>
                            </body>
                        </html>"""
                        emails.emailtouser(email,subject,body)
                        success=True
                        return jsonify(status=success)
                    else:
                        success=False
                        error="MongoDB server error"
                        return jsonify(status=success,error=error)
                else:
                    success=False
                    error="MongoDB server error"
                    return jsonify(status=success,error=error)
            except:
                success=False
                error="MongoDB server error"
                return jsonify(status=success,error=error)
        else:
            success=False
            error="An error occured!"
            return jsonify(status=success,error=error)
    else:
        return redirect(url_for("index"))


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        email=request.form["user_email"]
        password=request.form["user_password"]
        x=False

        try:
            emailQuery={"email":email}
            for i in mongoCollectionDetails.find(emailQuery):
                if i["email"]==email:
                    x=True
                    userDetails=i
                else:
                    success=False
                    error="User not registered"
                    return jsonify(status=success,error=error)
        except:
            success=False
            message="MongoDB server error"
            return jsonify(status=success,message=message)

        if x:
            verified=userDetails["verification"]
            if verified:
                #if not userDetails["user_state"]:
                if True:
                    password1=userDetails["password"]
                    password1=check_password_hash(password1,password)

                    if password1:
                        session["user_email"]=email
                        try:
                            dataCollectionDetailsQuery={ 
                                "email": email 
                            }
                            dataCollectionDetailsNewValues={ 
                                "$set": { 
                                    "user_state": True 
                                } 
                            }
                            mongoCollectionDetails.update_one(dataCollectionDetailsQuery,dataCollectionDetailsNewValues)
                        except:
                            success=False
                            error="MongoDB Server Error"
                            return jsonify(status=success,error=error)

                        success=True
                        return jsonify(status=success)
                    else:
                        success=False
                        error="Incorrect Password!"
                        return jsonify(status=success,error=error)
                else:
                    success=False
                    error="You are logged in some other browser or tab!. First logout from all your session and login again"
                    return jsonify(status=success,error=error)
            else:
                success=False
                error="User not verified!"
                return jsonify(status=success,error=error)
        else:
            success=False
            error="User is not registered!"
            return jsonify(status=success,error=error)
    else:
        return redirect(url_for("index"))


@app.route("/forgotpasswordkey",methods=["POST","GET"])
def forgotpasswordkey():
    if request.method == "POST":
        email=request.form["user_email"]
        x=False

        try:
            emailQuery={"email":email}
            for i in mongoCollectionDetails.find(emailQuery):
                if i["email"]==email:
                    x=True
                    userDetails=i
                else:
                    success=False
                    error="User not registered"
                    return jsonify(status=success,error=error)
        except:
            success=False
            message="MongoDB server error"
            return jsonify(status=success,message=message)

        if x==True:
            email=request.form["user_email"]
            pin=userDetails["pin"]
            subject="Forgot Password Pin"
            body="""
            <html>
                <head>
                </head>
                <body style="background-color: #349FEE; color: #FFFFFF; width: 100%; height: 100%;max-width: 900px; padding-bottom:10px;">
                    <center><h1 style="padding: 10px">Anti-Smokify Team</h1></center>
                    <h4 style="padding: 10px;">Please enter the following key in the form to change the password {}</h4>
                </body>
            </html>""".format(pin)
            emails.emailtouser(email,subject,body)

            success=True
            return jsonify(status=success)
        else:
            success=False
            error="User not registered!"
            return jsonify(status=success,error=error)
    else:
        return redirect(url_for("index"))


@app.route("/forgotpassword",methods=["POST","GET"])
def forgotpassword():
    if request.method == "POST":
        email=request.form["user_email"]
        x=False
        try:
            emailQuery={"email":email}
            for i in mongoCollectionDetails.find(emailQuery):
                if i["email"]==email:
                    x=True
                    userDetails=i
                else:
                    success=False
                    error="User not registered"
                    return jsonify(status=success,error=error)
        except:
            success=False
            message="MongoDB server error"
            return jsonify(status=success,message=message)

        if x==True:
            pin=request.form["user_pin"]
            password=request.form["user_password"]
            databasepin=str(userDetails["pin"])
            if pin!=databasepin:
                success=False
                error="Incorrect Pin!"
                return jsonify(status=success,error=error)
            elif pin==databasepin:
                newpin=random.randint(100000,999999)
                password=generate_password_hash(password)
                try:
                    dataCollectionDetailsQuery={ 
                        "email": email 
                    }
                    dataCollectionDetailsNewValues={ 
                        "$set": { 
                            "pin": newpin ,
                            "password":password
                        } 
                    }
                    mongoCollectionDetails.update_one(dataCollectionDetailsQuery,dataCollectionDetailsNewValues)
                    success=True
                    return jsonify(status=success)

                except:
                    success=False
                    error="MongoDB server error!"
                    return jsonify(status=success,error=error)
        else:
            success=False
            error="User not registered!"
            return jsonify(status=success,error=error)
    else:
        return redirect(url_for("index"))


@app.route("/deleteuser",methods=["POST","GET"])
def deleteuser():
    if request.method == "POST":
        if "user_email" in session:
            email=session["user_email"]
            try:
                dataCollectionDetailsQuery = { 
                    "email": email
                }
                mongoCollectionDetails.delete_one(dataCollectionDetailsQuery)
                mongoCollectionHistory.delete_one(dataCollectionDetailsQuery)
                success=True
                return jsonify(status=success)
            except:
                success=False
                error="MongoDB server error!"
                return jsonify(status=success,error=error)
        else:
            success=False
            error="Session expired!"
            return jsonify(status=success,error=error)
    else:
        return redirect(url_for("index"))


@app.route("/emailverification/<string:hashemail>/<string:orgemail>",methods=["GET"])
def emailverification(hashemail,orgemail):
    x=False
    #Database Interaction
    email=orgemail
    try:
        emailQuery={"email":email}
        for i in mongoCollectionDetails.find(emailQuery):
            if i["email"]==email:
                x=True
    except:
        return render_template("error.html")

    if x==True:
        try:
            dataCollectionDetailsQuery={ 
                "email": email 
            }
            dataCollectionDetailsNewValues={ 
                "$set": { 
                    "verification": True 
                } 
            }
            mongoCollectionDetails.update_one(dataCollectionDetailsQuery,dataCollectionDetailsNewValues)
        except:
            return render_template("verificationerror.html")
        return render_template("verified.html")
    else:
        return render_template("verificationerror.html")

@app.route("/timeline", methods=["GET"])
def timeline():
    return render_template("dashboard.html")

@app.route("/dashboard",methods=["GET"])
def dashboard():
    email=session["user_email"]
    x=False
    try:
        emailQuery={"email":email}
        for i in mongoCollectionHistory.find(emailQuery):
            if i["email"]==email:
                x=True
                userDetails=i
            else:
                return render_template("welcome.html")
    except:
        return render_template("welcome.html")

    if x==True:
        data = userDetails["history"]
        success=True
        print("returned")
        finalfinalist=[]
        folders=os.listdir("static/photos/")
        email=session["user_email"]
        folders1=[]
        for i in folders:
            if email in i:
                folders1.append("static/photos/"+i+"/")
        folders1=sorted(folders1)
        x,y,z,w=[],[],[],[]
        for i in folders1:
            x.append(os.listdir(i))
        for i in x:
            y.append(sorted(i))
        t=0
        for i in y:
            z=[]
            for j in i:
                z.append(folders1[t]+j)
            w.append(z)
            t+=1
        t=0
        for i in w:
            final=[]
            for j in i:
                u=[]
                for i in os.listdir(j):
                    u.append(j+"/"+i)
                final.append(u)
            finalfinalist.append(final)
        return jsonify(status=success,data=data,photos=finalfinalist)
    else:
        success=True
        error="No data available"
        return jsonify(status=success,error=error)


@app.route("/upload",methods=["GET","POST"])
def upload_file():
    if "user_email" in session:
        if request.method == "POST":
            ################################################# Saving the Video #############################################
            currenttime = str(int(time.time()))
            folder_path="videos/"
            app.config["UPLOAD_FOLDER"] = folder_path
            email = request.form["email"]
            file = request.files["user_file"]
            filename = file.filename[0:-4:1]+request.form["email"]+currenttime+".mp4"
            filename1 = file.filename[0:-4:1]
            filenamewoext=file.filename[0:-4:1]+request.form["email"]+currenttime

            if file:
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            ################################################# Confirmation to user #########################################
            email=request.form["email"]
            subject="Processing"
            body="""
            <html>
                <head>

                </head>
                <body style="background-color: #349FEE; color: #FFFFFF; width: 100%; height: 100%;max-width: 900px; padding-bottom:10px;">
                    <center><h1 style="padding: 10px">Anti-Smokify Team</h1></center>
                    <h4 style="padding: 10px;">The video: "<i>{}</i>" is being processed. \n Results will be emailed to you soon </h4>
                </body>
            </html>""".format(filename1)
            emails.emailtouser(email,subject,body)

            ################################################# Video to Frame #########################################
            pwd=os.getcwd()
            os.mkdir("frames/"+filenamewoext)
            videoFile = pwd+"/videos/"+filename
            subprocess.call('ffmpeg -i "'+ videoFile +'" -vf fps='+os.environ["FPS"] +' frames/"'+filenamewoext+'"/frame%04d.jpg -hide_banner',shell=True)
            # count=0
            # cap = cv2.VideoCapture(videoFile)
            # frameRate = cap.get(5)
            # while(cap.isOpened()):
            #     frameId = cap.get(1)
            #     ret, frame = cap.read()
            #     if (ret != True):
            #         break
            #     if (frameId % math.floor(frameRate) == 0):
            #         cv2.imwrite("frames/"+filenamewoext+"/frame{}.jpg".format(count), frame)
            #         count+=1


            ################################################# Predicting Frames ############################################
            smokingimages=[]
            timestampfinal=[]
            path=os.getcwd()
            path = path+'/frames/'+filenamewoext
            #use_yolo.predict(path)
            status=os.listdir(path)
            smokingimages = own_model_new.predict(path, model)

            # i=0
            # smokingimages=[]
            # teach_url="http://localhost:8080/classificationbox/models/5c492e65b0faf119/predict"
            # predictingimages=os.listdir("frames/"+filenamewoext)
            # while i<len(predictingimages):
            #     path=os.getcwd()
            #     path=path+"/frames/"+filenamewoext+"/"+predictingimages[i]
            #     x=prediction.predict(teach_url,path)
            #     if x=="smoking":
            #         smokingimages.append(predictingimages[i])
            #         i+=1
            #     elif x=="not_smoking":
            #         i+=1

            if not smokingimages:
                success=False
                data="No smoking scenes"

                subject="Results"
                body="""
                <html>
                    <head>
                    </head>
                    <body style="background-color: #349FEE; color: #FFFFFF; width: 100%; height: 100%; max-width: 900px; padding-bottom:10px;">
                        <center><h1 style="padding: 10px">Anti-Smokify Team</h1></center>
                        <h4 style="padding: 10px;">There are no smoking scenes in "<i> """+filename1+""" </i>"<br/></h4>
                    </body>
                </html>"""
                emails.emailtouser(email,subject,body)
                #shutil.rmtree("frames/"+filenamewoext)
                os.remove("videos/"+filename)
                return jsonify(status=success,data=data)

            else:


                ################################################ Creating Scenes ############################################
                os.mkdir("static/photos/"+filenamewoext)
                smokingimages1=[]
                for i in smokingimages:
                    shutil.copy("frames/"+filenamewoext+"/"+i, "static/photos/"+filenamewoext)
                    # framepath = os.path.join("frames/"+filenamewoext+"/",i)
                    # os.rename(framepath,"static/photos/"+filenamewoext+"/"+i)
                    #z=filenamewoext+"/"+i
                    #smokingimages1.append("static/photos/{}".format(z))


                start = 0
                end = 1
                scene_no = 1
                scene_path = 'static/photos/'+filenamewoext
                images = os.listdir(scene_path)
                total_frames = len(images)

                num,num1=[],[]
                for i in images:
                    num.append(re.findall(r'[0-9]+',i))

                for i in range(0,len(num)):
                    num1.append(int(num[i][-1]))

                for i in range(len(num1)):
                    for j in range(len(num1)-i-1):
                        if num1[j]>num1[j+1]:
                            num1[j],num1[j+1]=num1[j+1],num1[j]
                            images[j],images[j+1]=images[j+1],images[j]

                def create_new_scene(st_frame):
                    print('--------NEW SCENE CREATED-----------')
                    os.mkdir(scene_path+'/Scene'+str(scene_no))
                    shutil.move(scene_path+'/'+images[st_frame], scene_path+'/Scene'+str(scene_no))

                create_new_scene(start)

                while end < total_frames:
                    st_sec = int(re.findall("\d+", images[start])[0])
                    end_sec = int(re.findall('\d+', images[end])[0])
                    sec_diff = end_sec - st_sec
                    if sec_diff < 7:
                        shutil.move(scene_path+'/'+images[end], scene_path+'/Scene'+str(scene_no))
                        start += 1
                        end += 1
                    else:
                        start += 1
                        end += 1
                        scene_no += 1
                        create_new_scene(start)

                all_scenes = [scene for scene in os.listdir(scene_path)]


                for each_scene in all_scenes:
                    smoking_frames = [f for f in os.listdir(scene_path+'/'+each_scene)]
                    smoking_scene_images1=[]
                    for each_smoking_frame in smoking_frames:
                        smoking_scene_images1.append(scene_path+'/'+each_scene+'/'+each_smoking_frame)
                    smokingimages1.append(smoking_scene_images1)

                ####################################### Sorting images #################################################
                num,num1=[],[]
                for i in smokingimages1:
                    num0=[]
                    for j in i:
                        number=re.findall(r'[0-9]+',j)
                        num0.append(number)
                    num.append(num0)

                for i in range(0,len(num)):
                    num0=[]
                    for j in range(0,len(num[i])):
                        num0.append(int(num[i][j][-1]))
                    num1.append(num0)

                count=0
                smokingimages_final,smokingimages_final_finalist=[],[]
                for numtemp in num1:
                    smokingimages_temp=smokingimages1[count]
                    for i in range(len(numtemp)):
                        for j in range(len(numtemp)-i-1):
                            if numtemp[j]>numtemp[j+1]:
                                numtemp[j],numtemp[j+1]=numtemp[j+1],numtemp[j]
                                smokingimages_temp[j],smokingimages_temp[j+1]=smokingimages_temp[j+1],smokingimages_temp[j]
                    smokingimages_final.append(smokingimages_temp)
                    count+=1

                ################################################# Calculating timestamp #########################################
                timestamp=[]
                for i in smokingimages_final:
                    timestamp1=[]
                    timestamp1.append(int(i[0][-8:-4:1]))
                    timestamp1.append(int(i[-1][-8:-4:1]))
                    timestamp.append(timestamp1)
                timestamp=sorted(timestamp)
                for i in timestamp:
                    timestamp1=[]
                    for j in i:
                        hour=j//3600
                        j=j%3600
                        minutes=j//60
                        j=j%60
                        seconds=j
                        final="{}:{}:{}".format('%02d' %hour,'%02d' %minutes,'%02d' %seconds)
                        timestamp1.append(final)
                    timestampfinal.append(timestamp1)

                
                subject="Results"
                body="""
                <html>
                    <head>
                    </head>
                    <body style="background-color: #349FEE; color: #FFFFFF; width: 100%; height: 100%; max-width: 900px; padding-bottom:10px;">
                        <center><h1 style="padding: 10px">Anti-Smokify Team</h1></center>
                        <h4 style="padding: 10px;">The timestamps of smoking scenes of: "<i> """+filename1+""" </i>" video is as follows:<br/></h4>
                        <ul>
                    """
                for i in timestampfinal:
                    body+="""<li style="padding-inline-start: 0px;color: #FFFFFF">Smoking scene at """ +i[0]+ """ to """ + i[1] + """</li>"""
                body+="""</ol></body</html>"""
                emails.emailtouser(email,subject,body)
                
                ############################################### Storing History #################################################
                description = request.form["description"]
                filename1 = file.filename[0:-4:1]
                x=False
                print(email,description)
                try:
                    x = mongoCollectionHistory.find_one({"email":email})
                    print("Result:",x)
                    # for i in x:
                    #     print("Query:",i)
                    #     if i["email"]==email:
                    #         x=True
                    #         userDetails=i
                    #     else:
                    #         return render_template("welcome.html")
                except:
                    success=False
                    error="MongoDB Server Error!"
                    return jsonify(success=success,error=error)
                
                userDetails = x
                print("akldkald:",userDetails)
                y=userDetails["history"]
                print("y",y)
    
                data = [{"starttime":i[0],"endtime":i[1]} for i in timestampfinal]
                # data = {
                #     filename1: data
                # }
                dataCollectionHistoryInsertValues={
                        "description": description,
                        filename1: data,
                    }
                print("Data",data)
                finaldata=userDetails["history"] 
                finaldata.append(dataCollectionHistoryInsertValues)
                print("finaldata",finaldata)
                try:
                    
                    mongoCollectionHistory.update_one({"email":email},{"$set":{"history":finaldata}})
                except:
                    success=False
                    error="MongoDB Server Error!"
                    return jsonify(success=success,error=error)

                ################################################# Selecting 9 images ############################################
                for i in smokingimages_final:
                    x=len(i)
                    if x>=9:
                        x=i[:9]
                        smokingimages_final_finalist.append(x)
                    else:
                        smokingimages_final_finalist.append(i)
                smokingimages_final_finalist=sorted(smokingimages_final_finalist)

                ################################################# Deleting data #################################################
                shutil.rmtree("frames/"+filenamewoext)
                os.remove("videos/"+filename)

                ################################################# Returning data ###############################################
                data=json.dumps([{"filepath": filepath} for filepath in smokingimages_final_finalist])
                data=json.loads(data)
                success=True
                return jsonify(status=success,data=data,timestampfinal=timestampfinal)
        else:
            return redirect(url_for('index'))    
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default="cnn")
    args = parser.parse_args()
    model = args.model
    host_name = socket.gethostname() 
    host_ip = socket.gethostbyname(host_name)
    mongoClient=pymongo.MongoClient("mongodb://"+os.environ["IP"]+":27017/")
    mongoDb=mongoClient["anti-smokify"]
    mongoCollectionDetails=mongoDb["user_details"]
    mongoCollectionHistory=mongoDb["user_history"]
    print(mongoCollectionHistory)
    print("------CHECKING DB STATUS MANUALLY--------")
    emailQuery={"email":"jaynil123@gmail.com"}
    for i in mongoCollectionDetails.find(emailQuery):
                if i["email"]==email:
                    pass
                    # User  registered
                else:
                    pass
                    # User not registered
    print("-------DB STATUS success-----")
    app.run(debug = True,host=host_ip,port=80, threaded=True)
