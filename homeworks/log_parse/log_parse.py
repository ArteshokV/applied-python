# -*- encoding: utf-8 -*-
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
    for line in file:
        parsed_line = parseLine(line)
        if(parsed_line != 0):
            o = urlparse(parsed_line['url_adress'])
            #o.netloc
            #o.path
            print(o.netloc + o.path)


    file.close()
    return []
