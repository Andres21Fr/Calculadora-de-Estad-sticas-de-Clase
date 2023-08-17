"""Problema: Calculadora de Estadísticas de Clase

Niel Jr. es un estudiante en una clase de matemáticas y quiere construir una pequeña calculadora en Python para ayudar a sus compañeros de clase a calcular algunas estadísticas básicas. Le gustaría que le ayudes a construir esta calculadora.

Tu tarea es escribir un programa en Python que realice las siguientes funciones:

Promedio: Dada una lista de notas numéricas, calcula y muestra el promedio de las notas.
Máximo: Dada una lista de notas numéricas, encuentra y muestra la nota más alta.
Mínimo: Dada una lista de notas numéricas, encuentra y muestra la nota más baja.
Cantidad de Notas: Dada una lista de notas numéricas, muestra la cantidad total de notas."""

notas = []

numero = int(input("ingrese el numero de notas: "))

for i in range(numero):
    ingresar = int(input("digite el numero siguiente:"))
    notas.append(ingresar)
    pro = (sum(notas))/numero

print(f"el promedio de las notas es :{pro},La notas mas alta es:{max(notas)}, la nota mas baja es{min(notas)},y la cantidad total de notas es:{numero}")
