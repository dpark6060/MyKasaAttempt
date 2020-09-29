#!/usr/bin/env python
import http3
import itertools
import asyncio
import requests
import json
from multiprocessing import Pool
import time
uuid = "46cf6b44-4dc1-464e-8e6a-83a504b59e24"
baseurl = "https://wap.tplinkcloud.com/"
global token
import random
from aiohttp import ClientSession
import lightbulb_class as lc


colors = { "livingroom2": "8012B3DF47C4741986C06CA1A7BEB11B1CF8226A",
            "bedroom 1": "80124473D31C5733151D95F44BA0C7711C5E8FB5",
            "br_hallway_color": "8012BB11DEDA5093517240A6CF69C8A61CF7D91E",
            "kt_hallway_color": "80120FB5D03E04E999F4BD4D641FAFEE1D1A3F77",
            "livingroom1":"80125C0B89DAEAB1AA5406A4C47171641D1A95A5",
            "bedroom 2": "801246B0BCCAE659F048C513607844A61C5EAC18"
            }

ordered_list = ['bedroom 1','bedroom 2','br_hallway_color','kt_hallway_color','livingroom2','livingroom1']

whites = {  "br_hallway_white": "80122E59337B7E8470EFDF143167A5431B7DB743",
            "kt_hallway_white":"8012AE904B1147A9F0BC70B58F2A25E91B7DEEE5"}



token = lc.get_token()


lb1=lc.lightbulb(token,colors['bedroom 1'],'bedroom 1')
lb2=lc.lightbulb(token,colors['bedroom 2'],'bedroom 2')
lb3=lc.lightbulb(token,colors['br_hallway_color'],'br_hallway_color')
lb4=lc.lightbulb(token,colors['kt_hallway_color'],'kt_hallway_color')
lb5=lc.lightbulb(token,colors['livingroom2'],'livingroom2')
lb6=lc.lightbulb(token,colors['livingroom1'],'livingroom1')

bulb_list = [lb1,lb2,lb3,lb4,lb5,lb6]
print(bulb_list)

def daisy_chain_bulbs(bulb_list):
    
    for i in range(1,len(bulb_list)-1):
        bulb=bulb_list[i]
        prev = bulb_list[i-1]
        nxt = bulb_list[i+1]
        
        bulb.set_next(nxt)
        bulb.set_prev(prev)
    
    bulb = bulb_list[0]
    bulb.set_next(bulb_list[1])
    bulb.set_prev(bulb_list[-1])
    
    bulb = bulb_list[-1]
    bulb.set_prev(bulb_list[-2])
    bulb.set_next(bulb_list[0])
    
    return(bulb_list)


def pulse(dc_bulbs, npulse):
    
    
    bulb=dc_bulbs[0]
    hues = itertools.cycle([0,120,240])
    ipulse = 0
    hue = next(hues)
    while npulse != 0:
        
        print(hue)
        print(bulb.name)
        bulb.flash(hue,.1)
        bulb = bulb.get_next()
        npulse = npulse-1
        
        if ipulse%len(dc_bulbs) == 0:
            hue = next(hues)
            
        ipulse+=1
            
    pass



async def post_async(data):
    global token
    dest_url = f"https://wap.tplinkcloud.com/?token={token}"
    result = await requests.post(dest_url,json=data)
    print(result)

def post(data):
    global token
    dest_url = f"https://wap.tplinkcloud.com/?token={token}"    
    result = requests.post(dest_url,json=data)
    print(result)
    


def off(deviceId):
    data_string = {"smartlife.iot.smartbulb.lightingservice":{
            "transition_light_state":{
                "on_off": 0
                }
            }
        }
    
    data_full = {"method": "passthrough",
                 "params":{
                    "deviceId": deviceId,
                    "requestData": json.dumps(data_string)
                     }
                }
    
    post(data_full)


def list_off(devices):
    
    for name, deviceId in devices.items():
        off(deviceId)


def on(deviceId):
    data_string = {"smartlife.iot.smartbulb.lightingservice":{
        "transition_light_state":{
            "on_off": 1
            }
        }
    }

    data_full = {"method": "passthrough",
                 "params":{
                    "deviceId": deviceId,
                    "requestData": json.dumps(data_string)
                     }
                }
    
    post(data_full)



def list_on(devices):
    
    for name, deviceId in devices.items():
        on(deviceId)



def set_hue(deviceId, hue):
    
    #data_string = "{\"smartlife.iot.smartbulb.lightingservice\":{\"transition_light_state\":{\"hue\":"+str(hue)+"}}}"
    data_string = {"smartlife.iot.smartbulb.lightingservice":{
        "transition_light_state":{
            "hue":hue}}}
    
    
    data_full = {"method": "passthrough",
                 "params":{
                    "deviceId": deviceId,
                    "requestData": json.dumps(data_string)
                     }
                }
    post(data_full)
    
    

    

def set_to_color_mode(deviceId):
    
    data_string = {"smartlife.iot.smartbulb.lightingservice":{
        "transition_light_state":{
            "hue": 0,
            "saturation": 100,
            "color_temp": 0,
            "brightness": 100
            }
        }
    }
    
    data_full = {"method": "passthrough",
                 "params":{
                    "deviceId": deviceId,
                    "requestData": json.dumps(data_string)
                     }
                }
                 
    return(data_full)


def party(deviceId):
    
    next_hue = 0
    while True:
        print(next_hue)
        set_hue(deviceId, next_hue)
        next_hue = random_hue(next_hue)
        time.sleep(.35)

    pass

def random_hue(current_hue):
    new_hue = (current_hue + 90*[-1 if random.random()<0.5 else 1][0] )%360
    new_hue = new_hue + int(20*(random.random()-.5))
    return(new_hue)

    
def full_party():
    color_ids = list(colors.values())
    n_pool = len(color_ids)
    
    with Pool(n_pool) as p:
        p.map(party,color_ids)
        


def full_party2():
    color_ids = list(colors.values())
    
    bulbs = [lc.lightbulb(token, cid) for cid in color_ids]
    
    randomize_bulbs(bulbs)
    print('3...')
    time.sleep(1)
    print('2...')
    time.sleep(1)
    print('1...')
    time.sleep(1)
    print('boosters')
    time.sleep(1)
    
    while True:
        for abulb in bulbs:
            hue = abulb.random_hue()
            abulb.set_hue(hue)
            #time.sleep(.1)
        
            

def randomize_bulbs(bulbs):
    
    for abulb in bulbs:
        hue = int(random.random()*360)
        abulb.set_hue(hue)



def setup():
    
    list_on(colors)
    list_off(whites)
    
    for name,deviceId in colors.items():
        data_full = set_to_color_mode(deviceId)
        post(data_full)
    
    off(whites)

def run_test():
    
    hue = 100
    get_token()
   # call = set_hue(deviceId, hue)
    list_off(whites)
    list_off(colors)
    did="801246B0BCCAE659F048C513607844A61C5EAC18"
    on(did)
    set_hue(did,20)
    party(did)
    
    
def run_full_test():
    get_token()
    setup()
    full_party2()
    

async def set_hue_async(deviceId, hue, session):
    global token
    #data_string = "{\"smartlife.iot.smartbulb.lightingservice\":{\"transition_light_state\":{\"hue\":"+str(hue)+"}}}"
    data_string = {"smartlife.iot.smartbulb.lightingservice":{
        "transition_light_state":{
            "hue":hue}}}
    
    
    data_full = {"method": "passthrough",
                 "params":{
                    "deviceId": deviceId,
                    "requestData": json.dumps(data_string)
                     }
                }
         
    dest_url = f"https://wap.tplinkcloud.com/?token={token}"
    
    print(data_full)
    
    result = await session.request(method='POST',url=dest_url, data=json.dumps(data_full))
    result.raise_for_status()
    html = await result.text()
    print(result)
    print(html)
    return(html)

def make_hue_data(deviceId,hue):
    global token
    #data_string = "{\"smartlife.iot.smartbulb.lightingservice\":{\"transition_light_state\":{\"hue\":"+str(hue)+"}}}"
    data_string = {"smartlife.iot.smartbulb.lightingservice":{
        "transition_light_state":{
            "hue":hue}}}
    
    
    data_full = {"method": "passthrough",
                 "params":{
                    "deviceId": deviceId,
                    "requestData": json.dumps(data_string)
                     }
                }
         
    dest_url = f"https://wap.tplinkcloud.com/?token={token}"
    
    return(dest_url,data_full)
    


async def run_async_test():
    hues = [200]
    dids=["80124473D31C5733151D95F44BA0C7711C5E8FB5",
          "801246B0BCCAE659F048C513607844A61C5EAC18"]
    get_token()
    setup()
    
    async with ClientSession() as session:
        tasks = []
        for i in range(10):
            for hue in hues:
                for di in dids:
                    tasks.append(set_hue_async(di,hue,session))
        
        await asyncio.gather(*tasks)
        


async def run_async_test2():
    hues = [200,0]
    dids=["80124473D31C5733151D95F44BA0C7711C5E8FB5",
          "801246B0BCCAE659F048C513607844A61C5EAC18"]
    get_token()
    setup()
    
    async with http3.AsyncClient() as client:
        for hue in hues:
            for di in dids:
                url,data=make_hue_data(di,hue)
                r = await client.post(url,json.dumps(data))
                print(r)
            
        

        
    


def run_nonasync_test():
    hues = [0,200]
    dids=["80124473D31C5733151D95F44BA0C7711C5E8FB5",
          "801246B0BCCAE659F048C513607844A61C5EAC18"]
    

    get_token()
   # call = set_hue(deviceId, hue)
    setup()
    
    for di in dids:
        on(di)
    
    for i in range(10):
        for hue in hues:
            for di in dids:
                set_hue(di,hue)
                time.sleep(0.17)
    
#asyncio.run(run_async_test2())
#asyncio.run(run_async_test())
#run_async_test()


async def alternate_pulse(dc_lights, hue):

    tasks = []
    async with ClientSession() as client:
        
        for b in dc_lights:
            await b.aset_hue(hue,client)
            await asyncio.sleep(0.025)
        
        
def check_bedroom_status():
    
    token = lc.get_token()
    #token = "1434b640-ATCO6ALc6JJNnXTXYkKnZd0"
    bid='80124473D31C5733151D95F44BA0C7711C5E8FB5'
    url=f"https://wap.tplinkcloud.com?token={token}"
    bulb = lc.lightbulb(token, bid)
    
    data={"method": "getDeviceList"}

    #data_string = {"smartlife.iot.smartbulb.lightingservice":{}}
    data = {"system":{"get_sysinfo":"null"},"emeter":{"get_realtime":"null"}} 
    
    data_full = {"method": "passthrough",
                 "params":{
                    "deviceId": bid,
                    "requestData": json.dumps(data)
                     }
                }

    result = bulb.post(data_full)
    print('')
    print('')
    #print(json.loads(result.text))
    a=json.loads(result.text)['result']['responseData']
    a=json.loads(a)
    print(a['system']['get_sysinfo']['light_state'])
    
    print('')
    print('')
    
    #print(result.text)

def full_party3():
    color_ids = list(colors.values())
    
    bulbs = [lc.lightbulb(token, cid) for cid in color_ids]
    
    randomize_bulbs(bulbs)
    print('3...')
    time.sleep(1)
    print('2...')
    time.sleep(1)
    print('1...')
    time.sleep(1)
    print('boosters')
    time.sleep(1)
    
    while True:
        for abulb in bulbs:
            hue = abulb.random_party_hue()
            abulb.set_hue(hue)
            time.sleep(.05)
        
#setup()
#full_party3()

# dc_list = daisy_chain_bulbs(bulb_list)
# 
# for bulb in dc_list:
#     print(f"{bulb.get_prev().name} -> {bulb.name} -> {bulb.get_next().name}")
# 
# hues=itertools.cycle(list(range(0,360,60)))
# hue=next(hues)
# while True:
#     asyncio.run(alternate_pulse(dc_list, hue))
#     hue=next(hues)
#     


#pulse(dc_list,-1)

# token = lc.get_token()
# group = ["80124473D31C5733151D95F44BA0C7711C5E8FB5", "801246B0BCCAE659F048C513607844A61C5EAC18"]
# 
# bulb_group = lc.bulb_group(token, group)
# bulb_group.get_list('getGroupList')
# bulb_group.set_hue(0)



#colors={'blue':242, 'mag':315,'red':0,'green':120,'cyan':174}




# import socket
# port = 80
# sock = socket.socket()
# sock.connect((address, port)
# then
# sock.send('HTTP/1.1 .... POST blah blah')
# 
# 
# 
# 
# 
# 
# ip_addresses = [ x, y, z ... ]
# sockets = []
# 
# for bulb in ip_addresses:
#   sock = socket.socket()
#   sock.connect((bulb, port)
#   sock.send('HTTP/1.1 .... POST blah blah\n\n')
#   sockets.append(sock)
# 
# sleep 0.1
# 
# for sock in sockets:
#   sock.close()

def echo_thing(thing):
    print(f'process {thing}')


things = [1,2,3,4,5,6,7,8,9]
pp = Pool.map(echo_thing, things)
pp.wait()

#process = subprocess.Popen(['curl', 'args'...])
s = subprocess.Popen(['sleep', '60'])
s.poll()



Python 3.8.5 (default, Jul 21 2020, 10:48:26)
[Clang 11.0.3 (clang-1103.0.32.62)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import subprocess
>>> s = subprocess.Popen(['sleep', '60'])
>>> s.poll()
>>> print(s.poll())
None
>>> print(s.poll())
None
>>> print(s.poll())
None
>>> print(s.poll())
None
>>> print(s.poll())
None
>>> print(s.poll())
None
>>> print(s.poll())
None
>>> print(s.poll())
0
>>>