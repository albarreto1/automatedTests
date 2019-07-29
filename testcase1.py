# -*- coding: utf-8 -*-
from serialTeste import set_config, get_value, set_sampling
from potMask import mask10, mask20, mask40, mask60, getCurve
from get_panel import getPanel
from get_buzzer import getBuzzer
from get_led_voltage import getPotLum
from get_batlvl import getBatLvl
import random
import time

## Cenário 1: SETA
# Subcenário 1:
def switchCase2(var):
    switcher = {
        '[0, 0, 0, 1]': 60,
        '[0, 0, 1, 0]': 40,
        '[0, 1, 0, 0]': 20,
        '[1, 0, 0, 0]': 10,
    }
    return switcher.get(var, 'invalid configuration')

def getIndex(var1 = [] ,var2 = []):
    index1 = 0
    index2 = 0
    if(var1 == None or var2 == None):
        return 'um dos vetores está vazio'
    else:    
        for i in range(len(var1)):
            if(var1[i] == 1):
                index1 = i
        for j in range(len(var2)):
            if(var2[j] == 1):
                index2 = j
        return index1, index2

#Cenário SETA
#Subcenário 1
def testscenario1():
    FILE = open('TC1_SETA1_SUB_1.txt', 'a')
    rtime = random.randint(10, 30)
    rhex = hex(rtime)[2:]
    if(len(rhex) < 2):
        rhex = '0' + rhex
        FILE = open('randinfo.txt', 'w')
        FILE.write('{}\n'.format(rtime))
        FILE.close()
    
    set_config('01', '11', '0A')
    time.sleep(1)
    panel_before = getPanel()

    set_config('01', '11', rhex)
    time.sleep((rtime/10))


    panel_after = getPanel()
    i, j = getIndex(panel_before, panel_after)

    if((j - i) == 1 or (i - j) == 3):
        print("teste ok")
        print(j , i)
        return True
    else:
        print('falha. a ativacao de seta 1 vez nao mudou o perfil na ordem estabelecida')
        print(j, i, file = FILE)
        FILE.close()
        return False
    
#subcenário 2
def testscenario2():
    rtime = random.randint(2, 14)
    rhex = hex(rtime)[2:]
    if(len(rhex) < 2):
        rhex = '0' + rhex
    
    set_config('01', '12', '02')
    time.sleep(0.3)
    set_config('01', '12', '02')
    time.sleep(0.2)

    panel_before = getPanel()
    set_config('01', '12', '02')
    time.sleep(0.2)
    
    time.sleep(5)

    set_config('01', '11', rhex)
    time.sleep(rtime/10)

    panel_after = getPanel()
    
    i, j = getIndex(panel_before, panel_after)
    profile = switchCase2(str(panel_after))
    
    zero = time.time()
    future = zero + profile
    time.sleep(3)
    now = time.time()
    
    while(now <= future - 1):
        p = getPotLum()
        now = time.time()
        if(p == 0):
            FILE = open('TC1_SETA1_SUB_2.txt', 'a')
            FILE.write('teste falhou. led azul nao parece estar ligado\n')
            FILE.write('{}\t'.format(p))
            FILE.write('{}\t'.format(profile))
            FILE.write('{}\t'.format(rtime))
            FILE.write('{}\t'.format(panel_before))
            FILE.write('{}\n\n'.format(panel_after))
            FILE.close()
            return False
    
    if((j - i) == 1 or (i - j) == 3):
        print("teste ok")
        print(j , i)
        return True
    else:
        FILE = open('TC1_SETA1_SUB_2.txt', 'a')
        print('falha. a ativacao de seta 1 vez nao mudou o perfil na ordem estabelecida')
        FILE.write('{}\t'.format(panel_before))
        FILE.write('{}\n'.format(panel_after))
        FILE.close()
        return False

#Subcenário 3
def testscenario3():
    rtime = random.randint(10, 30)
    rhex = hex(rtime)[2:]
    if(len(rhex) < 2):
        rhex = '0' + rhex
    
    set_config('01', '12', '0A')
    time.sleep(1)
    panel_before = getPanel()

    time.sleep(5)

    set_config('01', '11', rhex)
    time.sleep(rtime/10)
    
    buz = getBuzzer()

    if(len(buz) == 0): #mudar depois para um teste com o período correto do buzzer
        FILE = open('TC1_SETA1_SUB_3.txt', 'a')
        print('erro no teste. nao houve beep', file = FILE)
        print('{}\n'.format(rtime), file = FILE)
        return False
    else:
        vbat = getBatLvl()
        print(vbat)
        if(vbat < 3.8):
            FILE = open('TC1_SETA1_SUB_3.txt', 'a')
            print('teste falhou. perfil de cura executado alem da restricao de bateria', file = FILE)
            print('{}\n'.format(vbat), file=FILE)
            FILE.close()
            return False
        else:
            panel_after = getPanel()
            i, j = getIndex(panel_before, panel_after)
            if((j - i) == 1 or (i - j) == 3):
                print("teste ok")
                return True
            else:
                FILE = open('TC1_SETA1_SUB_3.txt', 'a')
                print('falha. a ativacao de seta 1 vez nao mudou o perfil na ordem estabelecida', file = FILE)
                print('{}\t {}'.format(panel_before, panel_after))
                return False

#CENÁRIO SETA 2
#Subcenário 1
def testscenario4():
    if(getPotLum() != 0):
        FILE = open('TC1_SETA2_SUB_1.txt', 'a')
        print('led de cura ainda esta ativado')
        FILE.write('{}\n'.format(getPotLum()))
        FILE.close()
        return False
    else:
        set_config('01', '11', '02')
        time.sleep(0.2)
        panel_before = getPanel()

        set_config('01', '12', '32')
        time.sleep(5)        

        rtime = random.randint(10, 15)
        rhex = hex(rtime)[2:]
        if(len(rhex) < 2):
            rhex = '0' + rhex
        
        set_config('01', '11', rhex)
        time.sleep(rtime/10)
        time.sleep(3)

        set_config('01', '12', '0a')
        time.sleep(2)

        set_config('01', '12', '0a')
        time.sleep(1)

        panel_after = getPanel()

        if(panel_before != panel_after):
            FILE = open('TC1_SETA2_SUB_1.txt', 'a')
            print('teste falhou. seta interfere no mosotrador de bateria')
            FILE.write('{}\t {} \t {}\n'.format(panel_before, panel_after, rtime))
            FILE.close()
            return False
        else:
            print('teste passou')
            return True

#CENÁRIO ON/OFF 1
#Subcenário 1
def testscenario5():
    if(getPotLum() != 0):
        FILE = open('TC1_ONOFF1_SUB_1.txt', 'a')
        FILE.write('{}\n'.format(getPotLum()))
        FILE.close()
        return False
    else:
        rtime = random.randint(2, 9)
        rhex = hex(rtime)[2:]
        if(len(rhex) < 2):
            rhex = '0' + rhex

        set_config('01', '12', rhex)
        time.sleep(rtime/10)
        panel = getPanel()
        panel = str(panel)
        profile = switchCase2(panel)
        if(profile == 'invalid configuration'):
            FILE = open('TC1_ONOFF1_SUB_1.txt', 'a')
            print('{}\t{}'.format(profile, rtime), file= FILE)
            FILE.close()
            return False

        curve = getCurve(profile)

        for i in range(len(curve)):
            if(curve[i][1] == 0):
                if(i < 0 and i < len(curve) - 1):
                    curve[i][1] = (curve[i-1][1] + curve[i+1][1])/2
        

        set_config('01', '11', '02')
        time.sleep(0.2)
        flag = []
        
        if(profile == 10):
            for c in curve:
                if(mask10(c[1], c[0])):
                    flag.append(1)
                else:
                    FILE = open('TC1_ONOFF1_SUB_1.txt', 'a')
                    print(c, '\t', profile, file = FILE)
                    FILE.close()
                    flag.append(0)
        elif(profile == 20):
            for c in curve:
                if(mask20(c[1], c[0])):
                    flag.append(1)
                else:
                    FILE = open('TC1_ONOFF1_SUB_1.txt', 'a')
                    print(c, '\t', profile, file = FILE)
                    FILE.close()
                    flag.append(0)
        elif(profile == 40):
            for c in curve:
                if(mask40(c[1], c[0])):
                 flag.append(1)
                else:
                    FILE = open('TC1_ONOFF1_SUB_1.txt', 'a')
                    print(c, '\t', profile, file = FILE)
                    FILE.close()
                    flag.append(0)
        else:
            for c in curve:
                if(mask60(c[1], c[0])):
                    flag.append(1)
                else:
                    FILE = open('TC1_ONOFF1_SUB_1.txt', 'a')
                    print(c, '\t', profile, file = FILE)
                    FILE.close()
                    flag.append(0)
        if(min(flag) == 1):
            return True
        else:
            return False

#Subcenário 2
def testscenario6():
    if(getPotLum() != 0):
        FILE = open('TC1_ONOFF1_SUB_2.txt', 'a')
        FILE.write('{}\n'.format(getPotLum()))
        print('led de cura ainda esta ativado')
        return False
    else:
        if(getBatLvl() < 3.8):
            rtime = random.randint(2, 14)
            rhex = hex(rtime)[2:]
            if(len(rhex) < 2):
                rhex = '0' + rhex
            set_config('01', '12', rhex)
            time.sleep(rtime/10)
            
            time.sleep(1)
            buz = getBuzzer()
            if(len(buz) == 0):
                FILE = open('TC1_ONOFF1_SUB_2.txt', 'a')
                FILE.write('{}\t{}\n'.format(buz[0], buz[1]))
                print('teste falhou. nao houve beep')
                FILE.close()
                return False
            else:
                if(getPotLum() != 0):
                    FILE = open('TC1_ONOFF1_SUB_2.txt', 'a')
                    print(getPotLum(), file = FILE)
                    FILE.close()
                    return False
                else:
                    return True
        else:
            FILE = open('TC1_ONOFF1_SUB_2.txt', 'a')
            print('Bateria está acima de VBAT_MIN', file = FILE)
            FILE.close()
            return False

#Subcenário 3
def testscenario7():
    rtime = random.randint(30, 50)
    rhex = hex(rtime)[2:]
    if(len(rhex) < 2):
        rhex = '0' + rhex

    set_config('01', '12', rhex)
    time.sleep(rtime/10)
    

    panel_before = getPanel()
    options = [[0,0,1,1], [0,0,0,1], [0,1,1,1], [1,1,1,1], [0,0,0,0]]
    if(panel_before not in options):
        FILE = open('TC1_ONOFF1_SUB_3.txt', 'a')
        print(panel_before, '\t', getBatLvl(), '\n', file = FILE)
        FILE.close()
        return False
    else:
        pass
    
    time.sleep(5)

    panel_after = getPanel()
    if(panel_after != [0,0,0,0]):
        FILE = open('TC1_ONOFF1_SUB_3.txt', 'a')
        print(panel_after, file = FILE)
        FILE.close()
        return False
    else:
        return True

#Subcenário 4
def testscenario8():
    rtime = random.randint(30, 50)
    rhex = hex(rtime)[2:]
    if(len(rhex) < 2):
        rhex = '0' + rhex

    panel_before = getPanel()
    if(panel_before != [0,0,0,0]):
        FILE = open('TC1_ONOFF1_SUB_4.txt', 'a')
        print(panel_before, file = FILE)
        FILE.close()
        return False
    else:
        set_config('01', '12', rhex)
        time.sleep(rtime/10)
        

        panel_after = getPanel()
        options = [[0,0,1,1], [0,0,0,1], [0,1,1,1], [1,1,1,1], [0,0,0,0]]
        if(panel_after not in options):
            FILE = open('TC1_ONOFF1_SUB_4.txt', 'a')
            print(panel_after, file = FILE)
            FILE.close()
            return False
        else:
            time.sleep(6)

            panel_after = getPanel()
            if(panel_after != [0,0,0,0]):
                FILE = open('TC1_ONOFF1_SUB_4.txt', 'a')
                print(panel_after, file = FILE)
                FILE.close()
                return False
            else:
                return True

#CENÁRIO ON/OFF 2
#Subcenário 1
def testscenario9():
    rtime = random.randint(2, 29)
    rhex = hex(rtime)[2:]
    if(len(rhex) < 2):
        rhex = '0' + rhex
    set_config('01', '12', '0A')
    time.sleep(1)

    if(getPotLum() == 0):
        FILE = open('TC1_ONOFF2_SUB_1.txt', 'a')
        print('{}'.format(getPotLum()))
        FILE.close()
        return False
    else:
        time.sleep(5)

        set_config('01', '12', rhex)
        time.sleep(rtime/10)

        if(getPotLum() != 0):
            print(getPotLum(), file = FILE)
            FILE.close()
            return False
        else:
            return True

#Subcenário 2
def testscenario10():
    set_config('01', '11', '02')
    time.sleep(0.2)

    profile = switchCase2(str(getPanel()))
    
    #Escolha de um momento aleatório para começar a pressionar o botão ON/OFF
    press = random.randint(2, profile)
        
    #Escolha do momento de soltar o botão ON/OFF
    release = profile - press + random.randint(1, 2)
    rhex = hex(release*10)[2:]
    if(len(rhex)%2 != 0):
        rhex = '0' + rhex
    
    set_config('01', '12', '02')
    time.sleep(0.2)
    time.sleep(press)
    set_config('01', '12', rhex)
    time.sleep(release)
    
    set_config('01', '12', '02')
    time.sleep(0.2)
    time.sleep(5)
    if(getPotLum() == 0):
        FILE = open('TC1_ONOFF2_SUB_2.txt', 'a')
        print('{}\t{}\t{}'.format(profile, press, release))
        FILE.close()
        return False
    else:
        return True

#Subcenário 3
def testscenario11():
    rtime = random.randint(30, 60)
    rhex = hex(rtime)[2:]
    if(len(rhex) < 2):
        rhex = '0' + rhex
    set_config('01', '12', rhex)
    time.sleep(rtime/10)

    panel_before = getPanel()

    time.sleep(5)
    
    panel_after = getPanel()

    possibilities = [[1,1,1,1], [0,1,1,1], [0,0,1,1], [0,0,0,1]]
    if(panel_before not in possibilities):
        FILE = open('TC1_ONOFF2_SUB_3.txt', 'a')
        print('{}\t{}\t{}'.format(rtime, panel_before, panel_after), file = FILE)
        FILE.close()
        return False
    else:
        return True

    if(panel_after in possibilities):
        FILE = open('TC1_ONOFF2_SUB_3.txt', 'a')
        print('{}\t{}\t{}'.format(rtime, panel_before, panel_after), file = FILE)
        FILE.close()
        return False
    else:
        return True

#Subcenário 4 
def testscenario12():
    rtime = random.randint(30, 60)
    rhex = hex(rtime)[2:]
    if(len(rhex) < 2):
        rhex = '0' + rhex

    panel_before = getPanel()

    set_config('01', '12', rhex)
    time.sleep(rtime/10)

    time.sleep(5)
    
    panel_after = getPanel()

    if(panel_before != [0,0,0,0]):
        FILE = open('TC1_ONOFF2_SUB_4.txt', 'a')
        print('{}\t{}\t{}'.format(rtime, panel_before, panel_after), file = FILE)
        FILE.close()
        return False
    else:
        pass

    if(panel_after != [0,0,0,0]):
        FILE = open('TC1_ONOFF2_SUB_4.txt', 'a')
        print('{}\t{}\t{}'.format(rtime, panel_before, panel_after), file = FILE)
        FILE.close()
        return False
    else:
        return True

def main():
    # tests = [testscenario1, testscenario2, testscenario3, testscenario4, testscenario5, testscenario6,\
    #         testscenario7, testscenario8, testscenario9, testscenario10, testscenario11, testscenario12]
    cont = 0
    initialTime = time.time()
    for i in range(50):
            print("Round ", i)
            
            aux = testscenario5() ##Cenário quatro precisa da bateria a 3.8 ou abaixo
        
            if(aux):
                cont = cont + 1
            
            time.sleep(1)

    
    
    print("Successful tests percentage: ", (cont/50)*100)

    print("Unsuccessful tests percentage: ", ((50 - cont)/50) * 100)

    print("Elapsed time: ", time.time() - initialTime)


    with open('output_TC1s.txt', 'a') as f:
            print("Scene Four:")

            print("Successful tests percentage: ", (cont/50)*100, file=f)

            print("Unsuccessful tests percentage: ", ((50 - cont)/50) * 100, file=f)

            print("Elapsed time: ", time.time() - initialTime, file = f)

            print("############# END ###########\n\n", file=f)
    
    f.close()

if __name__ == "__main__":
  main()