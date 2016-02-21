/* HW 3*/

/* Serial device defines for dxl bus */
#define DXL_BUS_SERIAL1 1  //Dynamixel on Serial1(USART1)  <-OpenCM9.04

/* Dynamixel ID defines */
#define ninetyID 101        //45<-->90
#define oneEightyID 102    //0<-->180  

Dynamixel Dxl(DXL_BUS_SERIAL1);

void setup() {
  // Initialize the dynamixel bus: 
  Dxl.begin(3);
  Dxl.setPacketType(DXL_PACKET_TYPE2);
  delay(1000);
  
  Dxl.jointMode(ninetyID);
  Dxl.jointMode(oneEightyID);
  Dxl.goalPosition(ninetyID, 154);
  Dxl.goalPosition(oneEightyID, 307);
  delay(1000); 
}

void loop() {
  
 //0-1 Second
 Dxl.goalPosition(ninetyID, 0);
 Dxl.goalPosition(oneEightyID, 0);
 delay(500);
 
 Dxl.goalPosition(oneEightyID, 615);
 delay(500);
 
 //1-2 Second
 Dxl.goalPosition(ninetyID, 307);
 Dxl.goalPosition(oneEightyID, 0); 
 delay(500);
 
 Dxl.goalPosition(oneEightyID, 615);
 delay(500);
}


