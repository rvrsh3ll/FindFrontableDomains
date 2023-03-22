#!/usr/bin/python3
# Run setup.sh first!

import dns.resolver
import threading
import queue
import argparse
import sys
from Sublist3r import sublist3r
potentially_frontable = []

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
                query = dns.resolver.resolve(hostname, 'a')
                # Iterate through response and check for potential CNAMES
                for i in query.response.answer:
                    for j in i.items:
                        target =  j.to_text()
                        if 'cloudfront' in target:
                            print("CloudFront Frontable domain found: " + str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))  
                        elif 'appspot.com' in target:
                            print("Google Frontable domain found: " + str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))                               
                        elif 'msecnd.net' in target:
                            print("Azure Frontable domain found: " + str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))                                
                        elif 'aspnetcdn.com' in target:
                            print("Azure Frontable domain found: " + str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))                                
                        elif 'azureedge.net' in target:
                            print("Azure Frontable domain found: " + str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))                                
                        elif 'azurefd.net' in target:
                            print("Azure Frontable domain found: " + str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))                               
                        elif 'a248.e.akamai.net' in target:
                            print("Akamai frontable domain found: " + str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))                                
                        elif 'secure.footprint.net' in target:
                            print("Level 3 URL frontable domain found: " + str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))                                
                        elif 'cloudflare' in target:
                            print("Cloudflare frontable domain found: " + str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))                                
                        elif 'unbouncepages.com' in target:
                            print("Unbounce frontable domain found: " + str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))                                
                        elif 'x.incapdns.net' in target:
                            print("Incapsula frontable domain found: " +str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))                                
                        elif 'fastly' in target:
                            print("Fastly URL frontable domain found: " + str(hostname) + " " + str(target))
                            potentially_frontable.append(str(hostname))                                
            except Exception as e:
                pass
            self.queue.task_done()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=False)
    parser.add_argument('-t', '--threads', type=int, required=False, default=10)
    parser.add_argument('-d', '--domain', type=str, required=False)
    parser.add_argument('-c', '--check', type=str, required=False)
    parser.add_argument('-o', '--out', type=str, required=False)
    args = parser.parse_args()
    threads =  args.threads
    check=args.check
    file = args.file
    domain = args.domain
    out_file = args.out
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
    elif check:
        q.put(check)       
    elif domain:
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
        t.daemon = True
        t.start()
    
    q.join()
    print("")
    print("Search complete!")
    #filter out dupes from the list
    global potentially_frontable
    potentially_frontable = list(dict.fromkeys(potentially_frontable))
    if out_file:
       with open(out_file, 'w') as file_handle:
           for domain in potentially_frontable:
               file_handle.write('%s\n' % domain)
       

if __name__ == "__main__":
    main()
