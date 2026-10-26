// ===== BLDC LAB MODE =====

#define PWM_PIN 9
#define EN_PIN 8
#define BRK_PIN 7
#define FR_PIN 6

#define HALL1 2
#define PULSES_PER_REV 4

// ===== HALL =====
volatile unsigned long lastPulseTime = 0;
volatile unsigned long pulseInterval = 0;

void hallISR() {
  unsigned long now = micros();
  pulseInterval = now - lastPulseTime;
  lastPulseTime = now;
}

// ===== RPM =====
float rpm_meas = 0;
float rpm = 0;
float rpm_model = 0;

// ===== STEROWANIE =====w n
int pwmOut = 0;
int pwmTarget = 0;

float rpmTarget = 0;
bool closedLoop = false;

// regulator
float Kp = 0.02; //regulacja natychmiastowa
float Ki = 0.05; //kontrola w czasie
float integral = 0;

// ===== CZAS =====
unsigned long lastTime = 0;
unsigned long startTime = 0;

// ===== TRYB LAB =====
bool labMode = false;
int testPWM = 0;
unsigned long labTimer = 0;

#define PWM_STEP 10
#define SETTLE_TIME 3000   // ms

// ===== SETUP =====
void setup() {
  Serial.begin(115200);

  pinMode(PWM_PIN, OUTPUT);
  pinMode(EN_PIN, OUTPUT);
  pinMode(BRK_PIN, OUTPUT);
  pinMode(FR_PIN, OUTPUT);

  pinMode(HALL1, INPUT_PULLUP);

  digitalWrite(EN_PIN, LOW);
  digitalWrite(BRK_PIN, HIGH);
  digitalWrite(FR_PIN, LOW);

  
  attachInterrupt(digitalPinToInterrupt(HALL1), hallISR, RISING);

  lastTime = micros();
  startTime = millis();

  Serial.println("=== BLDC LAB READY ===");
  Serial.println("LAB -> auto charakterystyka");
  Serial.println("Pxxx -> PWM");
  Serial.println("Rxxx -> CL RPM");
  Serial.println("Time,Kff,Kp,Ki,RPM Hall,PWM,Target");
}

// ===== LOOP =====
void loop() {

  // ===== dt =====
  unsigned long now = micros();
  float dt = (now - lastTime) * 1e-6;
  lastTime = now;

  // ===== RPM =====
  unsigned long timeSincePulse = micros() - lastPulseTime;

  if (pulseInterval > 0 && timeSincePulse < 200000) {

    float freq = 1000000.0 / pulseInterval;
    rpm_meas = (freq * 60.0) / PULSES_PER_REV;

  }
  else {
    rpm_meas = 0;
  }

  //RPM value
  rpm = rpm_meas;

  // ===== LAB MODE =====
  if (labMode) {

    if (millis() - labTimer > SETTLE_TIME) {

      // zapis punktu
      Serial.print("DATA,");
      Serial.print(testPWM);
      Serial.print(",");
      Serial.println(rpm);

      testPWM += PWM_STEP;

      if (testPWM > 200) {
        labMode = false;
        pwmTarget = 0;
        Serial.println("LAB DONE");
        return;
      }

      pwmTarget = testPWM;
      labTimer = millis();
    }
  }

  // ===== CL REGULATOR =====
  static unsigned long lastControlTime = 0;

  if (closedLoop && rpmTarget > 0 &&
    millis() - lastControlTime >= 20) {

    lastControlTime = millis();

    // uchyb prędkości
    float error = rpmTarget - rpm;

    // wstępne wyliczenie sterowania
    float control = Kp * error + Ki * integral;

    // człon całkujący
    // całkuj tylko wtedy, gdy wyjście nie jest nasycone
    // albo błąd działa w kierunku wyjścia z nasycenia
    if (!((control >= 255 && error > 0) ||
          (control <= 0 && error < 0))) {

      integral += error * 0.02;
    }

    integral = constrain(integral, -5000, 5000);

    // ponowne wyliczenie sterowania
    control = Kp * error + Ki * integral;

    // ograniczenie PWM
    pwmTarget = constrain((int)control, 0, 255);
  }
  
  // ===== SOFT START =====
  if (pwmOut < pwmTarget) {
    pwmOut += 2;
    if (pwmOut > pwmTarget) pwmOut = pwmTarget;
  }

  if (pwmOut > pwmTarget) {
    pwmOut -= 2;
    if (pwmOut < pwmTarget) pwmOut = pwmTarget;
  }

  analogWrite(PWM_PIN, pwmOut);

  // ===== SERIAL =====
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "LAB") {
      labMode = true;
      closedLoop = false;

      testPWM = 20;
      pwmTarget = testPWM;
      labTimer = millis();

      Serial.println("START LAB");
    }
    else if (cmd.startsWith("P")) {
      pwmTarget = cmd.substring(1).toInt();
      closedLoop = false;
    }
    else if (cmd.startsWith("R")) {
      rpmTarget = cmd.substring(1).toFloat();

      if (rpmTarget <= 0) {
        rpmTarget = 0;
        closedLoop = false;
        integral = 0;
        pwmTarget = 0;
      }
      else {
        integral = 0;
        closedLoop = true;
      }
    }
  
  // ===== DEBUG =====
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint > 300) {

    Serial.print(rpm_meas);
    Serial.print(",");
    Serial.println(pwmOut);

    lastPrint = millis();
    }
  }
}