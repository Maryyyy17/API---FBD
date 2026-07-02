# API---FBD

O ItemNexus é um sistema de banco de dados relacional que atua como motor de inventário e painel de auditoria de um MMORPG. Voltado para desenvolvedores e administradores de servidores, o sistema rastreia o ciclo de vida completo de cada item em jogo, com controle de posse, transações e genealogia de criação.
O principal problema que resolve é conciliar o alto volume de dados gerado por itens comuns com a auditoria rigorosa exigida por artefatos únicos. Para isso, conta com dois motores de criação: a forja padrão, que instancia itens a partir de receitas pré-cadastradas, e a fusão exclusiva, que permite sacrificar artefatos de alta raridade para gerar novos registros autônomos no catálogo do servidor.
