import keyboard
import time
import playsound
import json
import datetime

blEndOfExecutionKeyPressed = False
blPushToTalkKeyPressed = False

strEOEkey = 'ctrl + 0'
strMuteUnmuteKeys = 'ctrl + d'
configs_json_file = "configs_file.json"#por que criar uma variável pra representar um arquivo só pra complicar a compreenção do código? POR QUE SIM! (na verdade ajuda se quiser trocar o path do arquivo, seu nome, etc. mas pra um programa pequeno como esse realmente é desnecessário)
press_play_sound_mp3_file = "press_playsound.mp3"
unpress_play_sound_mp3_file = "unpress_playsound.mp3"
#NOTA: quase todos os time.sleep() são puramente para otimização, já que menos instruções e checks serão executadas em uma dada quantidade de tempo

def serialize(dictionary,file_name):
    try:
        with open(file_name,"w") as file_writer:
            json.dump(dictionary,file_writer,indent=4)
    except:
        print('erro na serialização')
def deserialize(self_dictionary,file_name):
    try:
        with open(file_name,"r") as file:
            return json.load(file)
    except:
        print('erro na deserialização')
        return self_dictionary#sim, essa função só usa o self_dictionary pra retornar em caso de erro, assim o programa pode continuar

configs = {#configs pradões
    "strPushToTalkKey":"*",
    "blPlaySounds": True
}
print('carregando configurações salvas no arquivo ', configs_json_file)
configs = deserialize(configs, configs_json_file)#configs salvas no arquivo json
strPTTkey = configs["strPushToTalkKey"]
blPlaySounds = configs["blPlaySounds"]#uso desnecessário de variáveis, sim, mas eu to com preguiça de mudar isso :/, sem falar que n usando essas variáveis, eu podia transformas as mudanças de confuguração abaixo em uma função, pra ser mais organizado.

print('configurações atuais:')
print('Som:',end=' ')
if blPlaySounds: 
    print('ativado') 
else: 
    print('desativado')
print('Tecla Push To Talk: "',strPTTkey,'"')
print('Mudar configurações? ("s" para sim)')
if input() == 's':
    #start of configurations
    #mudar tecla pushtotalk
    print('Mudar a tecla de Push To Talk? "s" para sim. ')
    if (input() == 's'):
        time.sleep(0.4)
        while True:
            print('Pressione a tecla desejada (ESC para cancelar)')
            while True:
                time.sleep(0.01)
                newPTTkey = keyboard.get_hotkey_name()
                if newPTTkey != '':
                    break
            if newPTTkey == 'esc':
                print('cancelando...')
            else:
                print('tem certeza que quer trocar "',strPTTkey,'" por "',newPTTkey,'"? "s" para sim.')
                time.sleep(0.5) 
                if input() == 's':
                    strPTTkey = newPTTkey
                    #serialização
                    configs["PushToTalkKey"] = strPTTkey
                    serialize(configs,"configs_file.json")
                    break
                else:
                    strAnswer = input('tentar novamente?')
                    if strAnswer != 's':
                        break


    print('Mudar ativação de som?')
    if blPlaySounds: 
        print('ativado',end='') 
    else: 
        print('desativado',end='') 
    print(') "s" para sim')      
    if input() == 's':
        print('O som agora está:',end=' ')
        if blPlaySounds:#troca de valores
            blPlaySounds = False
            print('desativado.')
        else:
            blPlaySounds = True
            print('ativado.')
        configs["blPlaySounds"] = blPlaySounds
        serialize(configs, configs_json_file)
    #end of configurations       

input('Esperando por um ENTER...')
#aqui abaixo é onde o código que importa acontece
while blEndOfExecutionKeyPressed == False:
    time.sleep(0.01)#otimização
    isPTTkeyPressed = keyboard.is_pressed(strPTTkey)
    if keyboard.is_pressed(strPTTkey) == True and blPushToTalkKeyPressed == False:
        keyboard.press_and_release(strMuteUnmuteKeys)
        blPushToTalkKeyPressed = True
        print(datetime.datetime.now(),'MicOpen')
        if blPlaySounds:
            try:
                playsound.playsound(press_play_sound_mp3_file,block=False)
            except:
                print('erro: arquivo',press_play_sound_mp3_file,'não encontrado.')
        time.sleep(0.1)
    if blPushToTalkKeyPressed == True and keyboard.is_pressed(strPTTkey) == False: 
        keyboard.press_and_release(strMuteUnmuteKeys)
        blPushToTalkKeyPressed = False
        print(datetime.datetime.now(),'MicClosed')
        if blPlaySounds:
            try:
                playsound.playsound(unpress_play_sound_mp3_file,block=False)
            except:
                print('erro: arquivo',unpress_play_sound_mp3_file,'não encontrado.')
        time.sleep(0.1)
    if keyboard.is_pressed(strEOEkey):
        blEndOfExecutionKeyPressed = True
