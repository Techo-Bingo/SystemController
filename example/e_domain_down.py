import os
import socket
import sys
import threading
import time

#引入消息模块
sys.path.append(".")
import eGW650_down_msg_define as msg

# print(msg.ThirdMsg.msgRegister)
class DownDomain():
    def __init__(self,updomainIP,updomainPort,updomainGB,downdomainIP,downdomainPort,downdomainGB,cameraFile):
        self.remoteIP = updomainIP
        self.remotePort = updomainPort
        self.localIP = downdomainIP
        self.localPort = downdomainPort
        self.recvPacket = []
        msgdefin = msg.Register(updomainIP,updomainPort,updomainGB,downdomainIP,downdomainPort,downdomainGB)
        localAddressPort = (self.localIP, int(self.localPort))
        #================================transport define start================================
        #define remote IP Port
        self.eGWAddressPort = (self.remoteIP, int(self.remotePort))
        #define udpSocket
        self.sclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #define local IP Port
        self.sclient.bind(localAddressPort)
        #================================transport define end================================
        #================msg define start============================
        self.msgRegister = msgdefin.msgRegister
        self.mesCatalog = msg.CatalogRsp(updomainIP,updomainPort,updomainGB,downdomainIP,downdomainPort,downdomainGB, ).msgCatalogPacketList
        self.keepLive = msg.Keeplive(updomainIP,updomainPort,updomainGB,downdomainIP,downdomainPort,downdomainGB).keepLive
        self.notify = msg.Notify(updomainIP,updomainPort,updomainGB,downdomainIP,downdomainPort,downdomainGB).notify
        self.GisInfo = msg.GisInfo(updomainIP, updomainPort, updomainGB, downdomainIP, downdomainPort,
                                 downdomainGB).gisInfo

        #define response head
        self.responseMsgHead=["Call-ID","CSeq","From","To","Via"]
        self.responseSubHead=["Call-ID","CSeq","From","To","Via","Contact","Expires","Event"]
        self.responseInvHead=["Call-ID","CSeq","From","To","Via"]
        self.responseByeHead=["Call-ID","CSeq","From","To","Via"]
        #================msg define end============================
    def sendMsg(self, msgName, msgCtx):
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
        print("="*30 + nowTime + " send %s" % msgName + "="*30)
        msgContext=msgCtx
        self.sclient.sendto(msgContext.encode('utf-8'), self.eGWAddressPort)
    def start_domain_process(self):
        self.sendMsg("register", self.msgRegister)
        print(self.msgRegister)
        while True:
            data, addr = self.sclient.recvfrom(2048)
            info = data.decode('utf-8')
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
            #print(info)
            infoList = info.split("\r\n\r\n")
            infoHeadList = infoList[0].split("\r\n")
            if infoList[1]:
                infoBodyList = infoList[1].split("\r\n")

            #deal server response
            if infoHeadList[0] == "SIP/2.0 200 OK":
                print("+"*30 + nowTime + " recv rsp 200 OK" + "+"*30)
            # deal message packet
            elif "MESSAGE sip:" in infoHeadList[0]:
                msgType = "MESSAGE"
                responseMessage = "SIP/2.0 200 OK\r\n"
                infoend = "User-Agent: NCG V2.6.0.299939\r\nContent-Length: 0\r\n\r\n"
                sendResponseMsg = self.create_rsp_msg(msgType, responseMessage, infoHeadList, infoend)
                self.sclient.sendto(sendResponseMsg.encode('utf-8'), self.eGWAddressPort)
                if "<CmdType>Catalog</CmdType>" in infoList[1]:
                    print("+" * 30 + "recv catalog msg" + "+" * 30)
                    # th3 = threading.Thread(target=self.camera_info_send, args=[])
                    th3 = threading.Thread(target=self.multi_message_send, args=[])
                    th3.start()
                    #self.sclient.sendto(message2_Catalog, eGWAddressPort)
            # deal subscribe packet
            elif "SUBSCRIBE sip" in infoHeadList[0]:
                print("+" * 30 + nowTime + " recv subscribe msg" + "+" * 30)
                msgType = "SUBSCRIBE"
                responseMessage = "SIP/2.0 200 OK\r\n"
                infoend = "User-Agent: NCG V2.6.0.299939\r\nContent-Length: 0\r\n\r\n"
                sendResponseMsg = self.create_rsp_msg(msgType, responseMessage, infoHeadList, infoend)
                #self.sclient.sendto(sendResponseMsg.encode('utf-8'), self.eGWAddressPort)
                self.sendMsg("200 OK", sendResponseMsg)
                if "<CmdType>MobilePosition</CmdType>" in infoList[1]:
                    print("+" * 30 + nowTime + " recv MobilePosition msg" + "+" * 30)
                    th4 = threading.Thread(target=self.gis_info_send, args=[])
                    th4.start()
                if "<CmdType>Catalog</CmdType>" in infoList[1]:
                    print("+" * 30 + nowTime + " recv sub-catalog msg" + "+" * 30)
                    # th5 = threading.Thread(target=self.sendNotify(), args=[])
                    # th5.start()

            # deal invite packet
            elif "INVITE sip" in infoHeadList[0]:
                # get camera ID
                print("+" * 30 + nowTime + " recv invite msg" + "+" * 30)
                camIDcall=infoHeadList[0].split(":")[1]
                camID=camIDcall.split("@")[0]
                print(camID)
                # send try
                msgType = "INVITE"
                responseInv = "SIP/2.0 100 Trying\r\n"
                infoend = "Content-Length: 0\r\n\r\n"
                sendResponseMsg = self.create_rsp_msg(msgType, responseInv, infoHeadList, infoend)
                #self.sclient.sendto(sendResponseMsg.encode('utf-8'), self.eGWAddressPort)
                self.sendMsg("100 trying", sendResponseMsg)
                #time.sleep(50)
                #get port============need be careful===============
                inviteinfo=infoList[1].split("\r\n")
                for invTemp in inviteinfo:
                    if "m=video" in invTemp:
                        vidoInfo = invTemp.split(" ")
                        destPort = vidoInfo[1]
                        break
                print(destPort)
                #send ok
                responseInvok = "SIP/2.0 200 OK\r\n"
                msgHead = self.create_rsp_msg(msgType, responseInvok, infoHeadList,"")
                contact="Contact: <sip:"+self.localIP+":"+self.localPort+">\r\n"
                type="Content-Type: application/sdp\r\n"
                invOk="v=0\r\no=32028101002000094099 0 0 IN IP4 "+self.localIP+"\r\ns=Play\r\nc=IN IP4 "+self.localIP+"\r\nt=0 0\r\nm=video 20218 RTP/AVP 96\r\na=sendonly\r\na=rtpmap:96 PS/90000\r\ny=0104010385\r\n"
                contlen="Content-Length: "+str(len(invOk))+"\r\n\r\n"
                sendResponseInvok=responseInvok+msgHead+contact+type+contlen+invOk
                #sendResponseInvok=responseInvok+msgHead+type+contlen+invOk
                print(sendResponseInvok)
                #self.sclient.sendto(sendResponseInvok.encode('utf-8'), self.eGWAddressPort)
                self.sendMsg("200 OK", sendResponseInvok)
            # deal ack packet
            elif "ACK sip" in infoHeadList[0]:
                # print("received:", data, "from", addr)
                print("=" * 30 + nowTime + " rcv ACK msg" + "+" * 30)
                print("=" * 20 + nowTime + " start to send RTP packet" + "=" * 20)
                rtpcmd="D:\\testtool\\RTP_send_tool\\main_start.bat "+camID+" "+destPort
                print(repr(rtpcmd))
                os.system(rtpcmd)
            # deal bye packet
            elif "BYE sip" in infoHeadList[0]:
                print("+" * 30 + "rcv BYE msg" + "+" * 30)
                responseBye = "SIP/2.0 200 OK\r\n"
                for temp in infoHeadList[1:]:
                    headKeyValue = temp.split(":")
                    keadKey = headKeyValue[0]
                    # get camera ID
                    if keadKey =="To":
                        camID = headKeyValue[2].split("@")[0]
                    if keadKey in self.responseByeHead:
                        responseBye = responseBye + temp + "\r\n"
                infoend = "User-Agent: NCG V2.6.0.299939\r\nContent-Length: 0\r\n\r\n"
                sendResponseBye = responseBye + infoend
                self.sclient.sendto(sendResponseBye.encode('utf-8'), self.eGWAddressPort)
                print(camID)
                print("=" * 20 + "stop to send RTP packet" + "=" * 20)
                rtpcmd="D:\\testtool\\RTP_send_tool\\main_stop.bat "+camID
                #print(repr(rtpcmd))
                os.system(rtpcmd)
    def down_heartbeat(self):
        time.sleep(0.5)
        while True:
            self.sendMsg("heartbeat", self.keepLive)
            time.sleep(30)
    def create_rsp_msg(self, messageType, responseMessage, headList, msgend=None):
        msgHead = ""
        if messageType == "MESSAGE":
            msgHead = self.responseMsgHead
        elif messageType == "SUBSCRIBE":
            msgHead = self.responseSubHead
        elif messageType == "INVITE":
            msgHead = self.responseInvHead
        elif messageType == "BYE":
            msgHead = self.responseByeHead
        else:
            print("***********", "Message Type Error!", "************")

        for temp in headList[1:]:
            headKeyValue = temp.split(":")
            keadKey = headKeyValue[0]
            if keadKey in msgHead:
                responseMessage = responseMessage + temp + "\r\n"
        if msgend != None:
            sendResponseMsg = responseMessage + msgend
        return sendResponseMsg
    def camera_info_send(self):
        for msg in self.mesCatalog:
            print("=" * 30 + "send camera info" + "=" * 30)
            self.sclient.sendto(msg.encode('utf-8'), self.eGWAddressPort)
    def multi_message_send(self):
        self.camera_info_send
        self.camera_info_send
        self.camera_info_send
        self.camera_info_send
        self.camera_info_send
        self.camera_info_send
        self.camera_info_send
        self.camera_info_send
        self.camera_info_send

    def closeConnect(self):
        self.sclient.close()
    def sendNotify(self):
        while True:
            time.sleep(10)
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
            print("=" * 30 + nowTime + " send notify" + "=" * 30)
            self.sendMsg("notify", self.notify)
            self.sendMsg("notify", self.notify)
            self.sendMsg("notify", self.notify)
            self.sendMsg("notify", self.notify)
            self.sendMsg("notify", self.notify)
    def gis_info_send(self):
        while True:
            time.sleep(3)
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
            print("=" * 30 + nowTime + " send gis info" + "=" * 30)
            self.sendMsg("gisInfo", self.GisInfo)
    def get_key_value(self, KeyName, MsgBody):
        KeyValue = ""
        if KeyName not in MsgBody:
            print(KeyName + " not find !")
        else:
            pass
        return KeyValue
