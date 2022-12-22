from TikTokApi import TikTokApi
from flask import Flask,request,jsonify
import requests
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'logger'))
import myLogger

url_stats = 'https://tiktok.livecounts.io/user/stats/'
def getPostStatTiktok(link):
    stats = {}
    try :
        api = TikTokApi()
        video = api.video(url=link)
        # print(video.stats)
        stats['like'] = video.stats['diggCount']
        stats['views'] = video.stats['playCount']
        stats['share'] = video.stats['shareCount']
        user_id = video.author.user_id
        resp = requests.get('https://tiktok.livecounts.io/user/stats/' + str(user_id))
        if resp.status_code == 200:
            resp_obj = resp.json()
            stats['follower'] = resp_obj['followerCount']
    except Exception as e:
        print("error:",e)
        #myLogger.logging_error("flask","got exception when getPostStatTiktok : ",e)  
    return stats


app = Flask(__name__)
@app.route('/getPostStats', methods=['GET'])
def welcome():
    resp = {'status':'False'}
    myLogger.logging_info("flask"," /getPostStats:test ")
    data = request.get_json()
    myLogger.logging_info("flask"," /getPostStats: ",data)
    stats = getPostStatTiktok(data['Link'])
    if stats :
        resp['status'] = 'True'
        resp['data'] = stats
    return jsonify(resp)

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=1515)
    app.run()
    

# if __name__ == '__main__':
#     try:
#         print(getPostStatTiktok('https://vt.tiktok.com/ZSRCwvXrt/'))
#     except Exception as e:
#         print('got exception, e: ',e)

