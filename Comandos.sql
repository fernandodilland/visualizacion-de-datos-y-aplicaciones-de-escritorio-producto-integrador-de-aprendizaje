-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS Punto_de_venta;

-- Uso de la base de datos
USE Punto_de_venta;

-- Creación de las tablas dentro de la base de datos
CREATE TABLE almacen
(
  Clave INT NOT NULL,
  Descripcion VARCHAR(25) NOT NULL,
  Direccion VARCHAR(35) NOT NULL,
  Encargado VARCHAR(20) NOT NULL,
  Estatus VARCHAR(25) NOT NULL,
  PRIMARY KEY (Clave)
);

CREATE TABLE linea_de_producto
(
  Clave_linea INT NOT NULL,
  Descripcion VARCHAR(25) NOT NULL,
  Estatus VARCHAR(25) NOT NULL,
  PRIMARY KEY (Clave_linea)
);

CREATE TABLE producto
(
  Clave_producto INT NOT NULL,
  Descripcion VARCHAR(25) NOT NULL,
  Unidad_medida VARCHAR(25) NOT NULL,
  Fecha_ult_compra DATE NOT NULL,
  Fecha_ult_venta DATE NOT NULL,  
  Costo SMALLINT NOT NULL,
  Precio SMALLINT NOT NULL,
  PRIMARY KEY (Clave_producto)
);

CREATE TABLE cliente
(
  Clave_cliente INT NOT NULL,
  Nombre_cliente VARCHAR(25) NOT NULL,
  Direccion VARCHAR(35) NOT NULL,
  Correo VARCHAR(45) NOT NULL,
  Telefono VARCHAR(12) NOT NULL,
  Estatus VARCHAR(25) NOT NULL,
  Limite_credito FLOAT NOT NULL,
  Saldo FLOAT NOT NULL,  
  PRIMARY KEY (Clave_cliente)
);

CREATE TABLE ticket
(
  Numero_ticket INT NOT NULL,
  Fecha DATE NOT NULL,
  Sucursal VARCHAR(25) NOT NULL,
  Importe SMALLINT NOT NULL, 
  PRIMARY KEY (Numero_ticket)
);

CREATE TABLE detalle_ticket
(
  Numero_ticket INT NOT NULL,
  Detalle VARCHAR(25) NOT NULL,
  Producto VARCHAR(25) NOT NULL,
  Cantidad SMALLINT NOT NULL,
  Importe SMALLINT NOT NULL
);

CREATE TABLE movimiento_almacen
(
  Clave_movimiento INT NOT NULL,
  Tipo VARCHAR(25) NOT NULL,
  PRIMARY KEY (Clave_movimiento)
);

CREATE TABLE usuarios_sistema
(
  Clave_usuario INT NOT NULL,
  Nickname VARCHAR(25) NOT NULL,
  Contraseña VARCHAR(25) NOT NULL,
  Nombre VARCHAR(25) NOT NULL,
  Tipo VARCHAR(25) NOT NmysqULL,
  Correo VARCHAR(45) NOT NULL,
  Telefono VARCHAR(12) NOT NULL,
  Estatus VARCHAR(25) NOT NULL, 
  PRIMARY KEY (Clave_usuario)
);
-- Se importan usuarios administradores por defecto
INSERT INTO usuarios_sistema(Clave_usuario,Nickname,Contraseña,Nombre,Tipo,Correo,Telefono,Estatus) 
VALUES ('1','Fernando','123','Fernando Mireles','Administrador','fernando@gmail.com','8118181818','Activo');
INSERT INTO usuarios_sistema(Clave_usuario,Nickname,Contraseña,Nombre,Tipo,Correo,Telefono,Estatus) 
VALUES ('2','Jose','123','Jose Fernando','Administrador','jose@gmail.com','8118181818','Activo');
INSERT INTO usuarios_sistema(Clave_usuario,Nickname,Contraseña,Nombre,Tipo,Correo,Telefono,Estatus) 
VALUES ('3','Miguel','123','Miguel','Administrador','miguel@gmail.com','8118181818','Activo');
INSERT INTO usuarios_sistema(Clave_usuario,Nickname,Contraseña,Nombre,Tipo,Correo,Telefono,Estatus) 
VALUES ('4','Kevin','123','Kevin Ricardo','Administrador','kevin@gmail.com','8118181818','Activo');
INSERT INTO usuarios_sistema(Clave_usuario,Nickname,Contraseña,Nombre,Tipo,Correo,Telefono,Estatus) 
VALUES ('5','Juan','123','Juan De Dios','Administrador','juan@gmail.com','8118181818','Activo'); 
-- Vendedora por defecto
INSERT INTO usuarios_sistema(Clave_usuario,Nickname,Contraseña,Nombre,Tipo,Correo,Telefono,Estatus) 
VALUES ('6','Juanita','123','Juanita García','Vendedor','juanita@gmail.com','8118181818','Activo'); 
-- Cliente por defecto
INSERT INTO cliente(Clave_cliente,Nombre_cliente,Direccion,Correo,Telefono,Estatus,Limite_credito,Saldo) 
VALUES ('1','Arturo Peña','Simón Bolívar 1700, Mitras Centro','arturop@gmail.com','818181818','Activo','1500.20','0'); 
-- Almacen
INSERT INTO almacen(Clave,Descripcion,Direccion,Encargado,Estatus) 
VALUES ('1','Principal','Monterrey','Fernando Mireles','Activo'); 
INSERT INTO almacen(Clave,Descripcion,Direccion,Encargado,Estatus) 
VALUES ('2','Reserva','San Nicolás','Juan de Dios','Activo'); 
-- Movimiento
INSERT INTO movimiento_almacen(Clave_movimiento,Tipo)
VALUES ('1','Venta');
-- Productos
INSERT INTO producto(Clave_producto,Descripcion,Unidad_medida,Fecha_ult_compra,Fecha_ult_venta,Costo,Precio) 
VALUES ('1','Coca Cola 250 ml','ml','2022-05-15','2022-05-15','7','12'); 
INSERT INTO linea_de_producto(Clave_linea,Descripcion,Estatus) 
VALUES ('1','Refresco','Activo');

-- Ver contenidos de las tablas
select * from almacen
select * from cliente
select * from detalle_ticket
select * from linea_de_producto
select * from movimiento_almacen
select * from producto
select * from ticket
select * from usuarios_sistema

SELECT * FROM ticket WHERE Fecha = '2022-05-15';

SELECT dt.Producto, SUM(dt.Cantidad) AS total
FROM ticket as t inner join detalle_ticket as dt
WHERE Sucursal = "Monterrey" 
and t.Numero_ticket = dT.Numero_ticket
group by dt.Producto
order by SUM(dt.Cantidad) Desc;

-- Tendencia de venta de 5 días
SELECT FECHA, IMPORTE
FROM TICKET
WHERE Sucursal = "Monterrey"
order by FECHA ASC;

SELECT FECHA, sum(IMPORTE)
FROM TICKET
WHERE Sucursal = "Monterrey"
group by fecha
order by FECHA ASC;

SELECT FECHA, sum(IMPORTE)
FROM TICKET
WHERE Sucursal = "Monterrey"
group by fecha
order by FECHA ASC limit 5;

SELECT cast(FECHA as char), cast(sum(IMPORTE) as float)
FROM TICKET
WHERE Sucursal = "Monterrey"
group by fecha
order by FECHA ASC limit 5;

SELECT FECHA, IMPORTE
FROM TICKET
order by FECHA ASC


SELECT distinct(t.Importe), dt.Producto FROM ticket as t inner join detalle_ticket as dt WHERE Sucursal = "Monterrey" 
and t.Numero_ticket = dT.Numero_ticket ;

SELECT Descripcion, Costo From Producto;

SELECT Importe FROM ticket WHERE Sucursal = "Monterrey";

SELECT Nombre FROM Usuarios_sistema WHERE Nickname='Jose';

SELECT Limite_credito FROM cliente WHERE Nombre_cliente='Arturo Peña';

SELECT Saldo FROM cliente WHERE Nombre_cliente='Arturo Peña';

SELECT Precio FROM producto WHERE Descripcion='Coca Cola 250 ml';