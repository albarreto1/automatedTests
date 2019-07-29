# -*- coding: utf-8 -*-
from serialTeste import set_config, get_value
from potMask import mask10, mask20, mask40, mask60, getCurve
from get_panel import getPanel
from get_buzzer import getBuzzer
from get_led_voltage import getPotLum
from get_batlvl import getBatLvl
import random
import time

def switchCase2(var):
    switcher = {
        '[0, 0, 0, 1]': 60,
        '[0, 0, 1, 0]': 40,
        '[0, 1, 0, 0]': 20,
        '[1, 0, 0, 0]': 10,
        '[0, 0, 0, 0]': 0
    }
    return switcher.get(var, 'invalid configuration')

#Cenário SETA 1:
def testscenario1():
    FILE = open('testscenario1.txt', 'a')
    set_config('01', '12', '0a')
    time.sleep(1)

    set_config('01', '12', '0a')
    time.sleep(1)
    
    set_config('01', '11', '0a')
    time.sleep(1)
    panel_before = switchCase2(str(getPanel()))

    set_config('01', '11', '0a')
    time.sleep(1)
    panel_after = switchCase2(str(getPanel()))

    buz = getBuzzer()
    if(len(buz) == 0):
        print(buz, file = FILE)
        FILE.close()
        return False
    else:
        if(panel_before == 10):
            if(panel_after == 20):
                return True
            else:
                print(panel_before, '\t', panel_after, file = FILE)
                return False
        elif(panel_before == 20):
            if(panel_after == 40):
               return True
            else:
                print(panel_before, '\t', panel_after, file = FILE)
                return False
        elif(panel_before == 40):
            if(panel_after == 60):
                return True
            else:
                print(panel_before, '\t', panel_after, file = FILE)
                return False
        elif(panel_before == 60):
            if(panel_after == 10):
                return True
            else:
                print(panel_before, '\t', panel_after, file = FILE)
                return False
        else:
            return False

#Cenário SETA 2:
def testscenario2():
    FILE = open('testscenario2.txt', 'a')

    set_config('01', '12', '02')
    time.sleep(0.2)
    set_config('01', '12', '02')
    time.sleep(0.2)
    
    set_config('01', '11', '02')
    time.sleep(0.2)
    panel_before = switchCase2(str(getPanel()))

    set_config('01', '12', '02')
    time.sleep(0.2)

    time.sleep(5)

    set_config('01', '11', '02')
    time.sleep(0.2)
    panel_after = switchCase2(str(getPanel()))

    buz = getBuzzer()
    if(len(buz) == 0):
        print(buz, file = FILE)
        FILE.close()
        return False
    else:
        if(panel_before == 10):
            if(panel_after == 20):
                return True
            else:
                print(panel_before, '\t', panel_after, file = FILE)
                return False
        elif(panel_before == 20):
            if(panel_after == 40):
               return True
            else:
                print(panel_before, '\t', panel_after, file = FILE)
                return False
        elif(panel_before == 40):
            if(panel_after == 60):
                return True
            else:
                print(panel_before, '\t', panel_after, file = FILE)
                return False
        elif(panel_before == 60):
            if(panel_after == 10):
                return True
            else:
                print(panel_before, '\t', panel_after, file = FILE)
                return False
        else:
            return False

#Cenário ON/OFF 1:
def testscenario3():
    FILE = open('testscenario3.txt', 'a')
    set_config('01', '11', '02')
    time.sleep(0.2)

    rtime = random.randint(2, 9)
    rhex = hex(rtime)[2:]
    if(len(rhex) < 2):
        rhex = '0' + rhex

    set_config('01', '12', rhex)
    time.sleep(rtime/10)

    buz = getBuzzer()
    if(len(buz) == 0):
        print('erro: não houve beep:\t{}'.format(buz), file=FILE)
        return False

    panel = getPanel()
    profile = switchCase2(str(panel))
    
    now = time.time()
    future = now + profile
    while(now <= future):
        if(panel != getPanel()):
            print('erro. led não corresponde ao perfil ativado:\t{}\t{}\t{}'.format(profile, panel, getPanel()), file=FILE)
            return False
        now = time.time()
    return True

#Cenário ON/OFF 2:
def testscenario4():
    FILE = open('testscenario4.txt', 'a')

    set_config('01', '11', '02')
    time.sleep(0.2)

    set_config('01', '12', '02')
    time.sleep(0.2)

    panel = getPanel()
    profile = switchCase2(str(panel))

    rtime = random.randint(1, profile-3)
    time.sleep(rtime)

    set_config('01', '12', '02')
    time.sleep(0.2)

    if(getPotLum() != 0):
        print('erro: led de cura nao desligou: {}\t{}\t{}'.format(profile, rtime, getPotLum()), file=FILE)
        return False
    else:
        return True


def main():
    
    #sceneOne()
        # sceneTwo()
    #   sceneThree()
    
    #   sceneFour() ##Cenário quatro precisa da bateria a 3.8 ou abaixo
    cont = 0
    initialTime = time.time()
    for i in range(50):
            print("Round ", i)
            # aux  = sceneOne()
            # aux = sceneTwo()
            # aux = sceneThree()

            aux = testscenario4() ##Cenário quatro precisa da bateria a 3.8 ou abaixo
        
            if(aux):
                cont = cont + 1
            
            time.sleep(1)

    
    
    print("Successful tests percentage: ", (cont/50)*100)

    print("Unsuccessful tests percentage: ", ((50 - cont)/50) * 100)

    print("Elapsed time: ", time.time() - initialTime)


    with open('output_TC2s.txt', 'a') as f:
            print("Scene Four:")

            print("Successful tests percentage: ", (cont/50)*100, file=f)

            print("Unsuccessful tests percentage: ", ((50 - cont)/50) * 100, file=f)

            print("Elapsed time: ", time.time() - initialTime, file = f)

            print("############# END ###########\n\n", file=f)
    
    f.close()

if __name__ == "__main__":
  main()