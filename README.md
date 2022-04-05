Hice dos versiones, por un  lado main.ipynb y New_version.ipynb. La segunda versión la hice para hacerla de manera más ordenada y cambiando algunas cosas.

# Exploración de columnas y filas

Vemos la lista de filas en las que todos los valores son nulos

Podemos eliminar 5145 filas (hasta el 20%)

Eliminamos el mayor numero de filas con todo nulos que podemos

Ambas columnas "unnamed" están completamente vacias por lo que las vamos a rellenar de ceros

Las columnas que son categorias como (type, country, Area, location, Activity, Name, Sex, Age, Injury, Fatal...) las vamos a rellenar sus NAN con unknown por el momento ya que si no hay valor es que en principio no tenemos información.

## Columnas "Case Number"
La columna Case number son fechas, por lo que finalmente vamos a querer tenerla como date type. Antes de eliminar los nulos vamos a limpiarla de manera que solo nos queden fechas.

He usado Regex para seleccionar las fechas en formato yyyy.mm.dd, de esta manera los elementos del final que son i.e ND-0154 se eliminan ya que no sabemos si esos números hace referencia al año, dia, mes....


Rellenamos los valores nulos con la última fecha disponible ya que será la más cercana de las que tenemos

Sobreescribimos columna Case Number.1 y 2 ya que hemos hecho: len(shark.drop_duplicates(subset=["Case Number.1","Case Number.2"]))==len(shark) y hemos visto que son exactamente iguales a "Case Number"


## Columna "Year"

Para la columna Year como los años van en orden, vamos a rellenar los nulos con el año equivalente a su índice en la columa Date.

Como la columna Date tiene formato yyyy-mm-dd, queremos que solo se queden los 4 primeros números. Es decir, el año.

## Columna "Age"

Vamos a rellenar los nulos de la columna age con la media de edad de los datos que tenemos ya que nos conviene mantener en la columna todo valores numéricos en lugar de añadir alguna categoría como "unknown", por lo que vamos a sustituir los "unknown" que habiamos puesto antes por la media

Hay valores que tienen letras, por lo que cogemos solo los valores numérico

 ## Columna "Sex"
Queremos dejar solo 3 categorias para la columna Sex: F, M, Unknown, por lo que vamos a sustituir las otras.

 ## Columna "Species"
La columna Species está hecha un desastre, solo me van a interesar aquellas que especifiquen el tipo de tiburón por lo que voy a coger solo la primera palabra antes de "shark" i.e. the white shark cojo "white".

 ## Columna "Time"
Vamos a categorizar la columna Time de manera que tengamos tres opciones: "Morning", "Afternoon", "Late Afternoon"
