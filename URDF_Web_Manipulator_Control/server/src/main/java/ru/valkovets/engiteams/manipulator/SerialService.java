package ru.valkovets.engiteams.manipulator;

import com.fazecast.jSerialComm.SerialPort;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class SerialService {
@Value("${serial.port:COM3}")
private String portDescriptor;

@Value("${serial.rate:115200}")
private int baudRate;

private SerialPort serialPort;


@PostConstruct
public void initPort() {
  serialPort = SerialPort.getCommPort(portDescriptor);
  serialPort.setComPortTimeouts(SerialPort.TIMEOUT_NONBLOCKING, 100, 0);
  serialPort.setBaudRate(baudRate);
  serialPort.setParity(SerialPort.NO_PARITY);
  serialPort.setNumStopBits(SerialPort.ONE_STOP_BIT);
  serialPort.setNumDataBits(8);
  serialPort.openPort();
}

public void closePort() {
  serialPort.closePort();
}

public boolean write(final String s) {
  final byte[] bytes = s.getBytes();
  return serialPort.writeBytes(bytes, bytes.length) == bytes.length;
}

public int clearReadBuffer() {
  final int bytesToRead = serialPort.bytesAvailable();
  final byte[] bytes = new byte[bytesToRead];
  serialPort.readBytes(bytes, bytes.length);
  return bytesToRead;
}
}
