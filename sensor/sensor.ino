#include <avr/io.h>
#include "USART.h" 

#define N 5

#define ADMUX_X 0x42
#define ADMUX_Y 0x41 
#define ADMUX_Z 0x40

#define X_AXIS 0 
#define Y_AXIS 1 
#define Z_AXIS 2 

#define COUNT 1250

// ADC values
uint8_t admuxes[3] = {ADMUX_X, ADMUX_Y, ADMUX_Z};
float mean[3] = {0, 0, 0}; // ADC mean for x, y, z axis 
uint16_t adc_value = 0; // ADC value read each time 
int adc_idx = 0; 
int counter = 0; 

char msg[50]; // buffer for printString


// ADC interrupts, read ADC value and update the mean 
ISR(ADC_vect) { 
  if (counter++ > COUNT) {
    adc_value = ADCL; 
    adc_value |= (ADCH & 0x3) << 8; 

    mean[adc_idx] = mean[adc_idx] * float(N-1)/float(N) + float(adc_value) / float(N);
    adc_idx++;

    // one round of sampling is finished 
    // start to wait for the next round 
    if (adc_idx == 3) {
      adc_idx = 0; 
      counter = 0; 
    }

    ADMUX = admuxes[adc_idx];
  }

  
//  sprintf(msg, "ADC value %d\n", int(mean)); 
//  printString(msg);

}

void setup() {
//  TCCR0A = 0x2; 
//  TCCR0B = 0x5; 
//  OCR0A = 233;
//  TIMSK0 = 0x2;

  // sensor config 
  ADMUX = admuxes[adc_idx]; // first read ADC 0
  ADCSRA = 0xEF; // prescaler 128, ADC enabled, interrupt enabled 
  ADCSRB = 0x0; // free running mode 
//  DIDR0 = 0x3F;  

  SREG |= 0x80; // turn on global interrupt
}

int main() {
  init(); 
  initUSART();
  setup();

//  sprintf(msg, "ADCSRA %d\n", ADCSRA);
//  printString(msg);
//  ADCSRA |= 0xFF;
  
  while (true) {
    printString(""); 

    sprintf(msg, "x %d, y %d, z %d\n", (int)mean[X_AXIS], (int)mean[Y_AXIS], (int)mean[Z_AXIS]);
    printString(msg); 
  }
}
