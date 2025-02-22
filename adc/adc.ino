void setup() {
  Serial.begin(128000);
}

void loop() {
  int analogValue = analogRead(A0);
  Serial.println(analogValue);
}