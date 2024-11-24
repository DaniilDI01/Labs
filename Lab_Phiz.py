from math import *
from turtle import *


# Изменяемые параметры
h = 20000   # Высота м
m = 250     # Масса  Кг
t = [i for i in range(6)]       # Время работы двигателя
power = 270   # Сила двигателя в кН
F1 = [1, 0] # Направление силы тяги



# Константы и нормализация параметров
G = 6.6743e-11
MZ = 5.9736 * (10**24)
R = 6371
h /= 100
power /= 100

N1 = [0, h]
N2 = []
Cords = [N1]

dot(10, 'green')
pencolor('black') # Устанавливаем цвет пера
speed(3)          # Устанавливаем скорость РИСОВАНИЯ
pensize(2)        # Устанавливаем ширину линии1
penup()
goto(N1[0], N1[1])
pendown()

he = window_height()
we = window_width()
setup(we*1.5, he*1.5)

A_p, B_p = 0, 0


# Фунеция работы двигателя за время t
def plus_power(vector, scale_factor):
    x, y = vector
    length = sqrt(x**2 + y**2)  # Находим длину исходного вектора
    unit_vector_x = x / length
    unit_vector_y = y / length
    new_length = length * scale_factor
    new_x = unit_vector_x * new_length
    new_y = unit_vector_y * new_length
    
    return (new_x, new_y)


# Подсчёт силы притяжения
def change_F():
    V_x, V_y = list(pos())
    N_length = sqrt(V_x**2 + V_y**2)
    F_length = (G * m * MZ/((R+N_length)**2))/(10**8)
    A_x = -V_x * (F_length / N_length)
    A_y = -V_y * (F_length / N_length)

    return ([A_x, A_y])

# Изменение угла вектора, после совершения перемещения
def rot_vect(V, alpha):
    return([V[0]*cos(alpha)-V[1]*sin(alpha), V[0]*sin(alpha)+V[1]*cos(alpha)])

F2 = [0, -round((G * m * MZ/((R+h)**2))/(10**8), 3)]
k = 0

# Цикл работы программы
while True:
    k += 1
    Summ = [F1[0]+F2[0], F1[1]+F2[1]]
    N2 = [N1[0]+Summ[0], N1[1]+Summ[1]]
    Angle = 2*pi-(acos((N1[0]*N2[0]+N1[1]*N2[1])/(sqrt(N1[0]**2+N1[1]**2)*sqrt(N2[0]**2+N2[1]**2)))) # Определение угла вектора силы F1 и (1, 0)

    # Проверка на то - упала ли ракета
    if (sqrt(list(pos())[0]**2 + list(pos())[1]**2) <= 15):
        goto(0,0)
        break


    A_p = list(pos())
    goto(N2[0], N2[1])
    F1 = rot_vect(F1, Angle)
    F2 = rot_vect(F2, Angle)
    B_p = list(pos())
    N1 = N2
    F2 = change_F() # Подсчёт силы притяжения

    # Включение/выключение двигателя в нужные периуды времени
    if k in t:
        F1 = plus_power(F1, power)
done()