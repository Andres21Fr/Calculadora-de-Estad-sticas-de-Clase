num = int(input("Ingrese un número entero: "))
fact = 1
for i in range(1, num + 1):
    fact *= i

print(f"El factorial de {num} es {fact}")
