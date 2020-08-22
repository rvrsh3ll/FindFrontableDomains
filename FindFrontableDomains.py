#!/usr/bin/python3
#Run setup.sh first!

import dns.resolver
import threading
import queue
import argparse
import sys
import sslscan
import subprocess
from Sublist3r import sublist3r
from datetime import datetime

class ThreadLookup(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):

        while True:
            if self.queue.empty():
                break
            #grabs host from queue
            hostname = self.queue.get()
            try:

                dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
                dns.resolver.default_resolver.nameservers = ['209.244.0.3', '209.244.0.4','64.6.64.6','64.6.65.6', '8.8.8.8', '8.8.4.4','84.200.69.80', '84.200.70.40', '8.26.56.26', '8.20.247.20', '208.67.222.222', '208.67.220.220','199.85.126.10', '199.85.127.10', '81.218.119.11', '209.88.198.133', '195.46.39.39', '195.46.39.40', '96.90.175.167', '193.183.98.154','208.76.50.50', '208.76.51.51', '216.146.35.35', '216.146.36.36', '37.235.1.174', '37.235.1.177', '198.101.242.72', '23.253.163.53', '77.88.8.8', '77.88.8.1', '91.239.100.100', '89.233.43.71', '74.82.42.42', '109.69.8.51']
                query = dns.resolver.query(hostname, 'a')
                # Iterate through response and check for potential CNAMES
                for i in query.response.answer:
                    for j in i.items:
                        target =  j.to_text()
                        if 'cloudfront' in target:
                            print("CloudFront Frontable domain found: " + str(hostname) + " " + str(target))
                        elif 'ghs.googlehosted.com' in target:
                            print("Google Frontable domain found: " + str(hostname) + " " + str(target))
                        elif 'appspot.com' in target:
                            print("Appspot (Old) Frontable domain found: " + str(hostname) + " " + str(target))
                        elif 'aspnetcdn.com' in target or 'azureedge.net' in target or 'msecnd.net' in target :
                            try:
                                response=subprocess.getoutput(f'pysslscan scan --scan=protocol.http --scan=server.ciphers --tls10 {str(hostname)} | grep Accepted | wc -l')
                                if int(response) > 0:
                                    print("\033[92mAzure Frontable domain found: " + str(hostname) + " " + str(target) + '\033[0m')
                                    continue
                            except Exception as e:
                                print(e)
                                pass
                            print("Azure Frontable domain found: " + str(hostname) + " " + str(target))
                        elif 'a248.e.akamai.net' in target:
                            print("Akamai frontable domain found: " + str(hostname) + " " + str(target))
                        elif 'secure.footprint.net' in target:
                            print("Level 3 URL frontable domain found: " + str(hostname) + " " + str(target))
                        elif 'cloudflare' in target:
                            print("Cloudflare frontable domain found: " + str(hostname) + " " + str(target))
                        elif 'unbouncepages.com' in target:
                            print("Unbounce frontable domain found: " + str(hostname) + " " + str(target))
                        elif 'x.incapdns.net' in target:
                            print("Incapsula frontable domain found: " +str(hostname) + " " + str(target))
                        elif 'fastly' in target:
                            print("Fastly URL frontable domain found: " + str(hostname) + " " + str(target))
            except Exception as e:
                pass
            self.queue.task_done()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=False)
    parser.add_argument('-t', '--threads', type=int, required=False, default=20)
    parser.add_argument('-d', '--domain', type=str, required=False)
    parser.add_argument('-c', '--check', type=str, required=False)
    parser.add_argument('-r', '--recursive', type=str, required=False)
    args = parser.parse_args()
    threads =  args.threads
    check = args.check
    file = args.file
    domain = args.domain
    recursive = args.recursive

    from colorama import init
    init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
    from termcolor import cprint 
    from pyfiglet import figlet_format

    cprint(figlet_format('Find'))
    cprint(figlet_format('Frontable'))
    cprint(figlet_format('Domains'))

    q = queue.Queue()
    if file:
        with open(file, 'r') as f:
            for d in f:
                d = d.rstrip()
                if d:
                    q.put(d)   
    elif recursive:
        with open('./Subdomains-Found-%s.txt'%datetime.now().strftime('%d-%m-%Y_%H:%M'), 'w') as log:
            with open(recursive, 'r') as f:
                for d in f:
                    d = d.rstrip()
                    if d:
                        q.put(d)
                        subdomains = []
                        subdomains = sublist3r.main(d, threads, savefile=None, ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None)
                        for i in subdomains:
                            log.write(i + '\n')
                            print(i)
                            q.put(i)
    elif check:
        q.put(check)       
    elif domain:
        q.put(domain)
        subdomains = []
        subdomains = sublist3r.main(domain, threads, savefile=None, ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None)
        for i in subdomains:
            print(i)
            q.put(i)
    else:
        print("No Input Detected!")
        sys.exit()
    print("---------------------------------------------------------")
    print("Starting search for frontable domains...")
    # spawn a pool of threads and pass them queue instance
    for i in range(threads):
        t = ThreadLookup(q)
        t.setDaemon(True)
        t.start()
    
    q.join()
    print("")
    print("Search complete!")

if __name__ == "__main__":
    main()
