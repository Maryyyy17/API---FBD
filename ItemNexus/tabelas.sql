create table DONO(
	id_dono int primary key,
	tipo varchar (20) not null,
	ativo bool not null default true,
data_inativacao timestamp,

	constraint checar_tipo
	check (tipo in ('JOGADOR', 'GUILDA')),

	constraint verificar_inativacao
check (
(ativo = true and data_inativacao is null)
or
(ativo = false and data_inativacao is not null))
);

create table GUILDA(
	id_dono int primary key,
	nome varchar (20) not null,
	data_criacao timestamp not null,
	
	foreign key (id_dono)
	references DONO (id_dono)
	on delete cascade
);

create table JOGADOR(
	id_dono int primary key,
	nome varchar (20) not null,
	email varchar (50) not null unique,
	id_guilda int,
	cargo varchar (20),

	foreign key (id_dono)
	references DONO (id_dono)
	on delete cascade,

	foreign key (id_guilda)
	references GUILDA (id_dono)
	on delete set null,

	constraint cargo_valido
check (cargo in (
    		'LIDER',
'OFICIAL',
'MEMBRO'))
);
