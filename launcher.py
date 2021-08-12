import subprocess

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, s - запустить сервер, c - закрыть все окна')

    if ACTION == 'q':
        # while PROCESS:
        #     VICTIM = PROCESS.pop()
        #     VICTIM.kill()
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python server.py -p 8088 -a 192.168.3.8', \
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))

        for i in range(3):
            PROCESS.append(subprocess.Popen('python client.py -a 192.168.3.8 -p 8088', \
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'c':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
