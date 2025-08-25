#define fsrpin A0
int fsrreading;

void setup() {
  Serial.begin(9600);
}

void loop() {
  fsrreading = analogRead(fsrpin);
  Serial.print("Analog reading = ");
  Serial.print(fsrreading);

  if (fsrreading < 10) {
    Serial.println(" - No pressure");
  } else if (fsrreading < 200) {
    Serial.println(" - Light touch");
  } else if (fsrreading < 500) {
    Serial.println(" - Light squeeze");
  } else if (fsrreading < 800) {
    Serial.println(" - Medium squeeze");
  } else {
    Serial.println(" - Big squeeze");
  }

  delay(1000);
}
