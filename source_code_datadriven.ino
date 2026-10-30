const uint8_t  PWM_PIN      = 5;
const uint8_t  IN1_PIN      = 7;
const uint8_t  IN2_PIN      = 8;
const uint8_t  ENCODER_PIN  = 2;

const unsigned long Ts_ms   = 50;
const uint8_t  DUTY_MIN_PCT = 30;
const uint8_t  DUTY_MAX_PCT = 80;
const int      N_SAMPLES    = 400;

const float    COUNTS_PER_REV = 374.0;

volatile long encoderCount = 0;
long lastEncoderCount = 0;

unsigned long lastSampleTime = 0;
int sampleIndex = 0;

uint16_t lfsr = 0xACE1u;

bool prbsBit() {
  uint16_t bit = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5)) & 1u;
  lfsr = (lfsr >> 1) | (bit << 15);
  return bit;
}

void encoderISR() {
  encoderCount++;
}

void setup() {
  Serial.begin(115200);

  pinMode(PWM_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(ENCODER_PIN, INPUT_PULLUP);

  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);

  attachInterrupt(digitalPinToInterrupt(ENCODER_PIN), encoderISR, RISING);

  Serial.println("t_ms,u_duty,y_speed");

  lastSampleTime = millis();
}

void loop() {
  unsigned long now = millis();

  if (now - lastSampleTime >= Ts_ms && sampleIndex < N_SAMPLES) {
    lastSampleTime = now;

    uint8_t dutyPct = prbsBit() ? DUTY_MAX_PCT : DUTY_MIN_PCT;
    int pwmValue = map(dutyPct, 0, 100, 0, 255);
    analogWrite(PWM_PIN, pwmValue);

    noInterrupts();
    long countsNow = encoderCount;
    interrupts();

    long deltaCounts = countsNow - lastEncoderCount;
    lastEncoderCount = countsNow;

    float speed_rps = (deltaCounts / COUNTS_PER_REV) / (Ts_ms / 1000.0);

    Serial.print(now);
    Serial.print(",");
    Serial.print(dutyPct);
    Serial.print(",");
    Serial.println(speed_rps, 4);

    sampleIndex++;
  }

  if (sampleIndex >= N_SAMPLES) {
    analogWrite(PWM_PIN, 0);
  }
}