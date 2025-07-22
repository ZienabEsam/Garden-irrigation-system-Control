char btInput;
int relayPin = 8;

void setup() {
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW); // start with valve OFF
  Serial.begin(9600); // for HC-05
}

void loop() {
  if (Serial.available()) {
    btInput = Serial.read();
    
    if (btInput == '1') {
      digitalWrite(relayPin, HIGH); // Valve ON
      Serial.println("Valve is ON");
    }
    else if (btInput == '0') {
      digitalWrite(relayPin, LOW); // Valve OFF
      Serial.println("Valve is OFF");
    }
  }
}

