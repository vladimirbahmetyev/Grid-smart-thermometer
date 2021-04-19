#include <NewPing.h>
#include <i2cmaster.h>

#define PIN_TRIG 12 //ультразвук
#define PIN_ECHO 10 //ультразвук

#define MAX_DISTANCE 200 //константа для определения максимального расстояния, которое мы будем считать корректным

//создаем объект, методами которого будем затем пользоваться для получения расстояния
//в качестве параметров передаем номера пинов, к которым подключены выходы ECHO и TRIG датчика

NewPing sonar(PIN_TRIG, PIN_ECHO, MAX_DISTANCE); 

int data;
void setup() { 
  //инициализируем взаимодействие по последовательному порту на скорости 9600
  Serial.begin(9600);
  pinMode(11, OUTPUT); //красная лампочка
  pinMode(13, OUTPUT); //зеленая лампочка
  Serial.println("Setup...");
  i2c_init(); //инициализируем i2c
  PORTC = (1 << PORTC4) | (1 << PORTC5);//подключаем порты для датчика измерения температуры
  digitalWrite (13, LOW);
}
 
void loop() {
while (Serial.available()){
  data = Serial.read();
}
if (data == '1') {
    digitalWrite (11, LOW);
    digitalWrite (13, LOW);
    unsigned int distance = 100;
    //запускаем измерение расстояния
    while (distance > 50){
      //стартовая задержка, необходимая для корректной работы.
      delay(50);

      //получаем значение от датчика расстояния и сохраняем его в переменную
      distance = sonar.ping_cm();

      //печатаем расстояние в мониторе порта
      Serial.print(distance);
      Serial.println("см");
    }
    //когда человек подошел достаточно близко запускаем измерение температуры через 5 секунд
    delay(5000);
    int dev = 0x5A<<1;
    int data_low = 0;
    int data_high = 0;
    int pec = 0;
 
    i2c_start_wait(dev+I2C_WRITE);
    i2c_write(0x07);
 
    //читаем
    i2c_rep_start(dev+I2C_READ);
    data_low = i2c_readAck(); //читаем 1 байт и отправляе подтверждение
    data_high = i2c_readAck(); //читаем 1 байт и отправляе подтверждение
    pec = i2c_readNak();
    i2c_stop();
 
    //преобразуем старший и младший байты вместе и обрабатываем температуру, MSB является битом ошибки и игнорируется для температур
    double tempFactor = 0.02; //0,02 градуса на младший бит (разрешение измерения MLX90614)
    double tempData = 0x0000; //обнулить данные
    int frac; //данные после десятичной точки
 
    //маскируем бит ошибки старшего байта, затем перемещаем его влево на 8 бит и добавляем младший байт
    tempData = (double)(((data_high & 0x007F) << 8) + data_low);
    tempData = (tempData * tempFactor)-0.01;
   
    float celcius = tempData - 273.15;
 
    Serial.print("Celcius: ");
    Serial.println(celcius);
    delay(1000); 
    //если температура человека в норме, загорается зеленая лампочка
    if (celcius <= 32.5){
      digitalWrite(13, HIGH);
      delay(10000); // ждем 10 секунд
      digitalWrite(13, LOW);
      delay(1000); // ждем 1 секунду
    }
    //если нет - красная
    else {
      digitalWrite(11, HIGH);
      delay(10000); // ждем 10 секунд
      digitalWrite(11, LOW);
      delay(1000); // ждем 1 секунду
    }
    Serial.println("1");
    data = 0;
}
else { 
  if (data == '0'){
    digitalWrite (13, LOW);
    digitalWrite (11, HIGH);
    Serial.println("Bye, bye!");
}
}
}
