package ru.valkovets.engiteams.manipulator;

import lombok.RequiredArgsConstructor;
import lombok.Synchronized;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@EnableScheduling
public class ManipulatorService {
private final SerialService serialService;
private final float[] state = new float[7];

@Synchronized
public String setState(final int index, final float angle) {
  if (index < 0 || index >= 7) return null;

  if (index <= 5) {
    if (angle > Math.PI || angle < -Math.PI) return null;
    state[index] = (float) (angle * 180 / Math.PI);
  } else {
    if (angle > 0.037 || angle < 0) return null;
    state[index] = (float) ((angle / 0.0125) * 180 / Math.PI);
  }

  return getState();
}

public String getState() {
  return state[0] + " " + state[1] + " " + state[2] + " " +
         state[3] + " " + state[4] + " " + state[5] + " " +
         state[6];
}

@Scheduled(fixedDelay = 150)
private void sendState() {
  if (serialService.clearReadBuffer() != 1) return;

  final String stateBuf = getState();
  System.out.println("state=" + (serialService.write(stateBuf) ? stateBuf : "null"));
}

public String stop() {
  return serialService.write("STOP") ? "STOP" : null;
}
}
