from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime
#from flask import Flask, json
import threading
import time
import os
import random


N_THREAD = int(os.environ['N_THREAD'])
N_GET_THREAD = int(os.environ['N_GET_THREAD']) # number of get operation performed by each thread
URL = os.environ['TARGET_URL']
SELENIUM_HUB_URL = os.environ['SELENIUM_HUB_URL']

HOSTS = [URL+"/product/OLJCESPC7Z", URL+"/product/6E92ZMYYFZ", URL+"/product/LS4PSXUNUM", URL+"/product/9SIQT8TOJO", URL+"/cart"]

threadResults = [dict() for x in range(N_THREAD)]
threadCount = [dict() for x in range(N_THREAD)]
threadID = dict()

finalResult = dict()
finalCount = dict()

#api = Flask(__name__)

def PerformGetOperation(id):

    systemInited = False

    while systemInited == False:
        try:
            driver = webdriver.Remote(
                command_executor=SELENIUM_HUB_URL,
                desired_capabilities=getattr(DesiredCapabilities, "CHROME")
            )
            systemInited = True
        except:
            systemInited = False

    print("Thread {} inited".format(id), flush=True)

    for i in range(N_GET_THREAD):
        recordTime = datetime.now().strftime("%H:%M:%S")

        n = random.randint(0,4)
        
        driver.get(HOSTS[n])

        recordValue = GetNetworkResources(driver)
        if recordTime in threadResults[id].keys():
            threadResults[id][recordTime] = threadResults[id][recordTime] + recordValue
            threadCount[id][recordTime] = threadCount[id][recordTime] + 1
        else:
            threadResults[id][recordTime] = recordValue
            threadCount[id][recordTime] = 1

    driver.quit()


#Gets network information, including network calls
def GetNetworkResources(driver):
    Resources = driver.execute_script("return window.performance.getEntries();")
    
    max = 0
    for resource in Resources:
        if 'responseEnd' in resource.keys():
            if resource['responseEnd'] > max:
                max = resource['responseEnd']
                            
    return max


def MergeRecords():
    for i in range(N_THREAD):
        for key, value in threadResults[i].items():
            if key in finalResult.keys():
                finalResult[key] = finalResult[key] + value
                finalCount[key] = finalCount[key] + threadCount[i][key]
            else:
                finalResult[key] = value
                finalCount[key] = threadCount[i][key]

    for k, r in finalResult.items():
        print("{} {} {}".format(k, r/finalCount[k], finalCount[k]), flush=True)


#def ProduceJsonResult():
#    lst = []
#
#    for k, r in finalResult.items():
#        jsonRecord = {
#            'Time': k,
#            'Latency-Value': r,
#            'GET-Operation-Performed': finalCount[k],
#        }
#
#        lst.append(jsonRecord)
#
#    return lst


#@api.route('/results', methods=['GET'])
#def get_results():
#  return json.dumps(ProduceJsonResult())


if __name__ == "__main__":
    
    try:
        for i in range(N_THREAD):
            threadID[i] = threading.Thread(target=PerformGetOperation, args=(i,))
            threadID[i].start()

        for i in range(N_THREAD):
            threadID[i].join()


    except Exception as e: 
        print(e)

    MergeRecords()

    print("Test process completed", flush=True)

    #api.run()

    time.sleep(10000)

