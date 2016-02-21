/* Set Position Example*/
#define DXL_BUS_SERIAL1 1  //Dynamixel on Serial1(USART1)  <-OpenCM9.04
#define DXL_BUS_SERIAL2 2  //Dynamixel on Serial2(USART2)  <-LN101,BT210
#define DXL_BUS_SERIAL3 3  //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP

#define ID_NUM 102

Dynamixel Dxl(DXL_BUS_SERIAL1);

void setup() {
  Dxl.begin(3);  
  Dxl.setPacketType(DXL_PACKET_TYPE2);
  delay(1000);
  Dxl.jointMode(ID_NUM); //jointMode() is to use position mode
}

void loop() {
  Dxl.goalPosition(ID_NUM, 0); //forward
  delay(1000);
  Dxl.goalPosition(ID_NUM, 1023); //reverse
  delay(1000); 
}

