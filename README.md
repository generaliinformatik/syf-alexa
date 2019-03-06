# syf-alexa / Amazon Alexa Skill 

Amazon Alexa Skill `SyF` (Arbeitstitel) startet und fragt das Sigfox Backend via APIv2 zu neuen IoT-Messwerten ab.

Nutzer: `Alexa, öffne <invocation name>.`<br />
Nutzer: `Alexa, öffne <invocation name> mit Details.`<br />
Nutzer: `Alexa, öffne <invocation name> mit Team.`<br />


## Installation
###Sigfox Backend

1. Übergabe der Messwerte in Das Sigfox Backend über eine geeignete Routine.
2. Einrichten von Zugangsinformationen für die API-Nutzung. Diese Angaben werden in dem Alexa Skill später unter `Sigfox_API_USername` und `Sigfox_API_Password` eingetragen.

*Hinweis: In dem vorliegenden Szenario werden die Daten komprimiert, so dass der gewünschte Wertebereich als Byte gesendet werden kann. Die Informationen im Backend haben dabei das Format xxyy, wobei `xx`der Protokollversion (01) und `yy` dem Messwert entspricht.*

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



##### Tags
 #sigfox #iot #aws #alexa #python #temperature