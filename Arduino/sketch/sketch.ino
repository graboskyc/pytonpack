#include <Adafruit_NeoPixel.h>

#define PIN 1
#define PIXELS 28
#define PIXELSPER 7
#define DISKS 4

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(PIXELS, PIN, NEO_GRB + NEO_KHZ800);

void allOff() {
  for(int i=0;i<PIXELS;i++) {
    pixels.setPixelColor(i,0);
  }
  
  pixels.show();

}

void allOn(int disk) {
  int state = digitalRead(0);
  if(state == HIGH) 
  {
    for(int i=0;i<PIXELSPER;i++) {
      pixels.setPixelColor(i+(disk*PIXELSPER),pixels.Color(255,0,0));
    }
  }
  else {
    allOff();
  }
  
  pixels.show();

}

void setup() {
  // put your setup code here, to run once:
  pixels.begin();
  pinMode(0,INPUT); 
  allOff();
}

void loop() {
  // put your main code here, to run repeatedly:
  
    for(int i=0;i<DISKS;i++) {
      allOff();
      allOn(i);
      delay(1000);
    }
}
