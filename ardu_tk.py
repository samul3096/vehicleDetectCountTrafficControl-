import serial

ard_srl=serial.Serial('com6',9600)
print ard_srl.readline()
print ("Enter 1 to ON and 0 to OFF")

while 1:
    in_data=raw_input()
    print "you entered", in_data

    if(in_data=='1'):
        ard_srl.write('1')
        print ("LED ON")

    if (in_data == '0'):
        ard_srl.write('0')
        print ("LED OFF")
