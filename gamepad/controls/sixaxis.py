import threading

joy = { 'leftx': 0.0, 'lefty': 0.0, 'rightx': 0.0, 'righty': 0.0,
        'triangle' : False,
        'circle' : False,
        'cross' : False,
        'square' : False,
        'R1' : False,
        'R2' : False,
        'L1' : False,
        'L2' : False,
        'select' : False,
        'start' : False,
        'PS3' : False,
        'up' : False,
        'down' : False,
        'left' : False,
        'right' : False,
        }

running = 1

class ThreadClass(threading.Thread):
    def run(self):
        global pipe
        global action
        global spacing
        global running

        while running:
            for character in pipe.read(1):
                action += ['%02X' % ord(character)]
                
                if len(action) == 8:

                    num = int(action[5], 16)
                    percent254 = str(((float(num) - 128.0) / 126.0) - 100)[4:6]
                    percent128 = str((float(num) / 127.0))[2:4]

                    if percent254 == '.0':
                        percent254 = '100'
                    if percent128 == '0':
                        percent128 = '100'

                    if action[6] == '02' and (action[7] == '05' or action[7 == '04']):  # Arrow Buttons
                        if action[5] == '00':  # released (arrow Button)
                            if action[7] == '05' and action[4] == '00':
                                joy['up'] = False
                                joy['down'] = False
                            if action[7] == '04' and action[4] == '00':
                                joy['left'] = False
                                joy['right'] = False
                        else:  # pressed (arrow Button)
                            if action[7] == '05' and action[4] == '01':
                                joy['up'] = True
                            if action[7] == '05' and action[4] == 'FF':
                                joy['down'] = True
                            if action[7] == '04' and action[4] == '01':
                                joy['left'] = True
                            if action[7] == '04' and action[4] == 'FF':
                                joy['right'] = True
                        
                    if action[6] == '01':  # Button pressed/released
                        if action[4] == '01':  # pressed (Button)
                            if action[7] == '00':
                                joy['square'] = True
                            if action[7] == '01':
                                joy['cross'] = True 
                            if action[7] == '02':
                                joy['circle'] = True
                            if action[7] == '03':
                                joy['triangle'] = True
                            if action[7] == '04':
                                joy['L1'] = True
                            if action[7] == '05':
                                joy['R1'] = True
                            if action[7] == '06':
                                joy['L2'] = True
                            if action[7] == '07':
                                joy['R2'] = True
                            if action[7] == '08':
                                joy['select'] = True
                                running = 0
                            if action[7] == '09':
                                joy['start'] = True
                            if action[7] == '0C':
                                joy['PS3'] = True
                        else:  # released (Button)
                            if action[7] == '00':
                                joy['square'] = False
                            if action[7] == '01':
                                joy['cross'] = False 
                            if action[7] == '02':
                                joy['circle'] = False
                            if action[7] == '03':
                                joy['triangle'] = False
                            if action[7] == '04':
                                joy['L1'] = False
                            if action[7] == '05':
                                joy['R1'] = False
                            if action[7] == '06':
                                joy['L2'] = False
                            if action[7] == '07':
                                joy['R2'] = False
                            if action[7] == '08':
                                joy['select'] = False
                            if action[7] == '09':
                                joy['start'] = False
                            if action[7] == '0C':
                                joy['PS3'] = False

                    elif action[7] == '00':
                        num = int(action[5], 16)
                        if num >= 128:
                            joy['leftx'] = -int(percent254)
                        elif num <= 127 \
                        and num != 0:
                            joy['leftx'] = int(percent128)
                        else:
                            joy['leftx'] = 0


                    elif action[7] == '01':
                        num = int(action[5], 16)
                        if num >= 128:
                            joy['lefty'] = -int(percent254)
                        elif num <= 127 \
                        and num != 0:
                            joy['lefty'] = int(percent128)
                        else:
                            joy['lefty'] = 0


                    elif action[7] == '02':
                        num = int(action[5], 16)
                        if num >= 128:
                            joy['rightx'] = -int(percent254)
                        elif num <= 127 \
                        and num != 0:
                            joy['rightx'] = int(percent128)
                        else:
                            joy['rightx'] = 0

                    elif action[7] == '03':
                        num = int(action[5], 16)
                        if num >= 128:
                            joy['righty'] = -int(percent254)
                        elif num <= 127 \
                        and num != 0:
                            joy['righty'] = int(percent128)
                        else:
                            joy['righty'] = 0
                                
                    # print action
                    action = []
                    
t = ThreadClass()

def init(path):
    global pipe
    global action
    global spacing
    running = 1
    action = []
    spacing = 0
    try:
        pipe = open(path, 'r')
    except:
        return False
    t.deamon = True
    t.start()
    return True

def get_state():
    global joy
    return joy

def isRunning():
    global running
    return running
    
def shutdown():
    global running    
    running = 0
    t.join()
