#import sys
import threading
#sys.path.append(".")
import eGW650_domain_down as downdomain

# 模拟的下级域
localGBID = "51010701012000000101"
localIP = "22.22.22.169"
localPort = "5061"
# 上级域 网关
remoteGBID = "32050950002000005001"
remoteIP = "22.22.22.88"
remotePort = "5061"
filename = "testda"

newdomain = downdomain.DownDomain(remoteIP,remotePort,remoteGBID,localIP,localPort,localGBID,filename)
downdomainprocess = threading.Thread(target=newdomain.start_domain_process, args=[])
heartbeatprocess = threading.Thread(target=newdomain.down_heartbeat, args=[])
downdomainprocess.start()
heartbeatprocess.start()
