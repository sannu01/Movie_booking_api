from flask import request, jsonify
from flask_restful import Resource, Api
from flask_apscheduler import APScheduler
from datetime import datetime
from config import mysql
from app import app

api = Api(app)

class movie(Resource):
    def post(self):
        try:
            data=request.json
            name=data['name']
            phone=data['phone']
            timing=data['timing']
            timing=datetime.strptime(timing,'%d-%m-%Y %H:%M:%S')
            
            if name and phone and timing:
                diff=timing-datetime.now()
                diff=diff.total_seconds()
                if diff>0:
                    mydb=mysql.connect()
                    cursor=mydb.cursor()
                    sq="insert into movie(name,phone,timing,status) values(%s,%s,%s,%s)"
                    val=(name,phone,timing,"active")
                    csq=("select * from movie where timing=%s")
                    cval=(timing,)
                    cursor.execute(csq,cval)
                    result=cursor.fetchall()
                    if len(result)<20:
                        cursor.execute(sq,val)
                        mydb.commit()
                    else:
                        return {"message":"No seats available"}
                    
                    msg={
                        "message":"Booked ticket successfully"
                        }
                    
                    sqid="select * from movie order by ticketid desc limit 1"
                    cursor.execute(sqid)
                    result=cursor.fetchall()
                    data['ticketid']=result[0][0]
                    
                    msg['data']=data
                    cursor.close()
                    mydb.close()
                    return msg
                else:
                    return {"message":"can't book for a past time"}
                
            else:
                return {"message":"Invalid data format"}
            
        except Exception as e:
            print(e)
            cursor.close()
            mydb.rollback()
            mydb.close()
            
            return {"message":"something went wrong"}
        
class update_ticket(Resource):
    def put(self):
        try:
            data=request.json
            ticketid=data['ticketid']
            timing=data['timing']
            timing=datetime.strptime(timing,'%d-%m-%Y %H:%M:%S')
            
            if ticketid and timing:
                diff=timing-datetime.now()
                diff=diff.total_seconds()
                
                if diff>0:
                    mydb=mysql.connect()
                    cursor=mydb.cursor()
                    sq="select ticketid,name,phone from movie where ticketid=%s"
                    val=(ticketid,)
                    cursor.execute(sq,val)
                    query=cursor.fetchall()
                    
                    if len(query)>0:
                        sq="update movie set timing=%s where ticketid=%s"
                        val=(timing,ticketid)
                        cursor.execute(sq,val)
                        mydb.commit()
                        
                        result={"message":"ticket timing updated successfully"}
                        out={}
                        
                        out['ticketid']=query[0][0]
                        out['name']=query[0][1]
                        out['phone']=query[0][2]
                        out['timing']=timing
                        result['data']=out
                        cursor.close()
                        mydb.close()
                        return jsonify(result)
                    else:
                        return {"message":"no ticket found with given ticket id"}
                    
                else:
                    return {"message":"can't update to a past time"}
            else:
                return {"message":"invalid data format"}
        
        except Exception as e:
            print(e)
            return {"message":"something went wrong"}
        
class view_ticket(Resource):
    def get(self,timing):
        try:
            mydb=mysql.connect()
            cursor=mydb.cursor()
        
            sq="select ticketid,timing from movie where timing=%s"
            timing=datetime.strptime(timing,'%d-%m-%Y %H:%M:%S')
            val=(timing,)
        
            cursor.execute(sq,val)
            query=cursor.fetchall()
            out=[]
            for i in query:
                temp={}
                temp['ticketid']=i[0]
                temp['timing']=i[1]
                out.append(temp)
            result={}
            result['data']=out
            cursor.close()
            mydb.close()
            return jsonify(result)
        except Exception as e:
            print(e)
            cursor.close()
            mydb.close()
            
            return {"message":"something went wrong"}
        
class user(Resource):
    def get(self,ticketid):
        try:
            mydb=mysql.connect()
            cursor=mydb.cursor()
            sq="select name,phone from movie where ticketid=%s"
            val=(ticketid,)
            cursor.execute(sq,val)
            query=cursor.fetchall()
            if len(query)>0:
                out={}
                out['name']=query[0][0]
                out['phone']=query[0][1]
                
                result={}
                result['data']=out
                
                mydb.close()
                cursor.close()
                return jsonify(result)
            else:
                mydb.close()
                cursor.close()
                
                return {"message":"ticket id not found"}
            
        except Exception as e:
            print(e)
            cursor.close()
            mydb.close()
            
            return {"message":"something went wrong"}


class delete_ticket(Resource):
    def delete(self,ticketid):
        try:
            mydb=mysql.connect()
            cursor=mydb.cursor()
            sq="delete from movie where ticketid=%s"
            val=(ticketid,)
            csq="select * from movie where ticketid=%s"
            
            cursor.execute(csq,val)
            query=cursor.fetchall()
            if len(query)>0:
                cursor.execute(sq,val)
                mydb.commit()
                
                cursor.close()
                mydb.close()
                
                return {"message":"ticket deleted successfully"}
            else:
                cursor.close()
                mydb.close()
                
                return {"message":"no ticket found with given ticket id"}
            
        except Exception as e:
            print(e)
            cursor.close()
            mydb.rollback()
            mydb.close()
            
            return {"message":"something went wrong"}
start=0
def start_id():
    mydb=mysql.connect()
    mycursor=mydb.cursor()
    global start
    isq="select * from movie order by ticketid asc limit 1"
    mycursor.execute(isq)
    query=mycursor.fetchall()
    if len(query)>0:
        start=query[0][0]
    else:
        start=1
    
def delete_expired():
    global start
    if start==0:
        start_id()
   
    mydb=mysql.connect()
    mycursor=mydb.cursor()
    sq="select * from movie where ticketid between %s and %s order by ticketid asc"
    val=(start,start+100)
    mycursor.execute(sq,val)
    result=mycursor.fetchall()
    count=0
    for x in result:
        temp=datetime.now()-x[3]
        temp=temp.total_seconds()
        temp/=3600
        if temp>8:
            sq=("delete from movie where timing=%s")
            val=(x[3],)
            mycursor.execute(sq,val)
            mydb.commit()
            count+=1
    print(count,"Expired ticket deleted")
    if len(result)<100:
        start_id()
    else:
        start+=100
        
            
api.add_resource(user,"/user/<ticketid>")
api.add_resource(movie,"/book")
api.add_resource(view_ticket,"/view_ticket/<timing>")
api.add_resource(update_ticket,"/update_time")
api.add_resource(delete_ticket,"/delete_ticket/<ticketid>")
        
if __name__ =="__main__":
    scheduler=APScheduler()
    scheduler.add_job(func=delete_expired,trigger='interval',id='expire',seconds=100)
    scheduler.start()
    app.run(port=8000)
    scheduler.shutdown()
    




        