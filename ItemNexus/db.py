import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="guilda",
        user="postgres",
        password="marianesobral123",
        host="localhost"
        )
import psycopg2
# Conectar ao banco de dados
try:
    conn = psycopg2.connect(
        dbname='exemplo',
        user='seu_usuario',
        password='sua_senha',
        host='localhost',
        port='5432'
        )
    cursor = conn.cursor()


# Criar tabela
    cursor.execute ("""
       CREATE table DONO(
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
 
    """)

    cursor.execute (""""
    create table ITEM_CATALOGO(
	id_item_catalogo int primary key,
	nome varchar (30) not null,
	raridade varchar (10) not null,
	descricao varchar (200) not null,
	is_exclusivo bool not null,

	constraint checar_raridade
	check (raridade in (
'COMUM',
'RARO',
'EPICO',
'LENDARIO',
'EXCLUSIVO')),

	constraint exclusividade
check (
(raridade = 'EXCLUSIVO' and is_exclusivo = true)
or
(raridade <> 'EXCLUSIVO' and is_exclusivo = false))
);         
                    
                    """)
    
    cursor.execute ("""
        create table RECEITA(
	id_receita int primary key,
	nome varchar (30) not null,
	id_resultado int not null,

foreign key (id_resultado)
references ITEM_CATALOGO(id_item_catalogo)
	on delete restrict	
);

        """)

    cursor.execute ("""
        create table ITEM_INSTANCIA(
	id_instancia int primary key,
	status varchar (30) not null,
	data_criacao timestamp not null,
	id_catalogo int not null,
	
	foreign key (id_catalogo)
	references ITEM_CATALOGO(id_item_catalogo)
	on delete cascade,

	constraint status_do_item
	check (status in (
'ATIVO',
'DESTRUIDO',
'FUNDIDO'))
);
    """)

    cursor.execute ("""
        create table GUILDA(
	id_dono int primary key,
	nome varchar (20) not null,
	data_criacao timestamp not null,
	
	foreign key (id_dono)
	references DONO (id_dono)
	on delete cascade
);

        """)
    

    cursor.execute ("""
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

        """)
    

    cursor.execute ("""
        create table POSSE(
	id_posse int primary key,
	data_inicio timestamp not null,
	data_fim timestamp,
	dono int not null,
	instancia int not null,
	
	foreign key (dono)
	references DONO (id_dono)
	on delete restrict,
	
	foreign key (instancia)
	references ITEM_INSTANCIA (id_instancia)
	on delete cascade,

	constraint posse_valida
check (data_fim is null or data_fim > data_inicio)
);
        """)

    cursor.execute ("""
        create table USA(
	id_receita int not null,
    	id_item_catalogo int not null,
    	quantidade int not null,

	primary key (id_receita, id_item_catalogo),

	foreign key (id_receita)
    	references RECEITA (id_receita)
    	on delete cascade,
	
	foreign key (id_item_catalogo)
	references ITEM_CATALOGO (id_item_catalogo)
	on delete restrict,

	constraint quantidade_positiva
check (quantidade > 0) 
);
        """)
    

    cursor.execute ("""
        create table LEILAO(
	id_leilao int primary key,
	preco_inicial numeric (8,2) not null,
	data_inicio timestamp not null,
	data_fim timestamp,
	status varchar (20) not null default 'AGENDADO',
	id_instancia int not null,

	foreign key (id_instancia)
	references ITEM_INSTANCIA (id_instancia)
	on delete restrict,

	constraint status_invalido
	check (status in (
'AGENDADO',
		'ATIVO',
		'FINALIZADO',
		'CANCELADO',
		'SEM_LANCES',
		'ARREMATADO',
		'EXPIRADO',
		'SUSPENSO',
		'INVALIDO')),

	constraint nao_termina_antes_de_comecar
	check (data_fim is null or data_fim > data_inicio),

	constraint preco_positivo
check (preco_inicial > 0) 
);

create unique index item_em_apenas_um_leilao
on LEILAO (id_instancia)
where status = 'ATIVO';
        """)
    

    cursor.execute (""""
        create table LANCE(
	id_lance int primary key,
	valor numeric (15,2) not null,
	data_lance timestamp not null,
	id_dono int not null,
	id_leilao int not null,

	foreign key (id_dono)
	references DONO (id_dono)
	on delete restrict,

	foreign key (id_leilao)
	references LEILAO (id_leilao)
	on delete cascade,

	constraint valor_lance
check (valor > 0) 
); 
                    """)

























# Inserir dados
cursor.execute('INSERT INTO alunos (nome) VALUES (%s)', ('Maria',))
cursor.execute('INSERT INTO alunos (nome) VALUES (%s)', ('João',))
conn.commit()
except Exception as e:
conn.rollback()
print(f'Erro ao executar operações no banco de dados: {e}')

# Consultar dados
cursor.execute('SELECT * FROM alunos')
resultados = cursor.fetchall()
for linha in resultados:
print(linha)
except Exception as e:
print(f'Erro ao conectar ao banco de dados: {e}')
finally:
# Fechar conexões
if cursor:
cursor.close()
if conn:
conn.close()