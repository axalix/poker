--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.5
-- Dumped by pg_dump version 9.6.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: users; Type: TABLE; Schema: public; Owner: sitetaker
--

CREATE TABLE users (
    id bigint NOT NULL,
    first_name character varying(128) NOT NULL,
    last_name character varying(128) NOT NULL
);


ALTER TABLE users OWNER TO sitetaker;


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: sitetaker
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO sitetaker;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sitetaker
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: sitetaker
--

COPY users (id, first_name, last_name) FROM stdin;
1	Roy	Park
2	Emmett	White
3	Johnnie	Harris
4	Phyllis	Daniel
5	Beth	Rodriguez
6	Alonzo	Pittman
7	Lorene	Carson
\.




--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: sitetaker
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

