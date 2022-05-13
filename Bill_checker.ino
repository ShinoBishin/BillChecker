const int MaxPoint = 4; //お札を4カ所読み込む
int dd[MaxPoint]; //読み込みデータ格納配列
int dn; //計測したデータの数。これが溜まる(4になる)とデータをPCに送信する
boolean rf; //スイッチを離すタイミングを検出する変数
int ss; //モード変数(お札の種類をチェック！）


// LOW = Button_Push!
void setup()
{
    Serial.begin(9600);
    pinMode(2, INPUT_PULLUP);
    pinMode(3, INPUT_PULLUP);
    pinMode(4, INPUT_PULLUP);
    pinMode(5, INPUT_PULLUP);
    pinMode(6, INPUT_PULLUP);
    dn = 0;
    rf = true;
    ss = -1;
}

void loop()
{
    if (digitalRead(2) == LOW) {
        rf = false;
        delay(100);
    }
    else {
        if (rf == false) {
            rf = true;
            int v = analogRead(0);
            dd[dn] = v;
            dn++;
            if (dn == MaxPoint) {
                for (int i = 0; i < MaxPoint; i++) {
                    Serial.print(String(dd[i]) + ",");
                }
                Serial.println(ss);
                dn = 0;
            }
        }
    }

    if (digitalRead(3) == LOW) {
        ss =0;
        dn = 0;
    }

    else if (digitalRead(4) == LOW) {
        ss = 1;
        dn = 0;
    }
    else if (digitalRead(5) == LOW) {
        ss = 2;
        dn = 0;
    }

    else if (digitalRead(6) == LOW) {
        ss =3;
        dn = 0;
    }
}
