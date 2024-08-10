#include <Servo.h>
int redLED = 13;
int greenLED = 12;
Servo myServo;  // Create a Servo object
int servoPin = 8;  // Pin where the servo is connected

void setup() {
  Serial.begin(9600);  // Start the serial communication
  myServo.attach(servoPin);  // Attach the servo to the pin
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {  // Check if data is available
    String command = Serial.readStringUntil('\n');  // Read the command
    command.trim();  // Remove any whitespace

    if (command.equalsIgnoreCase("Authorized")) {
      myServo.write(180);  // Move servo to 90 degrees
      digitalWrite(greenLED, HIGH);
      digitalWrite(redLED, LOW);
    }
    else if (command.equalsIgnoreCase("Background")) {
      myServo.write(90);  // Move servo to 180 degrees
      digitalWrite(greenLED, LOW);
      digitalWrite(redLED, LOW);
    }
    else if (command.equalsIgnoreCase("Unauthorized")) {
      digitalWrite(greenLED, LOW);
      digitalWrite(redLED, HIGH);
      myServo.write(90);  // Move servo to 180 degrees
    }
  }
}
