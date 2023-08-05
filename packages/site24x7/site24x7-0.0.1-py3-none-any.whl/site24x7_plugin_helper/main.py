#!/usr/bin/python3.6
import connector
import sys
import os
import json
import argparse
from subprocess import call
# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.FileHandler('/tmp/plugin.log')
# logger.info(msg="test")
# breakpoint()
#import ggplot as gg
passDbConnection = True


if __name__ == "__main__":
    # server infos are given as arguments
    server = sys.argv[1]
    database = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    driverLocation = sys.argv[5] # /opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.1.1
    query = sys.argv[6] 
    thisPluginName = sys.argv[7] 
    cache = {
        "server":server,
        "database":database,
        #"username":username,
        #"password":password,
        "driverLocation":driverLocation,
        "query":query,
        #"rowAll":rowAll,
        "thisPluginName":thisPluginName,
    }
    if not passDbConnection:
        cursor = connector.getCursorFromDatabase(server, database, username, password, driverLocation)
        print("connnected")
        # existing query that returns all rows from the table for caching
        # 'EXEC [Ultramerchant].dbo.pr_membership_credit_billing_stats_24x7_monitor_sel'
        rows = connector._fetchall(cursor, query)
        for i in range(len(rows)):
            key = rows[i][1]
            value = rows[i][2]
            cache[key] = value
    # # validate data before saving to cache
    # ww = connector.validatePluginData(cache)
    # breakpoint()
    
    # save cache to file as thisPluginName 
    cacheFileName = "/tmp/" + thisPluginName + ".cache" # 
    open(cacheFileName, 'w').write(
        json.dumps(cache, indent=4)
    )
    print(json.dumps(cache, indent=4, sort_keys=True))

    site24x7_location = "/opt/site24x7/monagent/plugins//plugin/plugin.py"
    folderDestination = os.path.join(site24x7_location, thisPluginName)
    fileDestination = os.path.join(folderDestination, thisPluginName + ".py")
    print("folderDestination: " + folderDestination)
    print("fileDestination: " + fileDestination)
    # BELOW PROCESS WILL BE DONE BY JENKINS
    # create a folder if not exists
    if not os.path.exists(folderDestination):
        call(f"mkdir {folderDestination}", shell=True)
        os.mkdir(folderDestination)

    # create a python file if not exists
    if not os.path.isfile(fileDestination):
        call(f"touch {fileDestination}", shell=True)
    open(fileDestination, 'w').write(f'''#!/usr/bin/python3.6
import json
cacheData = json.loads(open("{cacheFileName}").read())
PLUGIN_VERSION = "2"
HEARTBEAT = "true"
FREQUENCY = "1"
METRIC_UNITS = {{}}

def metricCollector():
    data = {{}}
    data["plugin_version"] = PLUGIN_VERSION
    data['heartbeat_required'] = HEARTBEAT
    data["CPU"] = 100
    # data["FREQUENCY"] = FREQUENCY
    for i in cacheData:
        data[i] = cacheData[i]
    return data

if __name__ == "__main__":
    result = metricCollector()
    print(json.dumps(result, indent=4, sort_keys=False))
''' )
