create table catalogo_sintoma(
	id_sintoma serial not null primary key,
	nombre_sintoma varchar(40) not null,
	is_hipoglucemia boolean not null,
	is_tipo_sintoma_hipoglucemia varchar(40) null,
	is_activo boolean not null
)

INSERT INTO catalogo_sintoma (
	nombre_sintoma,
	is_hipoglucemia,
	is_activo
) VALUES
(
	'Necesidad de comer',
	False,
	True
)
select * from catalogo_sintoma where is_tipo_sintoma_hipoglucemia is not null
update catalogo_sintoma set is_activo = False
where id_sintoma=17

create table catalogo_intensidad(
	id_intensidad serial not null primary key,
	nombre_intensidad varchar(40) not null,
	is_activo boolean not null

)

insert into catalogo_intensidad (
	nombre_intensidad,
	is_activo
)values(
	'Mucho',
	True
)
select * from catalogo_intensidad

create table relacion_sintoma_intensidad(
	id_sintoma_intensidad_cat serial not null primary key,
	sintoma_id int not null,
	intensidad_id int not null,
	is_activo boolean not null,
	constraint fk_sintoma FOREIGN KEY (sintoma_id) REFERENCES catalogo_sintoma (id_sintoma),
	constraint fk_intensidad FOREIGN KEY (intensidad_id) REFERENCES catalogo_intensidad (id_intensidad)
)
SELECT * FROM fn_insertar_relacion_sintoma_intensidad()
select * from relacion_sintoma_intensidad
CREATE VIEW catalogo_sintoma_intensidad_view AS
SELECT 
	rsi.id_sintoma_intensidad_cat as id_intensidad,
	ci.nombre_intensidad as intensidad,
	cs.id_sintoma,
	cs.nombre_sintoma as sintoma
FROM relacion_sintoma_intensidad rsi
INNER JOIN catalogo_intensidad ci on rsi.intensidad_id=ci.id_intensidad
INNER JOIN catalogo_sintoma cs on rsi.sintoma_id = cs.id_sintoma
where rsi.is_activo = True and ci.is_activo = True and cs.is_activo=True
ORDER BY rsi.id_sintoma_intensidad_cat ASC
CREATE OR REPLACE FUNCTION fn_catalogo_sintoma_intensidad()
returns table (
	id_intensidad INTEGER,
	intensidad VARCHAR(40),
	id_sintoma INTEGER,
	sintoma varchar(40)
) as $$
BEGIN
	RETURN QUERY
	SELECT 
		iv.id_intensidad,
		iv.intensidad,
		iv.id_sintoma,
		iv.sintoma
	FROM catalogo_sintoma_intensidad_view iv;
END;
$$ LANGUAGE plpgsql;

select * from fn_catalogo_sintoma_intensidad()

SELECT 
	*
FROM relacion_sintoma_intensidad rsi
INNER JOIN catalogo_intensidad ci on rsi.intensidad_id=ci.id_intensidad
INNER JOIN catalogo_sintoma cs on rsi.sintoma_id = cs.id_sintoma
where rsi.is_activo = True and ci.is_activo = True and cs.is_activo=True

select * from registro_glucosa


ALTER TABLE registro_glucosa
ADD COLUMN id_intensidad_vision INT
   CONSTRAINT fk_intensidad_vision 
   REFERENCES relacion_sintoma_intensidad (id_sintoma_intensidad_cat);
select * from catalogo_sintoma

update registro_glucosa set id_intensidad_vision = 61;
select id_sintoma_intensidad_cat from relacion_sintoma_intensidad
where intensidad_id=1 and is_activo = True


update registro_glucosa set 

	id_intensidad_palpitacion = 7
	

where id =21;
select * from registro_glucosa ORDER BY id ASC
SELECT 
	rsi.id_sintoma_intensidad_cat as id_intensidad,
	ci.nombre_intensidad as intensidad,
	cs.id_sintoma,
	cs.nombre_sintoma as sintoma
FROM relacion_sintoma_intensidad rsi
INNER JOIN catalogo_intensidad ci on rsi.intensidad_id=ci.id_intensidad
INNER JOIN catalogo_sintoma cs on rsi.sintoma_id = cs.id_sintoma
where rsi.is_activo = True and ci.is_activo = True and cs.is_activo=True
and ci.id_intensidad = 1
ORDER BY rsi.id_sintoma_intensidad_cat ASC

CREATE OR REPLACE FUNCTION fn_ins_glucose_record(
   p_nivel_glucosa INTEGER,
   p_id_toma_muestra INTEGER,
   p_id_actividad_fisica INTEGER,
   p_id_usuario INTEGER,
   p_id_intensidad_temblor INTEGER,
   p_id_intensidad_palpitacion INTEGER,
   p_id_intensidad_sudoracion INTEGER,
   p_id_intensidad_hambre INTEGER,
   p_id_intensidad_palidez INTEGER,
   p_id_intensidad_fatiga INTEGER,
   p_id_intensidad_dolor_cabeza INTEGER,
   p_id_intensidad_f_atencion INTEGER,
   p_id_intensidad_habla INTEGER,
   p_id_intensidad_incoordinacion INTEGER,
   p_id_intensidad_convulsion INTEGER,
   p_id_intensidad_confusion INTEGER,
   p_id_intensidad_humor INTEGER,
   p_id_intensidad_orinar INTEGER,
   p_id_intensidad_agua INTEGER,
   p_id_intensidad_vision INTEGER
)
RETURNS TEXT
LANGUAGE plpgsql
AS $BODY$
DECLARE
   id_insercion INTEGER;
   mensaje TEXT;
BEGIN
   -- Insertar registro de glucosa
   INSERT INTO registro_glucosa (
       fecha_toma,
       hora_toma,
       nivel_glucosa,
       id_toma_muestra,
       id_actividad_fisica,
       id_usuario,
       activo,
       id_intensidad_temblor,
       id_intensidad_palpitacion,
       id_intensidad_sudoracion,
       id_intensidad_hambre,
       id_intensidad_palidez,
       id_intensidad_fatiga,
       id_intensidad_dolor_cabeza,
       id_intensidad_f_atencion,
       id_intensidad_habla,
       id_intensidad_incoordinacion,
       id_intensidad_convulsion,
       id_intensidad_confusion,
       id_intensidad_humor,
       id_intensidad_orinar,
       id_intensidad_agua,
       id_intensidad_vision
   )
   VALUES (
       NOW()::DATE,
       NOW()::TIME,
       p_nivel_glucosa,
       p_id_toma_muestra,
       p_id_actividad_fisica,
       p_id_usuario,
       TRUE,
       p_id_intensidad_temblor,
       p_id_intensidad_palpitacion,
       p_id_intensidad_sudoracion,
       p_id_intensidad_hambre,
       p_id_intensidad_palidez,
       p_id_intensidad_fatiga,
       p_id_intensidad_dolor_cabeza,
       p_id_intensidad_f_atencion,
       p_id_intensidad_habla,
       p_id_intensidad_incoordinacion,
       p_id_intensidad_convulsion,
       p_id_intensidad_confusion,
       p_id_intensidad_humor,
       p_id_intensidad_orinar,
       p_id_intensidad_agua,
       p_id_intensidad_vision
   )
   RETURNING id INTO id_insercion;
  
   -- Construir mensaje de éxito
   mensaje := format('Tu registro ha sido almacenado exitosamente!! #%s', id_insercion);
  
   RETURN mensaje;
  
EXCEPTION
   WHEN OTHERS THEN
       -- Retornar mensaje de error con detalles
       RAISE EXCEPTION 'Falló la inserción: %', SQLERRM;
END;
$BODY$;

CREATE TABLE seguridad_usuario(
	id_seguridad_usuario serial primary key not null,
	nombre_usuario varchar(100) not null,
	contrasenia varchar(255) not null,
	email varchar(255) not null,
	fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP not null,
	fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP null,
	ultimo_acceso TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP null,
	is_activo boolean default True,
	catalogo_usuario_id int not null,
	constraint fk_usuario_seguridad FOREIGN KEY (catalogo_usuario_id) REFERENCES catalogo_usuario (id)
)
insert into seguridad_usuario (
nombre_usuario,
contrasenia,
email,
catalogo_usuario_id

)
values(
'araceli',
'12345',
'bb@gmail.com',
1
)
select * from seguridad_usuario

-- ============================================
-- PROCEDIMIENTOS ALMACENADOS PARA AUTENTICACIÓN
-- PostgreSQL Functions para Login Seguro
-- ============================================


-- ============================================
-- FUNCIÓN: validate_login
-- Valida credenciales y retorna datos del usuario
-- NO retorna la contraseña por seguridad
-- ============================================
CREATE OR REPLACE FUNCTION validate_login(
   p_username VARCHAR,
   p_password VARCHAR
)
RETURNS TABLE(
   is_valid BOOLEAN,
   user_id INTEGER,
   username VARCHAR,
   name VARCHAR,
   ape_pat VARCHAR,
   ape_mat VARCHAR,
   email VARCHAR,
   message VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
   -- Buscar usuario activo con las credenciales
   RETURN QUERY
   SELECT
       TRUE AS is_valid,
	   u.catalogo_usuario_id,
	   u.nombre_usuario,
       cu.nombre,
	   cu.apellido_paterno,
	   cu.apellido_materno,
	   u.email,
       'Login exitoso'::VARCHAR AS message
   FROM seguridad_usuario u
   INNER JOIN catalogo_usuario cu ON u.catalogo_usuario_id = cu.id
   WHERE u.nombre_usuario = p_username
     AND u.contrasenia = p_password  -- Temporal: comparación texto plano
     AND u.is_activo = TRUE
   LIMIT 1;
  
   -- Si no se encontró usuario, retornar registro inválido
   IF NOT FOUND THEN
       RETURN QUERY
       SELECT
           FALSE AS is_valid,
           NULL::INTEGER AS user_id,
           NULL::VARCHAR AS username,
           NULL::VARCHAR AS name,
		   NULL::VARCHAR AS ape_pat,
   		   NULL::VARCHAR AS ape_mat,
           NULL::VARCHAR AS email,
           'Credenciales inválidas'::VARCHAR AS message;
   END IF;
END;
$$;


-- ============================================
-- COMENTARIO
-- ============================================
COMMENT ON FUNCTION validate_login(VARCHAR, VARCHAR) IS
'Valida credenciales de login sin exponer la contraseña. Retorna información del usuario si es válido.';


SELECT * FROM validate_login(
   'araceli',
   '12345'
)









