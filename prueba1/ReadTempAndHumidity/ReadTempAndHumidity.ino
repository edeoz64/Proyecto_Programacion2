#include <DHT11.h>
#include <Arduino.h>

DHT11 dht11(5);
#define PIN_LUD 2
#define PIN_MOT 4
#define PIN_BOC 23

int value_led1=0;
int value_led2=0;
int value_bocina=0;
//String cad, cad1, cad2, cad3;
//int vled = 0, vmot = 0, vboc = 0, pos;

void fnActuadores(String cad){
  int pos;
  String label, value;
  cad.trim();
  cad.toLowerCase();
  pos = cad.indexOf(':');
  label = cad.substring(0,pos);
  value = cad.substring(pos+1);

  Serial.println(cad);

  if(label.equals("led1")){
    if(value_led1 != value.toInt()){
      value_led1 = value.toInt();
      digitalWrite(PIN_LUD,value_led1);
    }
  }
  if(label.equals("led2")){
    if(value_led2 != value.toInt()){
      value_led2 = value.toInt();
      digitalWrite(PIN_MOT,value_led2);
    }
  }
  if(label.equals("bocina")){
    if(value_bocina != value.toInt()){
      value_bocina = value.toInt();
      digitalWrite(PIN_BOC,value_bocina);
    }
  }

}
void setup()
{
    Serial.begin(115200);
    delay(30);
    pinMode(PIN_LUD, OUTPUT);
    pinMode(PIN_BOC, OUTPUT);
    pinMode(PIN_MOT, OUTPUT);
    digitalWrite(PIN_LUD, value_led1);
    digitalWrite(PIN_MOT, value_led2);
    digitalWrite(PIN_BOC, value_bocina);
}

void loop()
{
    if (Serial.available()) {
      fnActuadores(Serial.readString());
    }
    delay(4000);

    float t = dht11.readTemperature();
    int h = dht11.readHumidity();
    if (t != DHT11::ERROR_CHECKSUM && t != DHT11::ERROR_TIMEOUT &&
        h != DHT11::ERROR_CHECKSUM && h != DHT11::ERROR_TIMEOUT)
    delay(1000);
    //Serial.print(F("Humedad: "));
    Serial.println(String(h) + "," + String(t,1));
    //Serial.print(F("%  Temperatura: "));
    //Serial.println(t);
    //Serial.println(F("°C "));
}
