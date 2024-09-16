package ru.valkovets.engiteams.manipulator;

public enum Direction {
  STOP,
  FORWARD_CLOCKWISE,
  BACKWARD_COUNTERCLOCKWISE;

private static final Direction[] VALUES = values();
public static Direction valueOf(final int ordinal) {
  if (ordinal < 0 || ordinal >= VALUES.length) return null;
  return VALUES[ordinal];
}
}
