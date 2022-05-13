import serial
with serial.Serial('COM12') as S:
    with open('train_data.txt', 'w') as F:
        while True:
            line = S.readline()
            line = line.rstrip().decode('utf-8')
            print(line)
            F.write((line) + '\n')
