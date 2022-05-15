"""
Software de punto de venta, creado por:
Caballero Cepeda Kevin Ricardo.
Chávez Castillo Jose Fernando.
Del Castillo Vázquez Miguel.
Mireles Cisneros Fernando Dilland.
Sánchez Juárez Juan De Dios.
"""
# Importación de librerías
import sys
from PyQt5 import uic
import mysql.connector
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from numpy import var
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Punto_de_venta(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Punto_de_venta.ui", self) # Abrir el archivo .ui
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )
        # Sistema de mostrado del nombre del usuarios del sistema (Ej. Fernando Mireles)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Nombre FROM Usuarios_sistema \
        WHERE Nickname='%s';" % (usuario_introducido))
        respuesta_bd = mycursor.fetchall()
        self.nombre_usuario.setText(str(respuesta_bd[0][0]))
        # Sistema de gestión con base al rango del usuario que inició sesión
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Tipo FROM Usuarios_sistema \
        WHERE Nickname='%s';" % (usuario_introducido))
        global rango_usuario
        rango_usuario = mycursor.fetchall()
        rango_usuario = rango_usuario[0][0] # Cajero, Vendedor o Administrador
        print("Rango:", rango_usuario)
        # Mostrado de botones de administracion de usuarios en usuarios del sistema
        if rango_usuario == "Administrador":
            self.texto_rango.setText(str("Administrador, cuenta con acceso"))
            self.label_8.setEnabled(True) # Activación de texto
            self.label_9.setEnabled(True) # Activación de texto
            self.label_10.setEnabled(True) # Activación de texto
            self.label_11.setEnabled(True) # Activación de texto
            self.label_12.setEnabled(True) # Activación de texto
            self.label_13.setEnabled(True) # Activación de texto
            self.label_14.setEnabled(True) # Activación de texto
            self.label_15.setEnabled(True) # Activación de texto
            self.celda_clave_usuario.setEnabled(True) # Activación de celda
            self.celda_contrasenia_usuario.setEnabled(True) # Activación de celda
            self.celda_nombre_usuario.setEnabled(True) # Activación de celda
            self.celda_correo_usuario.setEnabled(True) # Activación de celda
            self.celda_telefono_usuario.setEnabled(True) # Activación de celda
            self.celda_nickname_usuario.setEnabled(True) # Activación de celda
            self.combo_box_tipo.setEnabled(True) # Activación de combobox
            self.combo_box_estatus.setEnabled(True) # Activación de combobox
            self.boton_registrar_usuario.setEnabled(True) # Activación de botón
            self.boton_eliminar_usuario.setEnabled(True) # Activación de botón
        else:
            self.texto_rango.setText(str("No cuenta con acceso"))
        self.fn_init_UI()

    # Función Init_UI (para clics de botones)
    def fn_init_UI(self):
        global importe_total
        importe_total = 0
        self.boton_salir.clicked.connect(self.salida) # Botón salida general
        self.boton_act.clicked.connect(self.actualizar_lista_usuario) # Boton de actualizar lista de usuarios en usuarios del sistema
        self.boton_registrar_usuario.clicked.connect(self.fn_registrar)
        self.boton_registrar_usuario.clicked.connect(self.actualizar_lista_usuario)
        self.boton_registrar_usuario.clicked.connect(self.actualizar_lista_usuario)
        self.boton_eliminar_usuario.clicked.connect(self.fn_eliminar)
        self.boton_eliminar_usuario.clicked.connect(self.actualizar_lista_usuario)
        self.boton_act_2.clicked.connect(self.actualizar_lista_cliente) # Boton de actualizar lista de clientes
        self.boton_buscar_saldos_cte.clicked.connect(self.buscar_saldos_cliente)
        self.boton_actualizar_limite_credito_cte.clicked.connect(self.actualizar_limite_credito_cliente)
        self.boton_actualizar_limite_credito_cte.clicked.connect(self.buscar_saldos_cliente)
        self.boton_actualizar_limite_credito_cte.clicked.connect(self.actualizar_lista_cliente)
        self.boton_actualizar_saldo_cte.clicked.connect(self.actualizar_saldo_cliente)
        self.boton_actualizar_saldo_cte.clicked.connect(self.buscar_saldos_cliente)
        self.boton_actualizar_saldo_cte.clicked.connect(self.actualizar_lista_cliente)
        self.boton_registro_cte.clicked.connect(self.registro_cliente)
        self.boton_registro_cte.clicked.connect(self.actualizar_lista_cliente)
        self.boton_eliminacion_cliente.clicked.connect(self.elimina_cliente)
        self.boton_eliminacion_cliente.clicked.connect(self.actualizar_lista_cliente)
        self.boton_acr_almacen.clicked.connect(self.actualizar_alamcen)
        self.boton_acr_almacen.clicked.connect(self.actualizar_mov_alamcen)
        self.boton_actualizar_prod.clicked.connect(self.actualizar_linea_productos)
        self.boton_actualizar_prod.clicked.connect(self.actualizar_productos)
        self.boton_reg_producto.clicked.connect(self.registro_producto)
        self.boton_reg_producto.clicked.connect(self.actualizar_linea_productos)
        self.boton_reg_producto.clicked.connect(self.actualizar_productos)
        self.boton_agregar_producto_cuenta.clicked.connect(self.agregar_producto_cuenta)
        self.boton_registrar_venta.clicked.connect(self.registrar_venta)
        self.boton_obtener_reporte.clicked.connect(self.reporte_ventas_dia)
        self.boton_mostrar_grafica_barra.clicked.connect(self.mostrar_grafica_barra)
        self.boton_most_graf_inv.clicked.connect(self.mostrar_grafica_pastel)
        self.boton_most_tend.clicked.connect(self.mostrar_grafica_tendencia)

    # Función de salida del programa
    def salida(self):
        self.close()

    # Funcion actualizar lista de usuarios en usuarios del sistema
    def actualizar_lista_usuario(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM usuarios_sistema")
        datos = mycursor.fetchall()
        if datos:
            self.tabla_datos.setRowCount(len(datos))
            tablerow = 0
            for i in datos:
                self.tabla_datos.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(i[1])))
                self.tabla_datos.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str("******")))
                self.tabla_datos.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(i[3])))
                self.tabla_datos.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(i[4])))
                self.tabla_datos.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(i[5])))
                self.tabla_datos.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(i[6])))
                self.tabla_datos.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(i[7])))
                tablerow = tablerow + 1

    # Funcion actualizar lista de usuarios en usuarios del sistema
    def actualizar_lista_cliente(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM cliente")
        datos = mycursor.fetchall()
        if datos:
            self.tabla_datos_2.setRowCount(len(datos))
            tablerow = 0
            for i in datos:
                self.tabla_datos_2.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(i[1])))
                self.tabla_datos_2.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(i[2])))
                self.tabla_datos_2.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(i[3])))
                self.tabla_datos_2.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(i[4])))
                self.tabla_datos_2.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(i[5])))
                self.tabla_datos_2.setItem(tablerow, 5, QtWidgets.QTableWidgetItem("$"+str(i[6])))
                self.tabla_datos_2.setItem(tablerow, 6, QtWidgets.QTableWidgetItem("$"+str(i[7])))
                tablerow = tablerow + 1

    # Función de registro de usuario
    def fn_registrar(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO usuarios_sistema (Clave_usuario, Nickname, Contraseña, Nombre, Tipo,Correo, Telefono, Estatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        v1 = self.celda_clave_usuario.text()
        v2 = self.celda_nickname_usuario.text()
        v3 = self.celda_contrasenia_usuario.text()
        v4 = self.celda_nombre_usuario.text()
        v5 = str(self.combo_box_tipo.currentText())
        v6 = self.celda_correo_usuario.text()
        v7 = self.celda_telefono_usuario.text()
        v8 = str(self.combo_box_estatus.currentText())

        val = (v1,v2,v3,v4,v5,v6,v7,v8)

        #Inyección de datos a la base de datos
        mycursor.execute(sql, val) # Comando sql y valores a inyectar
        mydb.commit()

        # Limpieza de celdas
        self.celda_nickname_usuario.clear()
        self.celda_clave_usuario.clear()
        self.celda_contrasenia_usuario.clear()
        self.celda_nombre_usuario.clear()
        self.celda_correo_usuario.clear()
        self.celda_telefono_usuario.clear()

    # Función de eliminación de usuario con Nickname
    def fn_eliminar(self):

        varb = self.celda_nickname_usuario.text()
        varb = "\'"+varb+"\'"
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()
        sql = "DELETE FROM usuarios_sistema WHERE Nickname = "+varb
        mycursor.execute(sql)
        mydb.commit()
        print("Usuario borrado")

        # Limpieza de celdas
        self.celda_nickname_usuario.clear()

    # Función buscar saldo cliente
    def buscar_saldos_cliente(self):
        nombre_cte = self.celda_nombre_cte_gest_sald.text()
        print("Cliente a buscar saldo:", nombre_cte)

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        # Busqueda por nombre
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Limite_credito FROM cliente \
        WHERE Nombre_cliente='%s';" % (str(nombre_cte)))
        respuesta_limite_credito = mycursor.fetchall()
        print("Límite de crédito:", respuesta_limite_credito[0][0])

        mycursor.execute("SELECT Saldo FROM cliente \
        WHERE Nombre_cliente='%s';" % (str(nombre_cte)))
        respuesta_saldo = mycursor.fetchall()
        print("Saldo:", respuesta_saldo[0][0])

        self.label_16.setText("$"+str(respuesta_limite_credito[0][0]))
        self.label_17.setText("$"+str(respuesta_saldo[0][0]))

    def actualizar_limite_credito_cliente(self):
        nuevo_limite_credito = self.celda_nombre_cte_gest_sald_2.text()
        nombre_cte = self.celda_nombre_cte_gest_sald.text()

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )
        # Actualizar datos
        mycursor = mydb.cursor()
        mycursor.execute("""UPDATE cliente SET Limite_credito = %s WHERE Nombre_cliente = %s""", (nuevo_limite_credito, nombre_cte))
        mydb.commit()
        self.celda_nombre_cte_gest_sald_2.clear()

    def actualizar_saldo_cliente(self):
        nuevo_saldo = self.celda_nombre_cte_gest_sald_3.text()
        nombre_cte = self.celda_nombre_cte_gest_sald.text()

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )
        # Actualizar datos
        mycursor = mydb.cursor()
        mycursor.execute("""UPDATE cliente SET Saldo = %s WHERE Nombre_cliente = %s""", (nuevo_saldo, nombre_cte))
        mydb.commit()
        self.celda_nombre_cte_gest_sald_3.clear()

    def registro_cliente(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO cliente (Clave_cliente, Nombre_cliente, Direccion, Correo, Telefono, Estatus, Limite_credito, Saldo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        v1 = self.celda_registro_clave.text()
        v2 = self.celda_registro_nombre.text()
        v3 = self.celda_registro_direccion.text()
        v4 = self.celda_registro_correo.text()
        v5 = self.celda_registro_telefono.text()
        v6 = str(self.combo_box_registro_estatus.currentText())
        v7 = self.celda_registro_limite_credito.text()
        v8 = self.celda_registro_saldo.text()

        val = (v1,v2,v3,v4,v5,v6,v7,v8)

        #Inyección de datos a la base de datos
        mycursor.execute(sql, val) # Comando sql y valores a inyectar
        mydb.commit()

        # Limpieza de celdas
        self.celda_registro_clave.clear()
        self.celda_registro_nombre.clear()
        self.celda_registro_direccion.clear()
        self.celda_registro_correo.clear()
        self.celda_registro_telefono.clear()
        self.celda_registro_limite_credito.clear()
        self.celda_registro_saldo.clear()

    def elimina_cliente(self):
        varb = self.celda_nombre_cte_gest_sald.text()
        varb = "\'"+varb+"\'"
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()
        sql = "DELETE FROM cliente WHERE Nombre_cliente = "+varb
        mycursor.execute(sql)
        mydb.commit()
        print("Cliente borrado")

        # Limpieza de celdas
        self.celda_nombre_cte_gest_sald.clear()

    def actualizar_alamcen(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM almacen")
        datos = mycursor.fetchall()
        if datos:
            self.tabla_datos_almacen.setRowCount(len(datos))
            tablerow = 0
            for i in datos:
                self.tabla_datos_almacen.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(i[1])))
                self.tabla_datos_almacen.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(i[2])))
                self.tabla_datos_almacen.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(i[3])))
                self.tabla_datos_almacen.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(i[4])))
                tablerow = tablerow + 1

    def actualizar_mov_alamcen(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM movimiento_almacen")
        datos = mycursor.fetchall()
        if datos:
            self.tabla_datos_mov_almacen.setRowCount(len(datos))
            tablerow = 0
            for i in datos:
                self.tabla_datos_mov_almacen.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(i[1])))
                tablerow = tablerow + 1

    def actualizar_linea_productos(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM linea_de_producto")
        datos = mycursor.fetchall()
        if datos:
            self.tabla_linea_de_producto.setRowCount(len(datos))
            tablerow = 0
            for i in datos:
                self.tabla_linea_de_producto.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(i[1])))
                self.tabla_linea_de_producto.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(i[2])))
                tablerow = tablerow + 1

    def actualizar_productos(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM producto")
        datos = mycursor.fetchall()
        if datos:
            self.tabla_producto.setRowCount(len(datos))
            tablerow = 0
            for i in datos:
                self.tabla_producto.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(i[1])))
                self.tabla_producto.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(i[2])))
                self.tabla_producto.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(i[3])))
                self.tabla_producto.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(i[4])))
                self.tabla_producto.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(i[5])))
                self.tabla_producto.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(i[6])))
                tablerow = tablerow + 1

    def registro_producto(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO linea_de_producto (Clave_linea, Descripcion, Estatus) VALUES (%s, %s, %s)"
        sql2 = "INSERT INTO producto (Clave_producto, Descripcion, Unidad_medida, Fecha_ult_compra, Fecha_ult_venta, Costo, Precio) VALUES (%s, %s, %s,%s, %s, %s, %s)"

        v1 = self.celda_clave_linea_producto.text()
        v2 = self.celda_desc_linea_producto.text()
        v3 = str(self.combo_estatus_producto_linea.currentText())

        v4 = self.celda_registro_producto.text()
        v5 = self.celda_registro_desc.text()
        v6 = self.celda_registro_unidad.text()
        v7 = self.celda_registro_fecha_compra.text()
        v8 = self.celda_registro_fecha_venta.text()
        v9 = self.celda_registro_costo.text()
        v10 = self.celda_precio_product.text()

        val = (v1, v2, v3)
        val2 = (v4, v5, v6, v7, v8, v9, v10)

        #Inyección de datos a la base de datos
        mycursor.execute(sql, val) # Comando sql y valores a inyectar
        mydb.commit()
        #Inyección de datos a la base de datos
        mycursor.execute(sql2, val2) # Comando sql y valores a inyectar
        mydb.commit()

        # Limpieza de celdas
        self.celda_clave_linea_producto.clear()
        self.celda_desc_linea_producto.clear()

        self.celda_registro_producto.clear()
        self.celda_registro_desc.clear()
        self.celda_registro_unidad.clear()
        self.celda_registro_fecha_compra.clear()
        self.celda_registro_fecha_venta.clear()
        self.celda_registro_costo.clear()
        self.celda_precio_product.clear()

    # Agregar productos a la tabla
    def agregar_producto_cuenta(self):
        producto = self.producto_agregar.text()
        cantidad = self.cantidad_agregar.text()

        numRows = self.tabla_productos_agregados.rowCount()
        self.tabla_productos_agregados.insertRow(numRows)

        # Claculo importe
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )
        # Sistema de mostrado del nombre del usuarios del sistema (Ej. Fernando Mireles)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Precio FROM producto \
        WHERE Descripcion='%s';" % (producto))
        respuesta_bd = mycursor.fetchall()
        importe = int(cantidad) * float(respuesta_bd[0][0])

        global importe_total
        importe_total = importe_total + importe

        self.importe_total.setText("$"+str(importe_total))

        self.tabla_productos_agregados.setItem(numRows, 0, QtWidgets.QTableWidgetItem(str(producto)))
        self.tabla_productos_agregados.setItem(numRows, 1, QtWidgets.QTableWidgetItem(str(cantidad)))
        self.tabla_productos_agregados.setItem(numRows, 2, QtWidgets.QTableWidgetItem(str(importe)))

        # Limpieza de celdas
        self.producto_agregar.clear()
        self.cantidad_agregar.clear()

    def registrar_venta(self):
        # Obtención de datos de tabla
        cantidad_registros = self.tabla_productos_agregados.rowCount()
        print("Cantidad de registros:",cantidad_registros)
        datos_tabla = []
        for i in range(cantidad_registros):
            dato1 = self.tabla_productos_agregados.item(i,0).text()
            dato2 = self.tabla_productos_agregados.item(i,1).text()
            dato3 = self.tabla_productos_agregados.item(i,2).text()
            datos_tabla.append([dato1,dato2,dato3])
        print("Datos de tabla:",datos_tabla)
        print("Cantidad de productos diferentes:",len(datos_tabla))

        # Obtención de datos de celdas
        v1 = self.celda_num_tick.text()
        v2 = self.celda_fecha_venta.text()
        v3 = str(self.combo_sucursal_venta.currentText())
        v4 = self.celda_cliente_venta.text()
        v5 = self.producto_agregar.text()
        v6 = self.cantidad_agregar.text()

        print("Datos de celdas:", v1, v2, v3, v4, v5, v6)



        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO ticket (Numero_ticket, Fecha, Sucursal, Importe) VALUES (%s, %s, %s, %s)"
        sql2 = "INSERT INTO detalle_ticket (Numero_ticket, Detalle, Producto, Cantidad, Importe) VALUES (%s, %s, %s, %s, %s)"

        global importe_total

        #Inyección de datos a la base de datos
        val = (v1, v2, v3, importe_total)
        mycursor.execute(sql, val) # Comando sql y valores a inyectar
        mydb.commit()
        for i in range(len(datos_tabla)):
            val2 = (v1, "", datos_tabla[i][0], datos_tabla[i][1], datos_tabla[i][2])
            mycursor.execute(sql2, val2) # Comando sql y valores a inyectar
            mydb.commit()


        # Limpieza de celdas
        self.celda_num_tick.clear()
        self.celda_fecha_venta.clear()
        self.celda_cliente_venta.clear()
        self.producto_agregar.clear()
        self.cantidad_agregar.clear()
        self.tabla_productos_agregados.clearContents()
        self.tabla_productos_agregados.setRowCount(0)

        importe_total = 0
        self.importe_total.setText("$"+str(importe_total))

        print("Venta registrada con éxito")

    def reporte_ventas_dia(self):
        fecha_en_celda = (self.celda_fecha_reporte_dia.text())

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM ticket \
        WHERE Fecha ='%s';" % (fecha_en_celda))
        datos = mycursor.fetchall()
        if datos:
            self.tabla_reporte_ventas_dia.setRowCount(len(datos))
            tablerow = 0
            for i in datos:
                self.tabla_reporte_ventas_dia.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(i[1])))
                self.tabla_reporte_ventas_dia.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(i[2])))
                self.tabla_reporte_ventas_dia.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(i[3])))
                tablerow = tablerow + 1

    def mostrar_grafica_barra(self):
        almacen_elegido = (self.combo_grafica_barra_almacen_elegido.currentText())
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )
        # Sistema de mostrado del nombre del usuarios del sistema (Ej. Fernando Mireles)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT dt.Producto, SUM(dt.Cantidad) AS total \
        FROM ticket as t inner join detalle_ticket as dt \
        WHERE Sucursal = '%s' \
        and t.Numero_ticket = dT.Numero_ticket \
        group by dt.Producto \
        order by SUM(dt.Cantidad) Desc;" % (almacen_elegido))

        respuesta_bd = mycursor.fetchall()

        ## Declaramos valores para el eje x
        eje_x = [respuesta_bd[0][0],respuesta_bd[1][0],\
            respuesta_bd[2][0],respuesta_bd[3][0],respuesta_bd[4][0]]

        ## Declaramos valores para el eje y
        eje_y = [respuesta_bd[0][1],respuesta_bd[1][1],\
            respuesta_bd[2][1],respuesta_bd[3][1],respuesta_bd[4][1]]

        ## Creamos Gráfica
        plt.bar(eje_x, eje_y)

        ## Legenda en el eje y
        plt.ylabel('Cantidad de ventas')

        ## Legenda en el eje x
        plt.xlabel('Producto vendido')

        ## Título de Gráfica
        plt.title(('5 productos más vendidos de '+str(almacen_elegido)))

        ## Mostramos Gráfica
        plt.show()
        pass

    def mostrar_grafica_pastel(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )
        # Sistema de mostrado del nombre del usuarios del sistema (Ej. Fernando Mireles)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Descripcion, \
        Costo From Producto;")
        respuesta_bd = mycursor.fetchall()
        cantidad_registros = len(respuesta_bd)
        datos_tabla_costo = []
        for i in range(cantidad_registros):
            dato1 = respuesta_bd[i][0]
            datos_tabla_costo.append([dato1])

        costo = []
        descripcion = []
        for a, b in respuesta_bd:
            costo.append(b)
            descripcion.append(a)

        datos_tabla_descripcion = []
        for i in range(cantidad_registros):
            dato1 = respuesta_bd[i][1]
            datos_tabla_descripcion.append([dato1])

        plt.pie(costo, labels=descripcion, autopct="%0.1f %%")
        plt.axis("equal")
        plt.show()

    def mostrar_grafica_tendencia(self):
        print("gg1")
        almacen_elegido = (self.combo_grafica_barra_almacen_elegido_2.currentText())
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )
        # Sistema de mostrado del nombre del usuarios del sistema (Ej. Fernando Mireles)
        mycursor = mydb.cursor()
        print("gg2")
        mycursor.execute("SELECT cast(FECHA as char), cast(sum(IMPORTE) as float)\
        FROM TICKET \
        WHERE Sucursal = '%s' \
        group by fecha \
        order by FECHA ASC limit 5;" % (almacen_elegido))
        print("gg3")
        respuesta_bd_2 = mycursor.fetchall()
        cantidad_registros = len(respuesta_bd_2)
        datos_tabla_costo = []
        print("gg4", respuesta_bd_2)
        x = []
        y = []
        for a, b in respuesta_bd_2:
            x.append(b)
            y.append(a)
        print("gg5")
        #create data
        print("x", x)
        print("y", y)
        days = [1,2,3,4,5]
        #np.array(x).astype(np.float)
        sns.regplot(days, x, ci=None)
        plt.show()




# Gestión de clase para el Qt
class acceso_punto_de_venta(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Acceso_punto_de_venta.ui", self) # Abrir el archivo .ui
        self.fn_init_UI()

        #self.btn_Desactivar.setEnabled(False)

    # Función Init_UI (para clics de botones)
    def fn_init_UI(self):
        self.boton_acceso.clicked.connect(self.revisar_acceso)

    # Función que revisa el acceso (usuario y contraseña correctos)
    def revisar_acceso(self):
        print("-- Intento de acceso --")

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="punto_de_venta"
        )

        mycursor = mydb.cursor()

        #sql = "INSERT INTO usuarios_sistema (Clave_usuario, Nickname, Contraseña, Nombre, Tipo, Correo, Telefono, Estatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        global usuario_introducido
        usuario_introducido = self.campo_usuario.text()
        contrasenia_introducida = self.campo_contrasenia.text()

        # Sistema de retorno y verificación de contraseña
        #mycursor = mydb.cursor()
        mycursor.execute("SELECT Contraseña FROM Usuarios_sistema \
        WHERE Nickname='%s';" % (usuario_introducido))
        respuesta_bd = mycursor.fetchall()
        if respuesta_bd:
            if respuesta_bd[0][0] == contrasenia_introducida:
                respuesta_bd = "Aprobado"

        print("Acceso", respuesta_bd, "del usuario", usuario_introducido)
        if respuesta_bd != "Aprobado":
            self.alerta_acceso.setText("Usuario y/o contraseña erróneo")
        else:
            self.punto_de_venta() # Apertura de siguiente ventana

    # Gestión de clase para el Qt
    def punto_de_venta(self):
        self.ventana = Punto_de_venta()
        self.ventana.show()
        self.hide()


# Ejecución de módulo principal
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = acceso_punto_de_venta()
    GUI.show()
    sys.exit(app.exec_())