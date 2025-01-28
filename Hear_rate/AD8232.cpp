const int ecgPin = A0;

void setup() {
  Serial.begin(9600);
  pinMode(ecgPin, INPUT);
}

void loop() {
  int ecgValue = analogRead(ecgPin);  // Leer valor analógico del sensor
  Serial.println(ecgValue);           // Enviar valor al computador
  delay(10);                          // Ajusta según necesites
}
