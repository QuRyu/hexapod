#include <avr/io.h>
#include "USART.h"

char msg[50]; 

int position = 0;
boolean direction = false; 
unsigned long time = 0; 
unsigned int dTime; 
int rpm;
const int spokes = 2;

bool triggered = false; 

ISR(INT1_vect) {
  
  triggered != triggered; 
  //millis() returns the time in milliseconds since the board was turned on
  dTime = millis()-time;
  time = time + dTime;
  //use the time calculation and the number of spokes to calculate the rpm of the motor
  rpm = 1/spokes * 1/dTime * 1000 * 60;
}


//Direction and Speed Detection
void setup() { 
  EICRA = 0xC; // falling edge for INT1 
  EIMSK = 0x2; // enable interrupt 1
  
}

// The main program loop that runs while the board is active
// This loop flashes the pin 13 led at 1Hz, each delay is 500ms 
int main() {
  initUSART();
  setup();
  
  while(true) {
    printString("");

    sprintf(msg, "rmp %d, triggered %d\n", rpm, triggered);
    printString(msg);
  }
}
