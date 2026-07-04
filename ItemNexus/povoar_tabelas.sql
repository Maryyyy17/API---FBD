-- IMPORTANTE: rodar depois de criar as tabelas (tabelas.sql)
-- Ordem importa: DONO primeiro (pai), depois GUILDA e JOGADOR (filhos, via FK id_dono)

-- =========================================
-- 1) DONOS do tipo GUILDA (ativos)
-- =========================================
INSERT INTO DONO (id_dono, tipo, ativo, data_inativacao) VALUES
(1, 'GUILDA', true, null),
(2, 'GUILDA', true, null),
(3, 'GUILDA', true, null);

-- =========================================
-- 2) DONOS do tipo JOGADOR (ativos)
-- =========================================
INSERT INTO DONO (id_dono, tipo, ativo, data_inativacao) VALUES
(101, 'JOGADOR', true, null),
(102, 'JOGADOR', true, null),
(103, 'JOGADOR', true, null),
(104, 'JOGADOR', true, null);

-- =========================================
-- 3) Exemplo de DONO inativo (JOGADOR)
-- =========================================
INSERT INTO DONO (id_dono, tipo, ativo, data_inativacao) VALUES
(105, 'JOGADOR', false, '2026-05-10');

-- =========================================
-- 4) GUILDAS
-- =========================================
INSERT INTO GUILDA (id_dono, nome, data_criacao) VALUES
(1, 'Dragões do Norte', '2024-01-15'),
(2, 'Sombra Eterna', '2024-03-20'),
(3, 'Aliança Dourada', '2025-02-10');

-- =========================================
-- 5) JOGADORES
-- =========================================
INSERT INTO JOGADOR (id_dono, nome, email, id_guilda, cargo) VALUES
(101, 'Maria Silva', 'maria@teste.com', 1, 'líder'),
(102, 'João Souza', 'joao@teste.com', 1, 'membro'),
(103, 'Ana Costa', 'ana@teste.com', 2, 'membro'),
(104, 'Pedro Lima', 'pedro@teste.com', 3, 'líder'),
(105, 'Carlos Reis', 'carlos@teste.com', 2, 'membro');
