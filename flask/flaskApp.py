from TikTokApi import TikTokApi
from flask import Flask,request,jsonify
import requests
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'logger'))
import TiktokViewStats
import myLogger
import re
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
import time 

# url_stats = 'https://tiktok.livecounts.io/user/stats/'
# def getPostStatTiktok(link):
#     stats = {}
#     try :
#         api = TikTokApi()
#         video = api.video(url=link)
#         # print(video.stats)
#         stats['like'] = video.stats['diggCount']
#         stats['views'] = video.stats['playCount']
#         stats['share'] = video.stats['shareCount']
#         user_id = video.author.user_id
#         resp = requests.get('https://tiktok.livecounts.io/user/stats/' + str(user_id))
#         if resp.status_code == 200:
#             resp_obj = resp.json()
#             stats['follower'] = resp_obj['followerCount']
#     except Exception as e:
#         print("error:",e)
#         #myLogger.logging_error("flask","got exception when getPostStatTiktok : ",e)  
#     return stats

USER_DATA = {
    "admin": "SuperSecretPwd"
}

app = Flask(__name__)
CORS(app)
# auth = HTTPBasicAuth()

# @auth.verify_password
# def verify(username, password):
#     if not (username and password):
#         return False
#     return USER_DATA.get(username) == password

@app.route('/getTiktokVideoStats/', methods=['GET','POST'])
# @auth.login_required
def getTiktokVideoStats():
    resp = {'status':False}
    body = request.json
    myLogger.logging_info('flask','/getTiktokVideoStats/','body:',body)
    url = body['video_url']
    
    username = ''
    video_id = ''
    try:
        print("url lama", url)
        if "@" not in url:
            url  = TiktokViewStats.livecounts.getIdFromLongUrl(url)
        print("url baru", url)
        # username, video_id = re.findall(r'(@[a-zA-z0-9]*)\/.*\/([\d]*)?',url)[0]
        regexResult = url.split("/")
        username = regexResult[3]
        uncutId = regexResult[5].split("?")
        video_id = uncutId[0]
    except Exception as e:
        myLogger.logging_error('flask','got exc when extract video id:',e)
        resp['message'] = 'failed to extract video id'
        resp['status'] = '201'

    if username != '' and video_id != '':
        try:
            stats = TiktokViewStats.livecounts.video_info(video_id)
            print("ini stats", stats)
            if stats is not None:
                resp['status'] = True
                resp['message'] = 'success'
                resp['data'] = stats
            else :
                resp['message'] = 'empty data'
                resp['status'] = '202'
        except Exception as e:
            print("error",e)
            myLogger.logging_error('flask','got exc when get video stats:',e)
            resp['message'] = 'failed to get video stats'
            resp['status'] = '203'

    response = jsonify(resp)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type', 'application/json')
    # response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    return response

@app.route('/getCPM/', methods=['POST'])
# @auth.login_required
def getCPM():
    resp = {'status':False}
    body = request.json
    myLogger.logging_info('flask','/getCPM/','body:',body)
    username = body['username']
    cost = body['cost']

    listVideo = []

    try:
        listVideo = TiktokViewStats.getListVideoFromTiktokUser(username)
    except Exception as e:
        myLogger.logging_error('flask','got exc when get list video :',e)
        
    
    if len(listVideo) == 0 :
        resp['message'] = 'failed to get list video of users'
        resp['status'] = '201'
    elif cost <=0:
        resp['message'] = 'cost must be a positive amount'
        resp['status'] = '202'
    else:
        #print(listVideo)
        videoStats = []
        totalCount = 0
        totalViews = 0
        for videoId in listVideo:
            try:
                videoStatsAndData = TiktokViewStats.getVideoDataAndStats(videoId,username)
                # video_stats = TiktokViewStats.livecounts.video_info(videoId)
                # video_data = TiktokViewStats.livecounts.video_data(videoId)
                if videoStatsAndData['stats']['playCount'] > 0:
                    cpm = cost/videoStatsAndData['stats']['playCount']
                else:
                    cpm = 0
                videoStatsAndData['cpm'] = cpm
                #createTime = TiktokViewStats.getCreatedTime(videoId,username)
                #videoStats.append({'id':videoId,'stats':video_stats,"title":video_data["title"],"cpm":cpm,"createTime":createTime,"cover":video_data["cover"]})
                videoStats.append(videoStatsAndData)
                totalCount += 1
                totalViews += videoStatsAndData['stats']['playCount']
                #time.sleep(0.1)
            except Exception as e:
                myLogger.logging_error('flask','got exc when get video stats:',e)

        resp['videoStats'] = videoStats
        if totalViews > 0 and totalCount > 0:
            resp['avgView'] = totalViews/totalCount
            resp['avgCpm'] = cost / (totalViews/totalCount)
        resp['username'] = username
        resp['status'] = True
            
    response = jsonify(resp)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type', 'application/json')
    return response

@app.route('/getUserInfo/', methods=['GET','POST'])
# @auth.login_required
def getUserInfo():
    resp = {'status':False}
    body = request.json
    myLogger.logging_info('flask','/getUserInfo/','body:',body)
    username = body['username']

    if username == '':
        resp['message'] = 'username cannot be empty'
        resp['status'] = '201'
    else:
        try:
            respSearch = TiktokViewStats.livecounts.user_search(username)
            myLogger.logging_info('flask','respSearch:',respSearch)
            users = respSearch['userData']
            found = False
            for user in users:
                if user['id'] == username:
                    found = True
                    resp['userData'] = user
            if not found :
                resp['message'] = 'username not found'
                resp['status'] = '202'
        except Exception as e:
            myLogger.logging_error('flask','got exc when get user info:',e)
    
    response = jsonify(resp)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type', 'application/json')
    # response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    return response

@app.route('/getTiktokVideoWithUserStats/', methods=['GET','POST'])
# @auth.login_required
def getTiktokVideoWithUserStats():
    resp = {'status':False}
    body = request.json
    myLogger.logging_info('flask','/getTiktokVideoWithUserStats/','body:',body)
    url = body['video_url']
    
    username = ''
    video_id = ''
    try:
        print("url lama", url)
        if "@" not in url:
            url  = TiktokViewStats.livecounts.getIdFromLongUrl(url)
        print("url baru", url)
        regexResult = url.split("/")
        username = regexResult[3]
        uncutId = regexResult[5].split("?")
        video_id = uncutId[0]
        # username, video_id = re.findall(r'(@[a-zA-z0-9]*)\/.*\/([\d]*)?',url)[0]
    except Exception as e:
        myLogger.logging_error('flask','got exc when extract video id:',e)
        resp['message'] = 'failed to extract video id'
        resp['status'] = '201'

    if username != '' and video_id != '':
        try:
            myLogger.logging_info('flask','video_stats')
            video_stats = TiktokViewStats.livecounts.video_info(video_id)
            print("ini video", video_stats)
            myLogger.logging_info('flask',video_stats)

            # myLogger.logging_info('flask','video_data')
            video_data = TiktokViewStats.livecounts.video_data(video_id)
            print("ini ", video_data)
            myLogger.logging_info('flask',video_data)

            user_stats = {}
            if len(video_data) > 0:
                user_id = video_data['author']['userId']
                if user_id is not None and user_id != '' : 
                    user_stats = TiktokViewStats.livecounts.user_stats(user_id)
                    print("ini user stats", user_stats)
            
            if len(video_stats) > 0 and len(user_stats)>0:
                resp['status'] = True
                resp['message'] = 'success'
                resp['data'] = {'video':video_stats,'user':user_stats,'author':video_data['author']}
                print("ini resp", resp)
            else :
                resp['message'] = 'empty data'
                resp['status'] = '202'
        except Exception as e:
            print("ex",e)
            myLogger.logging_error('flask','got exc when get video stats:',e)
            resp['message'] = 'failed to get video stats'
            resp['status'] = '203'
    
    response = jsonify(resp)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type', 'application/json')
    # response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3131)