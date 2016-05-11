/* Serial device defines for dxl bus */
#define DXL_BUS_SERIAL1 1  //Dynamixel on Serial1(USART1)  <-OpenCM9.04
/* Dynamixel ID defines */
#define cam 99
#define rw 100
#define lw 101
#define shot 102
 
Dynamixel Dxl(DXL_BUS_SERIAL1); 
 
int speed = 150;
int timeout = 2000; //in units of ms
int timestamp = 0;

void setup() {
  // Initialize the dynamixel bus:
  // Dynamixel 2.0 Baudrate -> 0: 9600, 1: 57600, 2: 115200, 3: 1Mbps  
  Dxl.begin(3);
  Dxl.setPacketType(DXL_PACKET_TYPE2);
  delay(1000);
 
  Dxl.wheelMode(lw); //jointMode() is to use position mode
  Dxl.wheelMode(rw); //jointMode() is to use position mode 
  delay(500);
  
  Dxl.wheelMode(rw);   //FW- 0x400, BW-
  Dxl.wheelMode(lw);   //FW-      , BW-0x400 
  Dxl.jointMode(cam);  //FW-187   , BW-845
  Dxl.jointMode(shot); //UP-128   , DN-528 (speed = 200)
  delay(1000); 
  
  //Setup interrupt for keyboard input
  SerialUSB.println("Command Structure: DirectionSpeed");
  SerialUSB.println("Direction: i:Forward j:Left k:Backward l:right");
  SerialUSB.attachInterrupt(control);
}

void control(byte* input, byte ncount){
  SerialUSB.println("Received Command");
  
  char direction = input[0];
  char charSpeed[(ncount-1)];
  
  for(int i = 0; i < ncount; i++){
    charSpeed[i] = char(input[i+1]);
  }
  
  speed = atoi(charSpeed);
  
  /*Forward*/
  if (direction == 'i'){
    digitalWrite(BOARD_LED_PIN, LOW);
    Dxl.goalSpeed(lw, speed);
    Dxl.goalSpeed(rw, speed|0x400);
    
  }
  /*Backward*/
  else if (direction == 'k'){ 
    digitalWrite(BOARD_LED_PIN, LOW);
    Dxl.goalSpeed(lw, speed | 0x400);
    Dxl.goalSpeed(rw, speed);
    
  }
  /*Pivot Left*/
  else if (direction == 'j'){
    digitalWrite(BOARD_LED_PIN, LOW);
    Dxl.goalSpeed(lw, speed | 0x400);
    Dxl.goalSpeed(rw, speed | 0x400);
   
  }
  /*Pivot Right*/
  else if (direction == 'l'){
    digitalWrite(BOARD_LED_PIN, LOW);
    Dxl.goalSpeed(lw, speed);
    Dxl.goalSpeed(rw, speed); 
  }
  /*Turn camera forward*/
  else if (direction == 'f'){
    digitalWrite(BOARD_LED_PIN, LOW);
    Dxl.goalPosition(cam, 120); 
  }
  /*Turn camera backward*/
  else if (direction == 'b'){
    digitalWrite(BOARD_LED_PIN, LOW);
    Dxl.goalPosition(cam, 840); 
  }
  /*Shoot*/
  else if (direction == 's'){
    digitalWrite(BOARD_LED_PIN, LOW);
    Dxl.setPosition(shot, 128, 200);
    delay(1000);   
    Dxl.setPosition(shot, 528, 200); 
  }
  /*Stop*/
  else{
    digitalWrite(BOARD_LED_PIN, HIGH);
    Dxl.goalSpeed(lw, 0);
    Dxl.goalSpeed(rw, 0);
  }
  timestamp = millis();
}

 
void loop() {
  delay(200);
  if ((millis() - timestamp) > timeout){
    digitalWrite(BOARD_LED_PIN, HIGH);
    Dxl.goalSpeed(lw, 0);
    Dxl.goalSpeed(rw, 0); 
  } 
}



