from typing import Optional
from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from most_popular import MostPopular
import split_data
import json

client =MongoClient('mongo', port = 27017)
db = client["mydb"]
col = db["mycol"]
playlist = db["myplaylist"]
nam = db["mynam"]
lis = db["mylis"]
app = FastAPI()

@app.get("/")
async def get_hello():
    db.col.remove({})
    db.playlist.remove({})
    print("hi")
    return "hi"

@app.put("/users/")
async def put_user(uid: str, passwd: str):
    user = ({uid:passwd})
    curser = db.col.find({},{'_id':0})
    res = {}
    for x in curser:
        res.update(x)
    res.update(user)
    db.col.remove({})
    db.col.insert(res)
    return {"result":"SUCCESS"}

@app.get("/users")
async def get_user():
    res = {}
    lis = db.col.find({}, {'_id':0})
    for x in lis:
        print(x)
        res.update(x)
    return res

@app.delete("/users/")
async def delete_user(uid: str):
    res = {}
    plist = {}
    for x in db.col.find({}, {'_id':0}):
        res.update(x)
    for x in db.playlist.find({}, {'_id':0}):
        plist.update(x)
    if uid in res:
        del res[uid]
        print(res)
        db.col.remove({})
        db.col.insert(res)
        if uid in plist:
            del plist[uid]
            db.plist.remove({})
            db.plist.insert(plist)
        return {"result":"SUCCESS"}
    else:
        return {"result":"FAILED"}

@app.get("/users/_count_")
async def cnt_user():
    cnt = 0
    lis = db.col.find({}, {'_id':0})
    for x in lis:
        cnt = len(x)
        print(x)
    res = db.col.count()
    print(res)
    return {"count":cnt}

@app.put("/users/{userid}/playlist/{songid}")
async def put_song(userid: str, songid: int):
    lis = db.col.find({}, {'_id':0, 'passwd':0})
    res = {}
    plist = {}
    for x in lis:
        res.update(x)
    if userid in res:
        for x in db.playlist.find({}, {'_id':0}):
            plist.update(x)
        with open('song_meta.json', 'r') as f:
            jsonObject = json.load(f)
            for sm in jsonObject:
                if songid == sm["id"]:
                    plist.setdefault(userid, []).append(songid)
                    print(plist)
                    db.playlist.remove({})
                    db.playlist.insert(plist)
                    return {"result":"SUCCESS"}
            print("songid not matched")
            return {"result":"FAILED"}
    else:
        try:
            uid = int(userid)
        except ValueError:
            print("userid not matched")
            return {"result":"FAILED"}
        with open('train.json', 'r') as f:
            jsonObject = json.load(f)
            for tr in jsonObject:
                if uid == tr["id"]:
                    with open('song_meta.json', 'r') as g:
                        jsonObject2 = json.load(g)
                        for sm in jsonObject2:
                            if songid == sm["id"]:
                                plist.setdefault(userid, []).append(songid)
                                print(plist)
                                db.playlist.remove({})
                                db.playlist.insert(plist)
                                return {"result":"SUCCESS"}
                            else:
                                print("songid not matched")
                                return {"result":"FAILED"}
                else:
                    print("userid not matched")
                    return{"result":"FAILED"}

@app.get("/users/{userid}/playlist")
async def get_plt(userid: str):
    res = {}
    for x in db.playlist.find({}, {'_id':0}):
        res.update(x)
    if userid in res:
        ans = {userid:res[userid]}
        return ans
    else:
        with open('train.json', 'r') as f:
            jsonObject = json.load(f)
            for tr in jsonObject:
                uid = int(userid)
                if uid == tr["id"]:
                    plist = {}
                    plist.setdefault(userid, []).append(tr["songs"])
                    return plist
            print("no userid")
            return {"result":"FAILED"}

@app.get("/users/{userid}/recommendations")
async def get_rec(userid: str):
    res = {}
    for x in db.col.find():
        res.update(x)
    if userid in res:
        ans = []
        mp = MostPopular()
        ans = mp.run("train.json", "question.json")
        ans[0]["uid"] = userid
        return ans
    else:
        try:
            uid = int(userid)
        except ValueError:
            print("no userid")
            return {"result":"FAILED"}
        with open('train.json', 'r') as f:
            jsonObject = json.load(f)
            for tr in jsonObject:
                if uid == tr["id"]:
                    ans = []
                    mp = MostPopular()
                    ans = mp.run("train.json", "question.json")
                    ans[0]["uid"] = userid
                    return ans           
            return {"result":"FAILED"}

@app.get("/v2")
async def get_hi():
    print("hi")
    txt = ''
    with open('README.md', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break;
            txt += line
        return txt

@app.post("/v2/customers/{cid}")
async def post_user(cid: str):
    user = ({cid:None})
    print(user)
    res = {}
    for x in db.col.find({}, {'_id':0}):
        res.update(x)
    if cid in res:
        return {"result":"FAILED","message":f"duplicate {cid}"}
    res = {}
    for x in db.nam.find({}, {'_id':0}):
        res.update(x)
    if cid in res:
        return {"result":"FAILED","message":f"duplicate {cid}"}
    else:
        try:
            uid = int(cid)
        except ValueError:
            res.update(user)
            db.nam.remove({})
            db.nam.insert(res)
            return {"result":"SUCCESS","customer ID":cid}
        with open('train.json', 'r') as f:
            jsonObject = json.load(f)
            for tr in jsonObject:
                if uid == tr["id"]:
                    return {"result":"FAILED","message":f"duplicate {cid}"}
            res.update(user)
            db.nam.remove({})
            db.nam.insert(res)
            return {"result":"SUCCESS","customer":cid}

@app.put("/v2/customers/{cid}")
async def put_cid(cid: str, name: Optional[str] = None):
    user = ({cid:name})
    res = {}
    print(user)
    for x in db.nam.find({}, {'_id':0}):
        res.update(x)
    if cid in res:
        res.update(user)
        db.nam.remove({})
        db.nam.insert(res)
        if name == None:
            return {"result":"SUCCESS", "customer ID": f"{cid}", "name":""}
        else:
            return {"result":"SUCCESS", "customer ID": f"{cid}", "name":f"{name}"}
    else:
        with open('train.json', 'r') as f:
            jsonObject = json.load(f)
            for tr in jsonObject:
                try:
                    uid = int(cid)
                except ValueError:                   
                    return {"result":"FAILED","message":f"{cid} not found"}
                if uid == tr["id"]:
                    return {"result":"SUCCESS", "customer ID": f"{cid}", "name":""}
            return {"result":"FAILED","message":f"{cid} not found"}

@app.get("/v2/customers/{cid}")
async def get_cid(cid: str):
    user = ({cid:None})
    res = {}
    for x in db.col.find({}, {'_id':0, 'passwd':0}):
        res.update(x)
    if cid in res:
        return {"result":"SUCCESS", "customer ID": f"{cid}", "name":""}
    res = {}
    for x in db.nam.find({}, {'_id':0}):
        res.update(x)
    if cid in res:
        print(res)
        if res[cid] == None:
            print("no name")
            return {"result":"SUCCESS", "customer ID": f"{cid}", "name":""}
        else:
            print("yes name")
            return {"result":"SUCCESS", "customer ID": f"{cid}", "name":res[cid]}
    else:
        try:
            uid = int(cid)
        except ValueError:
            print("no userid")
            return {"result":"FAILED", "message":f"{cid} not found"}
        with open('train.json', 'r') as f:
            jsonObject = json.load(f)
            for tr in jsonObject:
                if uid == tr["id"]:
                    return {"result":"SUCCESS", "customer ID": f"{cid}", "name":""}
            return {"result":"FAILED", "message":f"{cid} not found"}

@app.delete("/v2/customers/{cid}")
async def delete_cid(cid: str):
    res = {}
    plist = {}
    for x in db.nam.find({}, {'_id':0}):
        res.update(x)
    for x in db.lis.find({}, {'_id':0}):
        plist.update(x)
    if cid in res:
        del res[cid]
        print(res)
        db.nam.remove({})
        db.nam.insert(res)
        if cid in plist:
            del plist[cid]
            db.lis.remove({})
            db.lis.insert(plist)
        return {"result":"SUCCESS", "customer ID": f"{cid}"}
    else:
        if cid in plist:
            del plist[cid]
            db.lis.remove({})
            db.lis.insert(plist)
            return {"result":"SUCCESS", "customer ID": f"{cid}"}
        else:
            return {"result":"FAILED", "message":f"{cid} not found"}

@app.post("/v2/customers/{cid}/listened/{sid}")
async def post_cid_sid(cid: str, sid: int):
    user = ({cid:sid})
    print(user)
    res = {}
    for x in db.col.find({}, {'_id':0}):
        res.update(x)
    for x in db.playlist.find({}, {'_id':0}):
        res.update(x)
    for x in db.nam.find({}, {'_id':0}):
        res.update(x)
    for x in db.lis.find({}, {'_id':0}):
        res.update(x)
    if cid in res:
        listen = {}
        for x in db.lis.find({}, {'_id':0}):
            listen.update(x)
        with open('song_meta.json', 'r') as f:
            jsonObject = json.load(f)
            print("json load")
            for sm in jsonObject:
                if sid == sm["id"]:
                    listen.setdefault(cid,[]).append(sid)
                    print(listen)
                    db.lis.remove({})
                    db.lis.insert(listen)
                    ans = {"customer":cid, "songs":listen[cid]}
                    return ans
            print("songid not matched")
            return {"result":"FAILED"}
    else:
        listen = {}
        try:
            uid = int(cid)
        except ValueError:
            print("no userid")
            return {"result":"FAILED", "message":f"{cid} not found"}
        with open('train.json', 'r') as f:
            jsonObject = json.load(f)
            for tr in jsonObject:
                if uid == tr["id"]:
                    with open('song_meta.json', 'r') as f:
                        jsonObject2 = json.load(f)
                        print("json load")
                        for sm in jsonObject2:
                            if sid == sm["id"]:
                                listen.setdefault(cid,[]).append(sid)
                                print(listen)
                                db.lis.remove({})
                                db.lis.insert(listen)
                                ans = {"customer":cid, "songs":listen[cid]}
                                return ans
                        print("songid not matched")
                        return {"result":"FAILED"}

@app.get("/v2/customers/{cid}/listened")
async def get_cid_lis(cid: str):
    res = {}
    for x in db.lis.find({}, {'_id':0}):
        res.update(x)
    if cid in res:
        ans = {"customer":cid, "songs":res[cid]}
        return ans
    else:
        try:
            uid = int(cid)
        except ValueError:
            print("no userid")
            return {"result":"FAILED", "message":f"{cid} not found"}
        with open('train.json', 'r') as f:
            jsonObject = json.load(f)
            for tr in jsonObject:
                if uid == tr["id"]:
                    plist = {}
                    plist.setdefault(cid, []).append(tr["songs"])
                    ans = {"customer":cid, "songs":plist[cid]}
                    return ans
            print("no userid")
            return {"result":"FAILED", "message":f"{cid} not found"}

@app.delete("/v2/customers/{cid}/listened/{sid}")
async def del_cid_sid(cid: str, sid: int):
    res = {}
    for x in db.lis.find({}, {'_id':0}):
        res.update(x)
    if cid in res:
        del res[cid][res[cid].index(sid)]
        print(res)
        db.lis.remove({})
        db.lis.insert(res)
        ans = {"customer":cid, "songs":res[cid]}
        return ans
    else:
        return {"result":"FAILED", "message":f"{cid} not found"}

@app.get("/v2/songs/{sid}")
async def put_user(sid: int):
    with open('song_meta.json', 'r') as f:
            jsonObject = json.load(f)
            for sm in jsonObject:
                if sid == sm["id"]:
                    res = {"song_id":sid,"album_id":sm["album_id"], "artists":sm["artist_id_basket"]}
                    return res
            print("songid not matched")
            return {"result":"FAILED"}

@app.get("/v2/customers/{cid}/suggestion")
async def get_sug(cid: str):
    res = {}
    for x in db.col.find({}, {'_id':0}):
        res.update(x)
    for x in db.playlist.find({}, {'_id':0}):
        res.update(x)
    for x in db.nam.find({}, {'_id':0}):
        res.update(x)
    for x in db.lis.find({}, {'_id':0}):
        res.update(x)
    if cid in res:
        ans = []
        mp = MostPopular()
        ans = mp.run("train.json", "question.json")
        ans[0]["uid"] = cid
        fin = {"customer ID": cid, "songs":ans[0]["songs"]}
        return fin
    else:
        try:
            uid = int(cid)
        except ValueError:
            return {"result":"FAILED", "message":f"{cid} not found"}
        with open('train.json', 'r') as f:
            jsonObject = json.load(f)
            for tr in jsonObject:
                if uid == tr["id"]:
                    ans = []
                    mp = MostPopular()
                    ans = mp.run("train.json", "question.json")
                    ans[0]["uid"] = cid
                    ans[0]["customer ID"] = ans[0].pop("uid")
                    fin = {"customer ID": cid, "songs":ans[0]["songs"]}
                    return fin
            return {"result":"FAILED", "message":f"{cid} not found"}

