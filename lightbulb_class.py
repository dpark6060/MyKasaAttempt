#!/usr/bin/env python
import requests
import json
from multiprocessing import Pool
import time
global token
import random
import asyncio
import aiofiles
import aiohttp

uuid = ""
baseurl = "https://wap.tplinkcloud.com/"



class lightbulb:
    def __init__(self, token, deviceId, name=''):
        self.deviceId = deviceId
        self.hue=0
        self.on=1
        self.brightness=100
        self.saturation=100
        self.token = token
        self.next_bulb = None
        self.prev_bulb = None
        self.name = name
        self.party_hues = [242, 315, 0, 120, 174]
        
    def set_next(self, bulb):
        self.next_bulb = bulb
        
    def set_prev(self, bulb):
        self.prev_bulb = bulb
    
    def get_next(self):
        return(self.next_bulb)
    
    def get_prev(self):
        return(self.prev_bulb)
    

    def random_party_hue(self):
        new_hue = random.choice(self.party_hues)
        while new_hue == self.hue:
            new_hue = random.choice(self.party_hues)
        return(new_hue)
    
        


    def random_hue(self):
        current_hue = self.hue
        new_hue = (current_hue + 90)%360
        new_hue = new_hue + int(20*(random.random()-.5))
        self.hue=new_hue
        return(new_hue)
    
    def post(self, data):
        dest_url = f"https://wap.tplinkcloud.com/?token={self.token}"    
        result = requests.post(dest_url,json=data)
        return(result)
        
    def apost(self, client, data):
        pass
    
    def hard_off(self):
        data_string = {"smartlife.iot.smartbulb.lightingservice":{
                "transition_light_state":{
                    "on_off": 0
                    }
                }
            }
        
        data_full = {"method": "passthrough",
                     "params":{
                        "deviceId":self. deviceId,
                        "requestData": json.dumps(data_string)
                         }
                    }
        
        self.post(data_full)      
        
    def off(self):
        data_string = {"smartlife.iot.smartbulb.lightingservice":{
                "transition_light_state":{
                    "brightness": 0
                    }
                }
            }
        
        data_full = {"method": "passthrough",
                     "params":{
                        "deviceId":self. deviceId,
                        "requestData": json.dumps(data_string)
                         }
                    }
        
        self.post(data_full)        
    
    def on(self):
        data_string = {"smartlife.iot.smartbulb.lightingservice":{
                "transition_light_state":{
                    "on_off": 1
                    }
                }
            }
        
        data_full = {"method": "passthrough",
                     "params":{
                        "deviceId":self. deviceId,
                        "requestData": json.dumps(data_string)
                         }
                    }
        
        self.post(data_full)     


    def set_to_color_mode(self):
        
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
                        "deviceId": self.deviceId,
                        "requestData": json.dumps(data_string)
                         }
                    }
                     
        self.post(data_full)



    def flash(self,hue,t=0):
        self.hue=hue
        data_string = {"smartlife.iot.smartbulb.lightingservice":{
                "transition_light_state":{
                "hue": hue,
                "saturation": 100,
                "color_temp": 0,
                "brightness": 100,
                }
            }
        }
        
        data_full = {"method": "passthrough",
                     "params":{
                        "deviceId": self.deviceId,
                        "requestData": json.dumps(data_string)
                         }
                    }
                     
        self.post(data_full)
        time.sleep(t)
        self.off()



    def set_hue(self, hue):
        self.hue = hue
        #data_string = "{\"smartlife.iot.smartbulb.lightingservice\":{\"transition_light_state\":{\"hue\":"+str(hue)+"}}}"
        data_string = {"smartlife.iot.smartbulb.lightingservice":{
            "transition_light_state":{
                "hue":hue}}}
        
        
        data_full = {"method": "passthrough",
                     "params":{
                        "deviceId": self.deviceId,
                        "requestData": json.dumps(data_string)
                         }
                    }
        self.post(data_full)
        

    async def aset_hue(self, hue, client):
        
        #data_string = "{\"smartlife.iot.smartbulb.lightingservice\":{\"transition_light_state\":{\"hue\":"+str(hue)+"}}}"
        data_string = {"smartlife.iot.smartbulb.lightingservice":{
            "transition_light_state":{
                "hue":hue}}}
        
        
        data_full = {"method": "passthrough",
                     "params":{
                        "deviceId": self.deviceId,
                        "requestData": json.dumps(data_string)
                         }
                    }
        dest_url = f"https://wap.tplinkcloud.com/?token={self.token}"    
        result = await client.request(method="POST",url=dest_url, data=json.dumps(data_full))
        
        return(result)




class bulb_group:
    def __init__(self, token, deviceIds, name=''):
        self.deviceIds = deviceIds
        self.hue=0
        self.on=1
        self.brightness=100
        self.saturation=100
        self.token = token
        self.next_bulb = None
        self.prev_bulb = None
        self.name = name
        self.party_hues = [242, 315, 0, 120, 174]
        
    def set_next(self, bulb):
        self.next_bulb = bulb
        
    def set_prev(self, bulb):
        self.prev_bulb = bulb
    
    def get_next(self):
        return(self.next_bulb)
    
    def get_prev(self):
        return(self.prev_bulb)
    

    def random_party_hue(self):
        new_hue = random.choice(self.party_hues)
        while new_hue == self.hue:
            new_hue = random.choice(self.party_hues)
        return(new_hue)
    
        


    def random_hue(self):
        current_hue = self.hue
        new_hue = (current_hue + 90)%360
        new_hue = new_hue + int(20*(random.random()-.5))
        self.hue=new_hue
        return(new_hue)
    
    def post(self, data):
        dest_url = f"https://wap.tplinkcloud.com/?token={self.token}"    
        result = requests.post(dest_url,json=data)
        print(result)
        print(result.text)
        return(result)

    
    def hard_off(self):
        data_string = {"smartlife.iot.smartbulb.lightingservice":{
                "transition_light_state":{
                    "on_off": 0
                    }
                }
            }
        
        data_full = {"method": "passthrough",
                     "params":{
                        "deviceId":self. deviceId,
                        "requestData": json.dumps(data_string)
                         }
                    }
        
        self.post(data_full)      
        
    def off(self):
        data_string = {"smartlife.iot.smartbulb.lightingservice":{
                "transition_light_state":{
                    "brightness": 0
                    }
                }
            }
        
        data_full = {"method": "passthrough",
                     "params":{
                        "deviceId":self. deviceId,
                        "requestData": json.dumps(data_string)
                         }
                    }
        
        self.post(data_full)        
    
    def on(self):
        data_string = {"smartlife.iot.smartbulb.lightingservice":{
                "transition_light_state":{
                    "on_off": 1
                    }
                }
            }
        
        data_full = {"method": "passthrough",
                     "params":{
                        "deviceId":self. deviceId,
                        "requestData": json.dumps(data_string)
                         }
                    }
        
        self.post(data_full)     


    def set_to_color_mode(self):
        
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
                        "deviceId": self.deviceId,
                        "requestData": json.dumps(data_string)
                         }
                    }
                     
        self.post(data_full)



    def set_hue(self, hue):
        self.hue = hue
        #data_string = "{\"smartlife.iot.smartbulb.lightingservice\":{\"transition_light_state\":{\"hue\":"+str(hue)+"}}}"
        data_string = {"smartlife.iot.smartbulb.lightingservice":{
            "transition_light_state":{
                "hue":hue}}}
        
        # Tried params as a list of dicts with different ID's
        # Tried a simple list of device IDs
        # Tried just passing in a list to device ID (self.params)

        
        data_full = {"method": "passthrough",
                     "params": {"deviceId": self.deviceIds,
                        "requestData": json.dumps(data_string)}
                    }
        print('')
        print(data_full)
        print('')
        self.post(data_full)
        
    
    def get_list(self, get):
        data_full = {"method":get}
        self.post(data_full)






def get_token():
    
    data = {
            "method": "login",
            "params": {
            "appType": "Kasa_Android",
            "cloudUserName": "",
            "cloudPassword": "",
            "terminalUUID": uuid
            }
           }
    
    d=requests.post(baseurl, json=data)
    print(d)
    print(d.text)
    
    token = d.json()['result']['token']
    return(token)