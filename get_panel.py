from serialTeste import *
import time

def switchCase(var):
    switcher = {
        '00': [0,0,0,0],
        '01': [0,0,0,1],
        '02': [0,0,1,0],
        '03': [0,0,1,1],
        '04': [0,1,0,0],
        '07': [0,1,1,1],
        '08': [1,0,0,0],
        '0f': [1,1,1,1]
    }
    return switcher.get(var, 'invalid configuration')
    
def getPanel():
    
    panel_value = get_value('02')
    
    if(panel_value[0:2] == '99'):
        panel_value = panel_value[2:]
    else:
        return 'error: message has no ACK'
    if(panel_value[0:2] == '02'):
        panel_value = panel_value[2:]
        print('responding to command 0x02')
    else:
        return 'error: response to unrequired command'
    if(panel_value[len(panel_value)-1:len(panel_value)-2] == 'ff'):
        panel_value = panel_value[:len(panel_value)-2]
    else:
        return 'error: message has no FIN'
    if(panel_value == '4552524fa'):
        print("Requisition not properly sent. Will try again in 5 seconds")
        time.sleep(5)
        return getPanel()

    return switchCase(panel_value)