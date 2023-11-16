import math

def generate_wheel_geometry(num_sides, radius, width):
    """
    Genera la geometría de una rueda y devuelve los vértices, normales y caras.
    """
    vertices = []  # Inicializa una lista vacía para almacenar los vértices

    for i in range(2):  # Itera dos veces (para los dos lados de la rueda)
        # Ajuste del ancho dependiendo del lado de la rueda
        if i == 1:
            width_offset = round(-width / 2, 5)  # Offset negativo para el lado opuesto con 5 decimales
        else:
            width_offset = round(width / 2, 5)   # Offset positivo para el lado cercano con 5 decimales

        # Añade el vértice central de la cara
        vertices.append([width_offset, 0, 0])  # Añade las coordenadas del vértice a la lista

        for j in range(num_sides):  # Itera a través del número de lados de la rueda
            # Calcula las coordenadas y y z de los vértices alrededor del centro
            y = round(radius * math.sin(math.radians(360 / num_sides * (j + 1))), 5)  # Con 5 decimales
            z = round(radius * math.cos(math.radians(360 / num_sides * (j + 1))), 5)  # Con 5 decimales

            vertices.append([width_offset,  y,  z])  # Añade las coordenadas del vértice a la lista

    caras = []  # Inicializa una lista vacía para almacenar las caras

    for i in range(num_sides):  # Itera a través del número de lados de la rueda
        if (i < num_sides - 1):
            # Añade las caras para las caras circulares y laterales
            caras.append([1, 3 + i, 2 + i])
            caras.append([num_sides + 2, num_sides + 3 + i, num_sides + 4 + i])
            caras.append([2 + i, 3 + i, num_sides + 3 + i])
            caras.append([3 + i, num_sides + 4 + i, num_sides + 3 + i])
        else:
            # Añade las caras para las caras circulares y laterales en la última iteración
            caras.append([1, 2, 2 + i])
            caras.append([num_sides + 2, num_sides + 3 + i, num_sides + 3])
            caras.append([2 + i, 2, num_sides + 3 + i])
            caras.append([2, num_sides + 3, num_sides + 3 + i])
    
    normales = []  # Inicializa una lista vacía para almacenar los vectores normales

    for i in range(num_sides):  # Itera a través del número de lados de la rueda
        if (i < num_sides - 1):
            # Calcula las normales para las caras circulares y laterales
            normales.append(calculate_normal(vertices, 0, i + 2, i + 1))
            normales.append(calculate_normal(vertices, num_sides + 1, num_sides + 2 + i, num_sides + 3 + i))
            normales.append(calculate_normal(vertices, 1 + i, 2 + i, num_sides + 2 + i))
            normales.append(calculate_normal(vertices, 2 + i, num_sides + 3 + i, num_sides + 2 + i))
        else:
            # Calcula las normales para las caras circulares y laterales en la última iteración
            normales.append(calculate_normal(vertices, 0, 1, 1 + i))
            normales.append(calculate_normal(vertices, num_sides + 1, num_sides + 2 + i, num_sides + 2))
            normales.append(calculate_normal(vertices, 1 + i, 1, num_sides + 2 + i))
            normales.append(calculate_normal(vertices, 1, num_sides + 2, num_sides + 2 + i))

    return vertices, normales, caras  # Devuelve las listas de vértices, normales y caras

def calculate_normal(vertices, i, j, z):
    """
    Calcula el vector normal entre tres vértices usando los índices que tienen estos en el vector de vértices.
    """
    # Calcula los vectores A y B
    A = [vertices[j][0] - vertices[i][0],  # Componente x de A
         vertices[j][1] - vertices[i][1],  # Componente y de A
         vertices[j][2] - vertices[i][2]]  # Componente z de A

    B = [vertices[z][0] - vertices[i][0],  # Componente x de B
         vertices[z][1] - vertices[i][1],  # Componente y de B
         vertices[z][2] - vertices[i][2]]  # Componente z de B

    # Calcula el producto cruz entre A y B para obtener el vector normal w
    w = [A[1] * B[2] - A[2] * B[1],  # Componente x del vector normal
         A[2] * B[0] - A[0] * B[2],  # Componente y del vector normal
         A[0] * B[1] - A[1] * B[0]]  # Componente z del vector normal

    return [round(w[0], 5), round(w[1], 5), round(w[2], 5)]  # Devuelve el vector normal redondeado con 5 decimales


def write_obj_file(vertices, normales, caras, file_path):
    """
    Escribe la geometría en un archivo OBJ.
    """
    output = []  # Inicializa una lista vacía para almacenar las líneas de salida

    for vertex in vertices:
        # Escribe los vértices en el formato 'v x y z'
        output.append(f"v {vertex[0]:.5f} {vertex[1]:.5f} {vertex[2]:.5f}\n")  # Con 5 decimales

    output.append("\n\n")  

    for normal in normales:
        # Escribe las normales en el formato 'vn x y z'
        output.append(f"vn {normal[0]:.5f} {normal[1]:.5f} {normal[2]:.5f}\n")  # Con 5 decimales

    output.append("\n\n") 

    for i in range(len(caras)):
        # Escribe las caras en el formato 'f v1//n1 v2//n2 v3//n3'
        output.append(f"f {caras[i][0]}//{i + 1} {caras[i][1]}//{i + 1} {caras[i][2]}//{i + 1}\n")

    with open(file_path, "w") as file:
        # Escribe todo el contenido en el archivo
        file.writelines(output)

if __name__ == "__main__":
    print("------ Modelo de creación de llantas ------\n\n")
    num_sides_input = input("¿Cuantos lados del circulo quiere? (Presione Enter para usar el valor predeterminado): ")

    if num_sides_input:
        num_sides = int(num_sides_input)
        if num_sides < 4 or num_sides > 360:
            print("El número de lados debe estar entre 3 (no igual) y 360.")
            exit()
    else:
        num_sides = 8

    radius_input = input("¿De cuánto quiere que sea el radio de la llanta? (Presione Enter para usar el valor predeterminado): ")
    width_input = input("¿De qué ancho quiere la llanta? (Presione Enter para usar el valor predeterminado): ")

    num_sides = int(num_sides_input) if num_sides_input else 8
    radius = float(radius_input) if radius_input else 1
    width = float(width_input) if width_input else 0.5

    # Genera la geometría de la rueda
    vertices, normals, faces = generate_wheel_geometry(num_sides, radius, width)

    # Escribe la geometría en un archivo OBJ
    write_obj_file(vertices, normals, faces, "./wheel.obj")  # Archivo de salida
    
    print("\n\n***** ¡Llanta creada con éxito! *****")
