#include <FlexiTimer2.h>

//serial receive
#include <SoftwareSerial.h>
SoftwareSerial mySerial(10, 11); // RX, TX
String data;

//nixie
#define SRCLK_A 2//shift register clock D2
#define SER_A 4//serial input D4
#define RCLK_A 3//storage register clock D3

#define SRCLK_C 7 //shift register clock D7
#define SER_C 5//serial input D5
#define RCLK_C 6//storage register clock D6

// 2^x slaveのQhを下位ビットとして出力するため、指定した数+1が表示される
int time[8] = {0, 1, 2, 8, 9, 10, 11, 12};
int time_m = 0;

void serial_receive(){
  //serial receive
  
  
  if (Serial.available() > 0){
    data = Serial.readStringUntil('\n');

    // 受信した文字列をintに変換
    for(int i = 0; i < 8; i++){

      if(isDigit(data[i])){
        if (data[i] == '0'){
          time[i] = 9;
        }
        else{
          time[i] = int(data[i] - '1');
        }
      }
      else if(data[i] == 'L'){
        time[i] = 10;
      }
      else if(data[i] == 'R'){
        time[i] = 11;      
      }
      else if(data[i] == 'N'){
        time[i] = 12;
      }
    }
  }

  
  for(int i = 0; i < 8; i++){
    Serial.print(time[i]);
    Serial.print(",");
  }
  Serial.println("");
  
    
}

void setup()
{
  //serial receive
  Serial.begin(57600); //hardware serial
    

  //mySerial.begin(57600); //57600 software serial

  //timer
  //FlexiTimer2::set(500, serial_receive); // msec
  //FlexiTimer2::start();
  
  //shift register anode
  pinMode(SRCLK_A, OUTPUT);
  pinMode(SER_A, OUTPUT);
  pinMode(RCLK_A, OUTPUT);

  digitalWrite(SER_A, LOW);
  digitalWrite(SRCLK_A, LOW);
  digitalWrite(RCLK_A,  LOW);

  //shift register cathode
  pinMode(SRCLK_C, OUTPUT);
  pinMode(SER_C, OUTPUT);
  pinMode(RCLK_C, OUTPUT);

  digitalWrite(SER_C, LOW);
  digitalWrite(SRCLK_C, LOW);
  digitalWrite(RCLK_C,  LOW);
}

void loop()
{
  /*
  time_m = millis();
  Serial.print("loop_start:");
  Serial.println(time_m);
  */
  
  serial_receive();
  
  for(int j = 0; j < 8; j++){    
    //カソード、数字指定
    digitalWrite(RCLK_C, LOW);
    shiftOut(SER_C, SRCLK_C, LSBFIRST, round(pow(2,time[j])));//下位8bit
    shiftOut(SER_C, SRCLK_C, LSBFIRST, round(pow(2,time[j])) >> 8);//上位8bit
    digitalWrite(RCLK_C, HIGH);
    
    //アノード、点灯管指定
    digitalWrite(RCLK_A, LOW);
    shiftOut(SER_A, SRCLK_A, LSBFIRST, 1<<(7-j));
    digitalWrite(RCLK_A, HIGH);

    //delay(1);//点灯時間
    delay(1);

    //アノード、消灯
    digitalWrite(RCLK_A, LOW);
    shiftOut(SER_A, SRCLK_A, LSBFIRST, 0);
    digitalWrite(RCLK_A, HIGH);

    //カソード、リセット
    digitalWrite(RCLK_C, LOW);
    shiftOut(SER_C, SRCLK_C, LSBFIRST, 0);
    shiftOut(SER_C, SRCLK_C, LSBFIRST, 0);
    digitalWrite(RCLK_C, HIGH);

    delayMicroseconds(300);//ブランク 100~250程度だと、レジスタのQhに接続した管（0）のゴーストが現れる。
  }
 
  //delay(1);
}
