# syf-alexa / Amazon Alexa Skill 

Amazon Alexa Skill `SyF` (Arbeitstitel) startet und fragt das Sigfox Backend via APIv2 zu neuen IoT-Messwerten ab.

Nutzer: `Alexa, öffne <invocation name>.`<br />
Nutzer: `Alexa, öffne <invocation name> mit Details.`<br />
Nutzer: `Alexa, öffne <invocation name> mit Team.`<br />


## Voraussetzungen
Folgende Bedingungen sind für diesen Skill vorausgesetzt:
1. Sigfox IoT-Gerät (z.B. Pycom-Geräte)
2. IoT-Gerät meldet Informationen an das Sigfox Backend (bzw. hat bereits gemeldet)
3. Sigfox Backend ist mittels API Zugang freigegeben
4. AWS Zugang
5. Amazon Developer (Alexa) Zugang

*Selbstverständlich können auch andere Geräte und ein anderes Netzwerk/Backend als Sigfox genutzt werden. Der Code ist entsprechend anzupassen.*

## Installation
###Sigfox Backend

1. Übergabe der Messwerte in Das Sigfox Backend über eine geeignete Routine.
2. Einrichten von Zugangsinformationen für die API-Nutzung. Diese Angaben werden in dem Alexa Skill später unter `Sigfox_API_USername` und `Sigfox_API_Password` eingetragen.

*Hinweis: In dem vorliegenden Szenario werden die Daten komprimiert, so dass der gewünschte Wertebereich als einzelnes Byte gesendet werden kann. Die Informationen im Backend haben dabei das Format xxyy, wobei `xx`der vom sendenden Gerät genutzten Protokollversion (01) und `yy` dem eigentlichen Messwert entspricht.*

###AWS Lambda

1. Amazon AWS Lambda Funktion anlegen (unter https://console.aws.amazon.com/console/home)
2. Neue Funktion mit Einstellungen `Author from scratch`, `Python 2.7 Runtine`, `Create a custome role` with `lambda_basic_execution' erstellen
2. `Alexa Skill Kit` als Trigger für die eigene Funktion auswählen
3. Code aus /aws_lambda/ in den Code9-Editor übernehmen
2. Environment Variables `Card_Title_Prefix`, `Skill_Name`, `Skill_Answer_DefaultMode`, `Sigfox_Device_ID`,  `Sigfox_API_USername` und `Sigfox_API_Password` definieren und mit den eigenen Werten angeben
3. Ausführbarkeit des Codes nochmals durch `Test`prüfen; hierzu ggf. ein Testereignis (`Testevent` auf Basis der Vorlage `Amazon Alexa Start Session`) erzeugen

###Alexa Skill
1. Amazon Alexa Skill anlegen im Amazon Developer (https://developer.amazon.com/home.html) unter `Alexa Skill Kit` einrichten
2. Skill mit `Custom` Modell und `Alexa-Hosted' Methode wählen.
2. `Invocation` angeben
3. Intents `detail`, `short`und `team` mit gewünschten eigenen Utterances anlegen (Beispiel siehe /alexa_skill/syf.json)
4. Endpoint für Amazon Alexa Skill ⇄ Amazon AWS Lambda Funktion einrichten und ARN des ASW Lambda Handlers eintragen
5. Skill nochmals speichern und neu generieren lassen

## Anmerkungen
Je nach Geschwindigkeit der Backend-Abfrage kann die initiale Start des Skills/der Lambda-Funktion und die Abfrage des Backends mehr als 3 Sekunden Zeit in Anspruch nehmen. Die Lambda-Funktion meldet in diesem Fall einen Timeout-Fehler. Tritt dieses Verhalten öfters auf, ist ggf. die Timeout-Voreinstellung von 3 Sekunden zu erhöhen. Dabei ist jedoch zu bedenken, dass längere Startphasen die UX beim Anwender beeinflussen können. Aus diesem Grund ist die hier dargestellte prototypische Abfrage auf ein Gerät (Device) beschränkt.

##### Tags
 #sigfox #iot #aws #alexa #python #temperature
