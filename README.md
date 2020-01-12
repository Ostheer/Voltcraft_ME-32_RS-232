# Voltcraft_ME-32_RS-232
Serial communication between computer and Voltcraft ME-32 (and similar) multimeters in Python

Proof of concept implementation of PySerial to use the DMM as data logger.

# The key
Alle Digitalmultimeter haben eine galvanische Trennung per Optokoppler zur Schnittstelle RS 232. *Die elektrische Spannungsversorgung der Optokoppler wird aus den Handshake-Leitungen des Computers ausgekoppelt. Hierzu ist die Leitung DTR auf  +12 Volt zu legen, die Leitung RTS muß mit -12 Volt belegt werden. Die Handshake-Leitungen dienen also nicht zur Synchronisierung der Datenübertragung sondern allein zur Stromversorgung* der galvanischen Trennung per Optokoppler.

So: the RTS and DTR lines must be forced to +-12V at all times. This is done via:
ser.setRTS(False)
ser.setDTR(True)
