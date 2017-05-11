##General Calls
import time
import serial

##Pubnub Calls
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
 
##Pubnub Configuration
pnconfig = PNConfiguration() 
pnconfig.subscribe_key = 'sub-c-c3322f58-e285-11e6-8d2d-02ee2ddab7fe'
pnconfig.publish_key = 'pub-c-3942c648-843c-496f-92cd-72c9f7208d04'
pnconfig.ssl = False
channel1 = 'EAP_ts1'
channel2 = 'EAP_ts2'
pubnub = PubNub(pnconfig)
 
def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
 
 
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
 
        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel(channel1).message("Connected").async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
 
    def message(self, pubnub, message):
        pass  # Handle new message stored in message.message
 
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(channel1).execute()

ser = serial.Serial('/dev/ttyUSB0', 9600)
var = 0
t = []
y = []

raw_data = ser.readline()
raw_data = ser.readline()

while (var <5000):
    raw_data = ser.readline(17)
    s = str(raw_data)
    end = s.find('%')
    cnts = float(s[1:end])
    strain = cnts
#    t.append(var)
#    y.append(cnts)    
    var = var + 1    
    pubnub.publish().channel(channel1).message({'eon': [strain]}).async(my_publish_callback)
    print (var, strain)
#    time.sleep(1)

print("All Done!!") 
pubnub.publish().channel(channel1).message("All Done!!").async(my_publish_callback)
