# Scopescreen

Scopescreen ermöglicht es ein analoges Oszilloskop als Bildschirm zu verwenden.

## Idee

Die Idee stammt vom Spiel [Osziflap](https://pintman.github.io/osziflap/), bei
dem ein analoges Oszilloskop als Bildschirm verwendet wird. Um die Signale für
das Oszilloskop zu erzeugen, werden R-2R-Netzwerke als Digital-Analog-Wandler
an der GPIO-Schnittstelle eines Raspberry Pi verwendet. Da sich die I/O-Pins
nicht schnell genug schalten ließen, hatte Osziflap noch eine relativ geringe
Auflösung. Bei Überlegungen zur Verbesserung der Auflösung ist dieses Projekt
entstanden.

## Beispiel

![Beispiel](doc/bird.jpg)