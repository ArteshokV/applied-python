# -*- encoding: utf-8 -*-
import datetime
import statistics
from parse import *
from urllib.parse import urlparse

def toInt(num):
    try:
        return int(num)
    except ValueError:
        return -1

def parseLine(line):
    if line[0] == '[':
        server_request = {}

        if len(list(findall("[{}]", line))) != 0: #if date found
            for r in findall("[{}]", line):
                server_request['date'] = r[0]
        else:
            return 0

        if len(list(findall("\"{}\"", line))) != 0: #if url found
            for r in findall("\"{}\"", line):
                urlArray = r[0].split(' ')
                if len(urlArray) != 3:
                    return 0
                server_request['url_method'] = urlArray[0]
                server_request['url_adress'] = urlArray[1]
                server_request['url_protocol'] = urlArray[2]
        else:
            return 0

        timeIn = line.split(' ')

        if len(timeIn) >= 2:
            server_request['response_code'] = toInt(timeIn[len(timeIn) - 2])
            server_request['response_time'] = toInt(timeIn[len(timeIn) - 1])

            #check if numbers are valid
            if server_request['response_code'] == -1 or server_request['response_time'] == -1:
                return 0
        else:
            return 0
    else:
        return 0

    if len(server_request.keys()) == 6:
        return server_request
    else:
        return 0


def checkAndModifyLogLine(parsed_line, ignore_files, ignore_urls, start_at, stop_at, request_type, ignore_www):
    parsed_url = urlparse(parsed_line['url_adress'])
    if ignore_files and (parsed_url.path.find('.') != -1): #if '.' is found in path - its file and we ignore
        return 0

    if len(ignore_urls):
        for url in ignore_urls:
            if parsed_line['url_adress'].find(url) != -1:  #if ignore url is found in line - we ignore
                return 0

    if start_at:
        start_date_object = datetime.datetime.strptime(start_at, "%d/%b/%Y %H:%M:%S") #IF FORMAT IS CORRECT
        date_object = datetime.datetime.strptime(parsed_line['date'], "%d/%b/%Y %H:%M:%S")
        if start_date_object > date_object:
            return 0

    if stop_at:
        stop_date_object = datetime.datetime.strptime(stop_at, "%d/%b/%Y %H:%M:%S")  # IF FORMAT IS CORRECT
        date_object = datetime.datetime.strptime(parsed_line['date'], "%d/%b/%Y %H:%M:%S")
        if stop_date_object < date_object:
            return 0

    if request_type:
        if parsed_line['url_method'] != request_type: #if requets type isnt desirable - ignore line
            return 0

    if ignore_www:
        if parsed_url.netloc[0:4] == 'www.':
            remove_from_index = parsed_line['url_adress'].find(parsed_url.netloc)
            parsed_line['url_adress'] = parsed_line['url_adress'][:remove_from_index]+parsed_line['url_adress'][remove_from_index+4:]

    return 1

def getTop5(URLs_dictionary):
    returnArray = []
    resetArray = []
    for i in range(0, 5):
        resetArray.append(max(URLs_dictionary, key=URLs_dictionary.get))
        returnArray.append(URLs_dictionary[resetArray[i]])
        URLs_dictionary[resetArray[i]] = -1
    # resetting changes back
    for i in range(0, 5):
        URLs_dictionary[resetArray[i]] = returnArray[i]
    return returnArray

def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):
    file = open('log.log')
    URLs_dictionary = {}

    for line in file:
        parsed_line = parseLine(line)
        if(parsed_line != 0): #line is acceptable
            if(checkAndModifyLogLine(parsed_line, ignore_files, ignore_urls, start_at, stop_at, request_type, ignore_www)): #all params are suitable and line changed according to params
                parsed_url = urlparse(parsed_line['url_adress'])

                if parsed_url.scheme == 'http' or parsed_url.scheme == 'https':
                    key = parsed_url.netloc + parsed_url.path
                else:
                    key = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path

                if not slow_queries: #without avarage count
                    URLs_dictionary[key] = URLs_dictionary.get(key,0) + 1
                else:
                    URLs_dictionary[key] = URLs_dictionary.get(key, [])
                    URLs_dictionary[key].append(parsed_line['response_time'])

    if slow_queries:
        for key, value in URLs_dictionary.items():
            URLs_dictionary[key] = int(statistics.mean(value))
    #print(URLs_dictionary)

    returnArray = getTop5(URLs_dictionary)
    file.close()

    return returnArray
