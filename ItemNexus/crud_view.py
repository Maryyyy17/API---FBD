from fastapi import APIRouter, HTTPException
from db import get_connection
from models import RelatorioJogador
from typing import List

router = APIRouter()


@router.get("/view/jogadores", response_model=List[RelatorioJogador])
async def listar_relatorio_jogadores():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                id_jogador,
                nome_jogador,
                email_jogador,
                cargo_jogador,
                jogador_ativo,
                data_inativacao_jogador,
                id_guilda,
                nome_guilda,
                data_criacao_guilda
            FROM vw_jogadores_completo
        """)
        rows = cur.fetchall()

    except Exception as e:
        raise HTTPException(400, f"Erro ao consultar relatório de jogadores: {e}")

    finally:
        cur.close()
        conn.close()

    return [
        RelatorioJogador(
            id_jogador=r[0],
            nome_jogador=r[1],
            email_jogador=r[2],
            cargo_jogador=r[3],
            jogador_ativo=r[4],
            data_inativacao_jogador=r[5],
            id_guilda=r[6],
            nome_guilda=r[7],
            data_criacao_guilda=r[8],
        )
        for r in rows
    ]


@router.get("/relatorio/jogadores/{id_jogador}", response_model=RelatorioJogador)
async def get_relatorio_jogador(id_jogador: int):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                id_jogador,
                nome_jogador,
                email_jogador,
                cargo_jogador,
                jogador_ativo,
                data_inativacao_jogador,
                id_guilda,
                nome_guilda,
                data_criacao_guilda
            FROM vw_jogadores_completo
            WHERE id_jogador = %s
        """, (id_jogador,))
        row = cur.fetchone()

    except Exception as e:
        raise HTTPException(400, f"Erro ao consultar relatório do jogador: {e}")

    finally:
        cur.close()
        conn.close()

    if row:
        return RelatorioJogador(
            id_jogador=row[0],
            nome_jogador=row[1],
            email_jogador=row[2],
            cargo_jogador=row[3],
            jogador_ativo=row[4],
            data_inativacao_jogador=row[5],
            id_guilda=row[6],
            nome_guilda=row[7],
            data_criacao_guilda=row[8],
        )
    raise HTTPException(404, "Jogador não encontrado no relatório")