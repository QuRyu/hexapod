#include <avr/io.h>
#include "USART.h" 

#define SPEED 200 // the speed of motors 
                  // changet this to adjust motor speed 

char msg[50]; // buffer for printString

typedef enum _State {
  BACK, MIDDLE, FRONT
} State; 

State state = BACK; 

uint8_t interval_time() {
  // assuming prescaler is 1024 and OCR2A = 0xFF
  
}

const int COUNTER_UP = 20; // the total state for one state 
                           // change this to adjust phase transition time 
int counter = 0; 

void set_state(State s) { 
  switch(s) {
    case BACK: 
      OCR0A = SPEED; 
      OCR0B = 0; 
      OCR1A = 0;
      state = BACK; 
      break;
    case MIDDLE: 
      OCR0B = SPEED;
      OCR0A = 0; 
      OCR1A = 0; 
      state = MIDDLE; 
      break; 
    case FRONT: 
      OCR1A = SPEED; 
      OCR0A = 0; 
      OCR0B = 0; 
      state = FRONT; 
      break;
  }
}

ISR(TIMER2_COMPA_vect) { 
  if (counter++ >= COUNTER_UP) {
  printString("switch state");
  switch(state) { 
    case BACK: 
      set_state(MIDDLE); 
      break; 
    case MIDDLE:
      set_state(FRONT); 
      break; 
    case FRONT: 
      set_state(BACK);
      break; 
  }
  counter = 0; 
  }
}

void setup() {
  // motor setup 
  DDRD = 0xE0;
  DDRB = 0x2;
//  PORTD = 0x40; 
  
  
  TCCR0A = 0xA3; // fast PWM, non-inverting mode for COMA and COMB
  TCCR0B = 0x5; // prescaler 1024
  OCR0A = 0;
  OCR0B = 0;
//  TIMSK0 = 0x6; // enable both OCMA and OCMB interrupts

  TCCR1A = 0x81; // fast PWM, non-inverting mode for COMA 
  TCCR1B = 0xD; // prescaler 1024
  OCR1A = 0; 

  TCCR2A = 0x82; // CTC mode 
  TCCR2B = 0x7; // prescaler 1024
  OCR2A = 0xFF;
  TIMSK2 = 0x2; // enable interrupt for COMPA
  
  SREG |= 0x80; // turn on global interrupt

  set_state(BACK);
}

int main() {
  init(); 
  initUSART();
  setup();
  
  while (true) {
      printString("");
  }
}
