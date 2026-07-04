import psycopg2

conn = None
cursor = None

def get_connection():
    return psycopg2.connect (
        dbname='ITEMNEXUS',
        user='postgres',
        password='marianesobral123',
        host='localhost',
        port='5432')
    
cursor = conn.cursor()

  
cursor.execute("""
        CREATE TABLE IF NOT EXISTS DONO(
            id_dono INT PRIMARY KEY,
            tipo VARCHAR(20) NOT NULL,
            ativo BOOL NOT NULL DEFAULT TRUE,
            data_inativacao TIMESTAMP,

            CONSTRAINT checar_tipo
                CHECK (tipo IN ('JOGADOR', 'GUILDA')),

            CONSTRAINT verificar_inativacao
                CHECK (
                    (ativo = TRUE AND data_inativacao IS NULL)
                    OR
                    (ativo = FALSE AND data_inativacao IS NOT NULL)
                )
        );
    """)
conn.commit()

    
dados_donos_guilda = [(i, 'GUILDA', True, None) for i in range(1, 11)]


dados_donos_jogador = [(i, 'JOGADOR', True, None) for i in range(101, 111)]

cursor.executemany(
        "INSERT INTO DONO (id_dono, tipo, ativo, data_inativacao) VALUES (%s, %s, %s, %s)",
        dados_donos_guilda + dados_donos_jogador
    )
conn.commit()

cursor.execute("SELECT * FROM DONO")
print("=== DONO ===")
for linha in cursor.fetchall():
        print(linha)


cursor.execute("""
        CREATE TABLE IF NOT EXISTS GUILDA(
            id_dono INT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            data_criacao TIMESTAMP NOT NULL,

            FOREIGN KEY (id_dono)
                REFERENCES DONO (id_dono)
                ON DELETE CASCADE
        );
    """)
conn.commit()

  
dados_guilda = [
        (1, 'Ordem Fênix', '2023-01-15 10:00:00'),
        (2, 'Legião Sombria', '2023-02-20 14:30:00'),
        (3, 'Guardiões Trono', '2023-03-10 08:45:00'),
        (4, 'Aliança Ferro', '2023-04-05 16:20:00'),
        (5, 'Clã do Lobo', '2023-05-12 11:00:00'),
        (6, 'Irmandade Dragão', '2023-06-18 09:30:00'),
        (7, 'Cavaleiros Aurora', '2023-07-22 13:15:00'),
        (8, 'Sentinela Caos', '2023-08-30 10:45:00'),
        (9, 'Mão da Justiça', '2023-09-14 15:00:00'),
        (10, 'Filhos Trovão', '2023-10-01 12:30:00'),
    ]

cursor.executemany(
        "INSERT INTO GUILDA (id_dono, nome, data_criacao) VALUES (%s, %s, %s)",
        dados_guilda
    )
conn.commit()

cursor.execute("SELECT * FROM GUILDA")
print("\n=== GUILDA ===")
for linha in cursor.fetchall():
        print(linha)


cursor.execute("""
        CREATE TABLE IF NOT EXISTS JOGADOR(
            id_dono INT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL UNIQUE,
            id_guilda INT,
            cargo VARCHAR(20),

            FOREIGN KEY (id_dono)
                REFERENCES DONO (id_dono)
                ON DELETE CASCADE,

            FOREIGN KEY (id_guilda)
                REFERENCES GUILDA (id_dono)
                ON DELETE SET NULL,

            CONSTRAINT cargo_valido
                CHECK (cargo IN ('LIDER', 'OFICIAL', 'MEMBRO'))
        );
    """)
conn.commit()


dados_jogador = [
        (101, 'Legolas', 'legolas@email.com', 1, 'OFICIAL'),
        (102, 'Arthas', 'arthas@email.com', 2, 'LIDER'),
        (103, 'Merlin', 'merlin@email.com', 3, 'LIDER'),
        (104, 'Xena', 'xena@email.com', 4, 'OFICIAL'),
        (105, 'Gandalf', 'gandalf@email.com', 5, 'LIDER'),
        (106, 'Aragorn', 'aragorn@email.com', 6, 'MEMBRO'),
        (107, 'Frodo', 'frodo@email.com', 7, 'MEMBRO'),
        (108, 'Saruman', 'saruman@email.com', 8, 'LIDER'),
        (109, 'Thrall', 'thrall@email.com', 9, 'OFICIAL'),
        (110, 'Jaina', 'jaina@email.com', 10, 'LIDER'),
    ]

cursor.executemany(
        "INSERT INTO JOGADOR (id_dono, nome, email, id_guilda, cargo) VALUES (%s, %s, %s, %s, %s)",
        dados_jogador
    )
conn.commit()

cursor.execute("SELECT * FROM JOGADOR")
print("\n=== JOGADOR ===")
for linha in cursor.fetchall():
        print(linha)



   
        cursor.close()
  
        conn.close()
      