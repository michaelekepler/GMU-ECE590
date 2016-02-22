/* Dynamixel ID Change Example*/
 /* Serial device defines for dxl bus */
#define DXL_BUS_SERIAL1 1  //Dynamixel on Serial1(USART1)  <-OpenCM9.04

/* Dynamixel ID defines */
#define J_ID 101
#define PRESENT_POS 54
 
Dynamixel Dxl(DXL_BUS_SERIAL1); 
 
void setup() {
  // Initialize the dynamixel bus:
  // Dynamixel 2.0 Baudrate -> 0: 9600, 1: 57600, 2: 115200, 3: 1Mbps  
  Dxl.begin(3);
Dxl.maxTorque(J_ID,1); // it has maxtorque for weak movement  
//  Dxl.jointMode(J_ID); //jointMode() is to use position mode  
}
 
void loop() {
  int pos;
  // Wait for 20 milliseconds
  delay(20);
 
  pos = Dxl.readWord(J_ID, PRESENT_POS); // Read present position
  SerialUSB.print("Present Position: ");
  SerialUSB.println(pos);
}
