
/* Serial device defines for dxl bus */
#define DXL_BUS_SERIAL1 1  //Dynamixel on Serial1(USART1)  <-OpenCM9.04

/* Dynamixel ID defines */
#define lw 101
#define rw 102

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
  
  pinMode(BOARD_LED_PIN, OUTPUT);
  digitalWrite(BOARD_LED_PIN, HIGH);

  Dxl.wheelMode(lw); //jointMode() is to use position mode
  Dxl.wheelMode(rw); //jointMode() is to use position mode 
  delay(500);
 
  //Setup interrupt for keyboard input
  SerialUSB.println("Command Structure: DirectionSpeed")
  SerialUSB.println("Direction: i:Forward
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
  /*Stop*/
  else{
    digitalWrite(BOARD_LED_PIN, HIGH);
    Dxl.goalSpeed(lw, 0);
    Dxl.goalSpeed(rw, 0);
  }
  timestamp = millis();
}

 
void loop(){  
  delay(200);
  if ((millis() - timestamp) > timeout){
    digitalWrite(BOARD_LED_PIN, HIGH);
    Dxl.goalSpeed(lw, 0);
    Dxl.goalSpeed(rw, 0); 
  }
  
}
