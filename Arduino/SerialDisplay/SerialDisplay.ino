/*
Code to dispay text sent over serial from other devices,
compatable with the 16x2 lcd keypad shield. Code was based on
the SerialDisplay example sketch found in the LiquidCrystal 
Library, and was expanded on by Mahmnood Gladney.

Note: sending somthing over serial will clear the whole string,
if you want to write just to the top row, begin the message with
'&'. If you want to do the same for the bottom row, use a '*'

Pressing the right button on the shield will send the number 45 
over serial, pressing the up button will send the number 99.
*/

// include the library code:
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 8, en = 9, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // initialize the serial communications:
  Serial.begin(2000000);
}

void loop() {
  // when characters arrive over the serial port...
  int x;
  x = analogRead(0);
  if (x < 60){
    Serial.write("45");
    delay(200);
    }
  else if (x < 200) {
    Serial.write("99");
    delay(200);
 }
  if (Serial.available()) {
    // wait a bit for the entire message to arrive
    delay(100);
    // read all the available characters
    char temp = Serial.read();
    if (temp == '*'){
       lcd.setCursor(0,1);
       }
    else if (temp == '&'){
      lcd.setCursor(0,0);
      }
    else {
      lcd.clear();
      lcd.write(temp);
      }
    while (Serial.available() > 0) {
      // display each character to the LCD
      lcd.write(Serial.read());
    }
  }
}
