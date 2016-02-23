
/* Serial device defines for dxl bus */
#define DXL_BUS_SERIAL1 1  //Dynamixel on Serial1(USART1)  <-OpenCM9.04

/* Dynamixel ID defines */
#define lw 101
#define rw 102

Dynamixel Dxl(DXL_BUS_SERIAL1); 
 
int speed = 150;
int timeout = 250; //in units of ms

void setup() {
  // Initialize the dynamixel bus:
  // Dynamixel 2.0 Baudrate -> 0: 9600, 1: 57600, 2: 115200, 3: 1Mbps  
  Dxl.begin(3);
  Dxl.setPacketType(DXL_PACKET_TYPE2);
  delay(1000);

  Dxl.wheelMode(lw); //jointMode() is to use position mode
  Dxl.wheelMode(rw); //jointMode() is to use position mode 
  delay(500);
 
  //Setup interrupt for keyboard input
  SerialUSB.attachInterrupt(direction);
}

void direction(byte* input, byte ncount){
  SerialUSB.println("Received Command");
  /*Forward*/
  if (char(input[0]) == 'i'){
    Dxl.goalSpeed(lw, speed);
    Dxl.goalSpeed(rw, (speed+15)|0x400);
    delay(timeout);
  }
  /*Backward*/
  else if (char(input[0]) == 'k'){  
    Dxl.goalSpeed(lw, speed | 0x400);
    Dxl.goalSpeed(rw, (speed+15));
    delay(timeout);
  }
  /*Pivot Left*/
  else if (char(input[0]) == 'j'){
    Dxl.goalSpeed(lw, speed | 0x400);
    Dxl.goalSpeed(rw, speed | 0x400);
    delay(timeout);
  }
  /*Pivot Right*/
  else if (char(input[0]) == 'l'){
    Dxl.goalSpeed(lw, speed);
    Dxl.goalSpeed(rw, speed);
    delay(timeout);
  }
  /*Stop*/
  else{
    Dxl.goalSpeed(lw, 0);
    Dxl.goalSpeed(rw, 0);
    delay(timeout);
  }
  
  //Set the speed to zero
  Dxl.goalSpeed(lw, 0);
  Dxl.goalSpeed(rw, 0);
}

 
void loop(){  
}
