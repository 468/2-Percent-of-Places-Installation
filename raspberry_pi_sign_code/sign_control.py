import bluetooth
import sign

hostMACAddress = 'mac_address_here' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3
backlog = 1
size = 1024
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server.bind((hostMACAddress, port))
server.listen(backlog)
s_display = sign.Sign()

display_activated = False

try:
    client, clientInfo = server.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            if display_activated:
			    s_display.stop()
            s_display.scrollPut(data + "     ")
            s_display.scroll()
            client.send(data) # Echo back to client
            display_activated = True
except:	
    print("Client disconnected?")
    client.close()
    server.close()
