--
-- PostgreSQL database dump
--

-- Dumped from database version 14.17 (Homebrew)
-- Dumped by pg_dump version 14.17 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: autores; Type: TABLE; Schema: public; Owner: adrianfloresvillatoro
--

CREATE TABLE public.autores (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    nacionalidad character varying(50),
    fecha_nacimiento date
);


ALTER TABLE public.autores OWNER TO adrianfloresvillatoro;

--
-- Name: autores_id_seq; Type: SEQUENCE; Schema: public; Owner: adrianfloresvillatoro
--

CREATE SEQUENCE public.autores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.autores_id_seq OWNER TO adrianfloresvillatoro;

--
-- Name: autores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adrianfloresvillatoro
--

ALTER SEQUENCE public.autores_id_seq OWNED BY public.autores.id;


--
-- Name: clientes; Type: TABLE; Schema: public; Owner: adrianfloresvillatoro
--

CREATE TABLE public.clientes (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    email character varying(100),
    telefono character varying(20),
    ciudad character varying(100)
);


ALTER TABLE public.clientes OWNER TO adrianfloresvillatoro;

--
-- Name: clientes_id_seq; Type: SEQUENCE; Schema: public; Owner: adrianfloresvillatoro
--

CREATE SEQUENCE public.clientes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clientes_id_seq OWNER TO adrianfloresvillatoro;

--
-- Name: clientes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adrianfloresvillatoro
--

ALTER SEQUENCE public.clientes_id_seq OWNED BY public.clientes.id;


--
-- Name: libroautor; Type: TABLE; Schema: public; Owner: adrianfloresvillatoro
--

CREATE TABLE public.libroautor (
    libro_id integer NOT NULL,
    autor_id integer NOT NULL,
    es_autor_principal boolean DEFAULT false
);


ALTER TABLE public.libroautor OWNER TO adrianfloresvillatoro;

--
-- Name: libros; Type: TABLE; Schema: public; Owner: adrianfloresvillatoro
--

CREATE TABLE public.libros (
    id integer NOT NULL,
    titulo character varying(200) NOT NULL,
    fecha_publicacion date,
    genero character varying(50)
);


ALTER TABLE public.libros OWNER TO adrianfloresvillatoro;

--
-- Name: libros_id_seq; Type: SEQUENCE; Schema: public; Owner: adrianfloresvillatoro
--

CREATE SEQUENCE public.libros_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.libros_id_seq OWNER TO adrianfloresvillatoro;

--
-- Name: libros_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adrianfloresvillatoro
--

ALTER SEQUENCE public.libros_id_seq OWNED BY public.libros.id;


--
-- Name: ventas; Type: TABLE; Schema: public; Owner: adrianfloresvillatoro
--

CREATE TABLE public.ventas (
    id integer NOT NULL,
    cliente_id integer,
    libro_id integer,
    fecha_venta date,
    cantidad integer NOT NULL,
    precio_unitario numeric(10,2) NOT NULL
);


ALTER TABLE public.ventas OWNER TO adrianfloresvillatoro;

--
-- Name: ventas_id_seq; Type: SEQUENCE; Schema: public; Owner: adrianfloresvillatoro
--

CREATE SEQUENCE public.ventas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ventas_id_seq OWNER TO adrianfloresvillatoro;

--
-- Name: ventas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: adrianfloresvillatoro
--

ALTER SEQUENCE public.ventas_id_seq OWNED BY public.ventas.id;


--
-- Name: autores id; Type: DEFAULT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.autores ALTER COLUMN id SET DEFAULT nextval('public.autores_id_seq'::regclass);


--
-- Name: clientes id; Type: DEFAULT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.clientes ALTER COLUMN id SET DEFAULT nextval('public.clientes_id_seq'::regclass);


--
-- Name: libros id; Type: DEFAULT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.libros ALTER COLUMN id SET DEFAULT nextval('public.libros_id_seq'::regclass);


--
-- Name: ventas id; Type: DEFAULT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.ventas ALTER COLUMN id SET DEFAULT nextval('public.ventas_id_seq'::regclass);


--
-- Data for Name: autores; Type: TABLE DATA; Schema: public; Owner: adrianfloresvillatoro
--

COPY public.autores (id, nombre, apellido, nacionalidad, fecha_nacimiento) FROM stdin;
1	María	González	Argentina	1975-06-12
2	Carlos	Pérez	México	1980-02-24
3	Lucía	Martínez	España	1990-10-05
4	Ana	Torres	Chile	1985-07-19
5	Javier	López	Colombia	1978-12-30
6	Elena	Ramírez	Perú	1982-04-21
7	Sofía	Hernández	Uruguay	1995-03-15
8	Miguel	Silva	Bolivia	1969-11-02
9	Laura	Morales	Paraguay	1988-08-10
10	Tomás	Ruiz	Venezuela	1972-01-28
\.


--
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: adrianfloresvillatoro
--

COPY public.clientes (id, nombre, email, telefono, ciudad) FROM stdin;
1	Andrea Ríos	andrea.rios@mail.com	555-1234	Buenos Aires
2	Pedro Núñez	pedro.nunez@mail.com	555-2345	Santiago
3	Lucía Vega	lucia.vega@mail.com	555-3456	Lima
4	Fernando Díaz	fernando.diaz@mail.com	555-4567	Bogotá
5	Camila Torres	camila.torres@mail.com	555-5678	Quito
6	Santiago Ruiz	santiago.ruiz@mail.com	555-6789	Caracas
7	Natalia López	natalia.lopez@mail.com	555-7890	Asunción
8	Joaquín Morales	joaquin.morales@mail.com	555-8901	La Paz
9	Valentina Gómez	valentina.gomez@mail.com	555-9012	Montevideo
10	Rodrigo Herrera	rodrigo.herrera@mail.com	555-0123	Ciudad de México
\.


--
-- Data for Name: libroautor; Type: TABLE DATA; Schema: public; Owner: adrianfloresvillatoro
--

COPY public.libroautor (libro_id, autor_id, es_autor_principal) FROM stdin;
1	1	t
2	2	t
3	3	t
3	4	f
4	5	t
5	6	t
6	7	t
6	8	f
7	9	t
8	10	t
9	1	t
9	2	f
10	3	t
\.


--
-- Data for Name: libros; Type: TABLE DATA; Schema: public; Owner: adrianfloresvillatoro
--

COPY public.libros (id, titulo, fecha_publicacion, genero) FROM stdin;
1	Introducción a la Filosofía	2020-03-15	Filosofía
2	Historia de América Latina	2018-10-01	Historia
3	Programación en Python	2021-07-20	Tecnología
4	El ensayo académico	2019-05-22	Educación
5	Fundamentos de Sociología	2017-09-10	Sociología
6	Matemáticas Discretas	2022-02-28	Matemáticas
7	Antropología Cultural	2016-06-12	Antropología
8	Teoría Literaria Moderna	2020-11-11	Literatura
9	Física Cuántica Básica	2019-08-18	Ciencia
10	Derecho Constitucional	2023-01-05	Derecho
\.


--
-- Data for Name: ventas; Type: TABLE DATA; Schema: public; Owner: adrianfloresvillatoro
--

COPY public.ventas (id, cliente_id, libro_id, fecha_venta, cantidad, precio_unitario) FROM stdin;
1	1	1	2023-06-01	2	25.00
2	2	2	2023-06-05	1	30.00
3	3	3	2023-06-10	3	40.00
4	4	4	2023-06-15	1	22.50
5	5	5	2023-06-20	2	28.00
6	6	6	2023-06-25	1	35.00
7	7	7	2023-06-30	4	26.50
8	8	8	2023-07-01	2	29.00
9	9	9	2023-07-05	1	32.00
10	10	10	2023-07-10	3	38.00
\.


--
-- Name: autores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: adrianfloresvillatoro
--

SELECT pg_catalog.setval('public.autores_id_seq', 10, true);


--
-- Name: clientes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: adrianfloresvillatoro
--

SELECT pg_catalog.setval('public.clientes_id_seq', 10, true);


--
-- Name: libros_id_seq; Type: SEQUENCE SET; Schema: public; Owner: adrianfloresvillatoro
--

SELECT pg_catalog.setval('public.libros_id_seq', 10, true);


--
-- Name: ventas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: adrianfloresvillatoro
--

SELECT pg_catalog.setval('public.ventas_id_seq', 10, true);


--
-- Name: autores autores_pkey; Type: CONSTRAINT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.autores
    ADD CONSTRAINT autores_pkey PRIMARY KEY (id);


--
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (id);


--
-- Name: libroautor libroautor_pkey; Type: CONSTRAINT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.libroautor
    ADD CONSTRAINT libroautor_pkey PRIMARY KEY (libro_id, autor_id);


--
-- Name: libros libros_pkey; Type: CONSTRAINT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.libros
    ADD CONSTRAINT libros_pkey PRIMARY KEY (id);


--
-- Name: ventas ventas_pkey; Type: CONSTRAINT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_pkey PRIMARY KEY (id);


--
-- Name: libroautor libroautor_autor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.libroautor
    ADD CONSTRAINT libroautor_autor_id_fkey FOREIGN KEY (autor_id) REFERENCES public.autores(id) ON DELETE CASCADE;


--
-- Name: libroautor libroautor_libro_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.libroautor
    ADD CONSTRAINT libroautor_libro_id_fkey FOREIGN KEY (libro_id) REFERENCES public.libros(id) ON DELETE CASCADE;


--
-- Name: ventas ventas_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.clientes(id) ON DELETE SET NULL;


--
-- Name: ventas ventas_libro_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: adrianfloresvillatoro
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_libro_id_fkey FOREIGN KEY (libro_id) REFERENCES public.libros(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

