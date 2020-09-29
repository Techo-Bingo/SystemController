import csv
import random

class Register:
    def __init__(self, updomainIP, updomainPort, updomainGB, downdomainIP, downdomainPort, downdomainGB):
        # third config
        localGBID = downdomainGB
        localIP = downdomainIP
        localPort = downdomainPort
        localAddress = localGBID + "@" + localIP + ":" + localPort
        # eGW650 config
        remoteGBID = updomainGB
        remoteIP = updomainIP
        remotePort = updomainPort
        remoteAddress = remoteGBID + "@" + remoteIP + ":" + remotePort

        randNum = random.randint(0, 9999)
        strIntreg = "%04d" % randNum
        regHead = "REGISTER sip:" + remoteAddress + " SIP/2.0\r\n"
        regCallID = "Call-ID: 4e59a5caeb6746e3a8f0ab0762e8" + strIntreg + "\r\n"
        regCSeq = "CSeq: 20 REGISTER\r\n"
        regFrom = "From: 测试<sip:" + localAddress + ">;tag=33229da6eee84c208c1783e1549a8898\r\n"
        #regFrom = "From: <sip:" + "51010701012000000101@196.1.1.101:71001111" + ">\n"#;tag=33229da6eee84c208c1783e1549a8898\r\n"
        regTo = "To: <sip:" + remoteAddress + ";transport=udp>\r\n"
        regVia = "Via: SIP/2.0/UDP " + localIP + ":" + localPort + ";branch=596eab56eaa1b5fa7;RPort=rport\r\n"
        #regVia = "Via: SIP/2.0/UDP " + "1.1.1." + ":" + "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111" + ";branch=596eab56eaa1b5fa7;RPort=rport\r\n"
        regMaxForwards = "Max-Forwards: 70\r\n"
        regContact = "Contact: <sip:" + localAddress + ">\r\n"
        regUserAgent = "User-Agent: NCG V2.6.0.299939\r\n"
        regExpires = "Expires: 3600\r\n"
        regContentLen = "Content-Length: 0\r\n\r\n"
        self.msgRegister = regHead + regCallID + regCSeq + regFrom + regTo + regVia + regMaxForwards + regContact + regUserAgent + regExpires + regContentLen
class Keeplive:
    def __init__(self, updomainIP, updomainPort, updomainGB, downdomainIP, downdomainPort, downdomainGB):
        localGBID = downdomainGB
        localIP = downdomainIP
        localPort = downdomainPort
        localAddress = localGBID + "@" + localIP + ":" + localPort
        # eGW650 config
        remoteGBID = updomainGB
        remoteIP = updomainIP
        remotePort = updomainPort
        remoteAddress = remoteGBID + "@" + remoteIP + ":" + remotePort

        randNum = random.randint(0,9999)
        strIntkeepLive = "%04d" %randNum

        msgLiveHead = "MESSAGE sip:"+remoteAddress+" SIP/2.0\r\n"
        msgLiveCallID = "Call-ID: d307561f247a4937bcd3abf208f5"+strIntkeepLive+"\r\n"
        msgLiveCSeq = "CSeq: 20 MESSAGE\r\n"
        msgLiveFrom = "From: <sip:"+localAddress+">;tag=d07f9af916ae415cb2209b2d82428890\r\n"
        msgLiveTo = "To: <sip:"+remoteAddress+";transport=udp>\r\n"
        msgLiveVia = "Via: SIP/2.0/UDP "+localIP+":"+localPort+";branch=4b20cd314852aba8e;RPort=rport\r\n"
        msgLiveMaxForward = "Max-Forwards: 70\r\n"
        msgLiveUserAgent = "User-Agent: NCG V2.6.0.299939\r\n"
        msgLiveContentType = "Content-Type: Application/MANSCDP+xml\r\n"
        msgLiveMsgbody = "<?xml version=\"1.0\"?>\r\n<Notify>\r\n<CmdType>Keepalive</CmdType>\r\n<SN>57</SN>\r\n<DeviceID>"+localGBID+"</DeviceID>\r\n<Status>OK</Status>\r\n</Notify>\r\n"
        msgLiveContentLen = "Content-Length: "+str(len(msgLiveMsgbody))+"\r\n\r\n"
        self.keepLive =msgLiveHead + msgLiveCallID + msgLiveCSeq + msgLiveFrom + msgLiveTo + msgLiveVia + msgLiveMaxForward + msgLiveUserAgent + msgLiveContentType + msgLiveContentLen + msgLiveMsgbody
class CatalogRsp:
    def __init__(self, updomainIP, updomainPort, updomainGB, downdomainIP, downdomainPort, downdomainGB,):
        localGBID = downdomainGB
        localIP = downdomainIP
        localPort = downdomainPort
        localAddress = localGBID + "@" + localIP + ":" + localPort
        # eGW650 config
        remoteGBID = updomainGB
        remoteIP = updomainIP
        remotePort = updomainPort
        remoteAddress = remoteGBID + "@" + remoteIP + ":" + remotePort
        randNum = random.randint(0, 9999)
        strIntmsg = "%04d" % randNum
        msgcatalogHead = "MESSAGE sip:" + remoteAddress + " SIP/2.0\r\n"
        msgcatalogCallID = "Call-ID: 1c3d0a10dcf14bdc9e2bab2c8911" + strIntmsg + "\r\n"
        msgcataloCSeq = "CSeq: 20 MESSAGE\r\n"
        msgcataloFrom = "From: <sip:" + localAddress + ">;tag=50bbea169e7d4b9898a9762d1708b13d\r\n"
        msgcataloTo = "To: <sip:" + remoteAddress + ";transport=udp>\r\n"
        msgcataloVia = "Via: SIP/2.0/UDP " + localIP + ":" + localPort + ";branch=ab331a7dfdeaeee0a;RPort=rport\r\n"
        msgcataloMaxForwards = "Max-Forwards: 70\r\n"
        msgcataloUserAgent = "User-Agent: NCG V2.6.0.299939\r\n"
        msgcataloContentType = "Content-Type: Application/MANSCDP+xml\r\n"

        # ===camera info xml===
        msgCatalogPacketList = []
        csvfile = open('cameraInfo.csv', 'r')
        lines = csv.reader(csvfile)
        infoListCsv = []
        for line in lines:
            infoListCsv.extend(line)
        csvfile.close()
        #packetlen = len(infoListCsv)
        packetlen = 2
        # ==============camera dir========  the dir can be change when need============
        CivilCode = "510103"
        cameraInfodir = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n" \
                        "<Response>\r\n" \
                            "<CmdType>Catalog</CmdType>\r\n" \
                            "<SN>155</SN>\r\n" \
                            "<DeviceID>" + localGBID + "</DeviceID>\r\n" \
                            "<SumNum>" + str(packetlen) + "</SumNum>\r\n" \
                            "<DeviceList Num=\"3\">\r\n" \
                                "<Item>\r\n" \
                                    "<DeviceID>51</DeviceID>\r\n" \
                                    "<Name>sichuan</Name>\r\n" \
                                "</Item>\r\n" \
                                "<Item>\r\n" \
                                    "<DeviceID>5101</DeviceID>\r\n" \
                                    "<Name>ctuy</Name>\r\n" \
                                "</Item>\r\n" \
                                "<Item>\r\n" \
                                    "<DeviceID>" + CivilCode + "</DeviceID>\r\n" \
                                    "<Name>TD_123456</Name>\r\n" \
                                "</Item>\r\n" \
                            "</DeviceList>\r\n<" \
                        "/Response>\r\n"
        catalogContentLen = "Content-Length: " + str(len(cameraInfodir)) + "\r\n\r\n"
        message2_Catalog_dir = msgcatalogHead + msgcatalogCallID + msgcataloCSeq + msgcataloFrom + msgcataloTo + msgcataloVia + msgcataloMaxForwards + msgcataloUserAgent + msgcataloContentType + catalogContentLen + cameraInfodir
        msgCatalogPacketList.append(message2_Catalog_dir)
        # ==============camera Info========
        i = 1
        for cameraTemp in infoListCsv[1:]:
            cameraInfoList = cameraTemp.split("\t")
            gbID = cameraInfoList[0]
            Name = cameraInfoList[1]
            randNum = random.randint(0, 9999)
            strIntmsg = "%04d" % randNum
            msgcatalogCallID = "Call-ID: 1c3d0a10dcf14bdc9e2bab2c8911" + strIntmsg + "\r\n"
            cameraInfoDev = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<Response>\r\n<CmdType>Catalog</CmdType>\r\n<SN>" + str(
                155 + i) + "</SN>\r\n<DeviceID>" + localGBID + "</DeviceID>\r\n<SumNum>" + str(
                packetlen) + "</SumNum>\r\n<DeviceList Num=\"1\">\r\n<Item>\r\n<DeviceID>" + gbID + "</DeviceID>\r\n<Name>" + Name + "</Name>\r\n<Manufacturer>TD-TECH</Manufacturer>\r\n<Model></Model>\r\n<Owner>" + localGBID + "</Owner>\r\n<CivilCode>" + CivilCode + "</CivilCode>\r\n<Block></Block>\r\n<Address>196.1.1.166</Address>\r\n<Parental>0</Parental>\r\n<ParentID>" + localGBID + "</ParentID>\r\n<RegisterWay>1</RegisterWay>\r\n<Secrecy>0</Secrecy>\r\n<IPAddress>196.1.1.166</IPAddress>\r\n<Port>5061</Port>\r\n<Password>510107010</Password>\r\n<Status>ON</Status>\r\n<CertNum></CertNum>\r\n<Certifiable>0</Certifiable>\r\n<ErrorCode>400</ErrorCode>\r\n<EndTime></EndTime>\r\n<Longitude>11</Longitude>\r\n<Latitude>11</Latitude>\r\n<PTZType>1</PTZType>\r\n</Item>\r\n</DeviceList>\r\n</Response>"
            catalogContentinfoLen = "Content-Length: " + str(len(cameraInfoDev)) + "\r\n\r\n"
            message2_Catalog_camera = msgcatalogHead + msgcatalogCallID + msgcataloCSeq + msgcataloFrom + msgcataloTo + msgcataloVia + msgcataloMaxForwards + msgcataloUserAgent + msgcataloContentType + catalogContentinfoLen + cameraInfoDev
            msgCatalogPacketList.append(message2_Catalog_camera)
            i = i + 1
        self.msgCatalogPacketList = msgCatalogPacketList
class Notify:
    # ====================define message_catalog start===========================
    def __init__(self, updomainIP, updomainPort, updomainGB, downdomainIP, downdomainPort, downdomainGB):
        localGBID = downdomainGB
        localIP = downdomainIP
        localPort = downdomainPort
        localAddress = localGBID + "@" + localIP + ":" + localPort
        # eGW650 config
        remoteGBID = updomainGB
        remoteIP = updomainIP
        remotePort = updomainPort
        remoteAddress = remoteGBID + "@" + remoteIP + ":" + remotePort
        randNum = random.randint(0, 9999)
        strIntmsg = "%04d" % randNum
        notifyHead = "NOTIFY sip:" + remoteAddress + " SIP/2.0\r\n"
        notifyCallID = "Call-ID: 1c3d0a10dcf14bdc9e2bab2c8911" + strIntmsg + "\r\n"
        notifyCSeq = "CSeq: 34 NOTIFY\r\n"
        notifyEvent = "Event: Catalog\r\n"
        notifyFrom = "From: <sip:" + localAddress + ">;tag=50bbea169e7d4b9898a9762d1708b13d\r\n"
        notifyTo = "To: <sip:" + remoteAddress + ";transport=udp>\r\n"
        notifyVia = "Via: SIP/2.0/UDP " + localIP + ":" + localPort + ";branch=ab331a7dfdeaeee0a;RPort=rport\r\n"
        notifyMaxForwards = "Max-Forwards: 70\r\n"
        notifySubState = "Subscription-State: active;expires=1000000\r\n"
        notifyUserAgent = "User-Agent: IMOS/V3\r\n"
        notifyContentType = "Content-Type: Application/MANSCDP+xml\r\n"

        cameraInfoDev = "<?xml version=\"1.0\"?> encoding=\"UTF-8\"?>\r\n" \
                        "<Notify>\r\n" \
                        "<CmdType>Catalog</CmdType>\r\n" \
                        "<SN>146</SN>\r\n" \
                        "<DeviceID>51010701012000000101</DeviceID>\r\n" \
                        "<SumNum>1</SumNum>\r\n" \
                        "<DeviceList Num=\"1\">\r\n<" \
                        "Item>\r\n" \
                        "<DeviceID>18297500001312120001</DeviceID>\r\n" \
                        "<Event>UPDATE</Event>\r\n" \
                        "<Name>IPdome_3</Name>\r\n" \
                        "<CatalogType>1</CatalogType>\r\n" \
                        "<DecorderTag>hikvision</DecorderTag>\r\n" \
                        "<RecLocation></RecLocation>\r\n" \
                        "<OperateType>ADD</OperateType>\r\n" \
                        "<CivilCode>51010701012000000101</CivilCode>\r\n" \
                        "<IPAddress>127.0.0.1</IPAddress>\r\n" \
                        "<Parental>0</Parental>\r\n" \
                        "<ParentID>51010701012000000101</ParentID>\r\n" \
                        "<Status>OFF</Status>\r\n" \
                        "<Longitude>0</Longitude>\r\n" \
                        "<Latitude>0</Latitude>\r\n" \
                        "<Privilege>%FF%FF%FF</Privilege>\r\n" \
                        "<Info>\r\n" \
                        "<CameraType>1</CameraType>\r\n" \
                        "</Info>\r\n" \
                        "</Item>\r\n" \
                        "</DeviceList>\r\n" \
                        "</Notify>"

        # cameraInfoDev = "<? xmlversion=\"1.0\"?>\r\n" \
        #                 "<Notify>\r\n" \
        #                    "<CmdType>Catalog</CmdType>\r\n" \
        #                    "<SN>22</SN>\r\n" \
        #                    "<DeviceID>51010701012000000101</DeviceID>\r\n" \
        #                    "<SumNum>1</SumNum>\r\n" \
        #                    "<DeviceListNum=\"1\">\r\n" \
        #                         "<Item>\r\n" \
        #                             "<DeviceID>51010701011312120001</DeviceID>\r\n" \
        #                             "<Event>DEFECT</Event>\r\n" \
        #                         "</Item>\r\n" \
        #                     "</DeviceList>\r\n" \
        #                 "</Notify>"
        # cameraInfoDev = "<? xmlversion=\"1.0\"?>\r\n" \
        #                 "<Notify>\r\n" \
        #                     "<CmdType>Catalog</CmdType>\r\n" \
        #                     "<SN>30</SN>\r\n" \
        #                     "<DeviceID>51010701012000000101</DeviceID>\r\n" \
        #                     "<SumNum>1</SumNum>\r\n" \
        #                     "<DeviceListNum=\"1\">\r\n" \
        #                         "<Item>\r\n" \
        #                             "<DeviceID>51010701011312120001</DeviceID>\r\n" \
        #                             "<Event>UPDATE</Event>\r\n" \
        #                             "<Name>IPC_101</Name>\r\n" \
        #                             "<Manufacturer>Tdtech</Manufacturer>\r\n" \
        #                             "<Model>1.0</Model>\r\n" \
        #                             "<Owner>0</Owner>\r\n" \
        #                             "<CivilCode>510107</CivilCode>\r\n" \
        #                             "<Address>axy</Address>\r\n" \
        #                             "<Parental>0</Parental>\r\n" \
        #                             "<RegisterWay>1</RegisterWay>\r\n" \
        #                             "<Secrecy>0</Secrecy>\r\n" \
        #                             "<Status>ON</Status>\r\n" \
        #                         "</Item>\r\n" \
        #                     "</DeviceList>\r\n" \
        #                 "</Notify>"

        catalogContentinfoLen = "Content-Length: " + str(len(cameraInfoDev)) + "\r\n\r\n"
        self.notify = notifyHead + notifyCallID + notifyCSeq + notifyEvent + notifyFrom + notifyTo + notifyVia + notifyMaxForwards + notifySubState + notifyUserAgent + notifyContentType + catalogContentinfoLen + cameraInfoDev
class GisInfo:
    # ====================define message_catalog start===========================
    def __init__(self, updomainIP, updomainPort, updomainGB, downdomainIP, downdomainPort, downdomainGB, ):
        localGBID = downdomainGB
        localIP = downdomainIP
        localPort = downdomainPort
        localAddress = localGBID + "@" + localIP + ":" + localPort
        # eGW650 config
        remoteGBID = updomainGB
        remoteIP = updomainIP
        remotePort = updomainPort
        remoteAddress = remoteGBID + "@" + remoteIP + ":" + remotePort
        randNum = random.randint(0, 9999)
        strIntmsg = "%04d" % randNum
        notifyHead = "NOTIFY sip:" + remoteAddress + " SIP/2.0\r\n"
        notifyCallID = "Call-ID: 1c3d0a10dcf14bdc9e2bab2c8911" + strIntmsg + "\r\n"
        notifyCSeq = "CSeq: 34 NOTIFY\r\n"
        notifyEvent = "Event: Catalog\r\n"
        notifyFrom = "From: <sip:" + localAddress + ">;tag=50bbea169e7d4b9898a9762d1708b13d\r\n"
        notifyTo = "To: <sip:" + remoteAddress + ";transport=udp>\r\n"
        notifyVia = "Via: SIP/2.0/UDP " + localIP + ":" + localPort + ";branch=ab331a7dfdeaeee0a;RPort=rport\r\n"
        notifyMaxForwards = "Max-Forwards: 70\r\n"
        notifySubState = "Subscription-State: active;expires=1000000\r\n"
        notifyUserAgent = "User-Agent: IMOS/V3\r\n"
        notifyContentType = "Content-Type: Application/MANSCDP+xml\r\n"

        gisInfo = "<?xml version=\"1.0\"?>\r\n<Notify>\r\n<CmdType>MobilePosition</CmdType>\r\n<SN>1</SN>\r\n<Time>2019-09-10T13:25:04</Time>\r\n<DeviceID>18297500001312120001</DeviceID>\r\n<Longitude>44</Longitude>\r\n<Latitude>45</Latitude>\r\n</Notify>"
        gisContentinfoLen = "Content-Length: " + str(len(gisInfo)) + "\r\n\r\n"
        self.gisInfo = notifyHead + notifyCallID + notifyCSeq + notifyEvent + notifyFrom + notifyTo + notifyVia + notifyMaxForwards + notifySubState + notifyUserAgent + notifyContentType + gisContentinfoLen + gisInfo
