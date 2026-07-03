from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Jogador, Update_Jogador
from typing import List, Optional


router = APIRouter()

@router.post("/jogador")
async def criar_itemc(jog: Jogador) :
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO jogador (id_dono, nome, email, id_guilda, cargo) VALUES(%s,%s,%s,%s,%s)",
            (jog.id_dono, jog.nome, jog.email, jog.id_email, jog.id_guilda )
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar um Jogador {e}")
    
    finally:
        cur.close()
        conn.close()
    return {"msg:" "Jogador criado com sucesso"}


@router.get("/departamento", response_model = List[Jogador])
async def listar_jogador():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(" SELECT id_dono, nome, email, id_guilda, cargo FROM Jogador ")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        Jogador(
            id_dono = i[0], nome = i[1], email =i[2], id_guilda = i[3], cargo = i[4], cargo = i[5]
        ) for i in rows
    ]


@router.get("/jogador/{id_dono}", response_model = Jogador)
async def get_jogador(id_dono: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_dono, nome, email, id_guilda, cargo FROM Jogador WHERE id_dono=%s", (id_dono,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Jogador(id_dono = row[0], nome = row[1], email =row[2], id_guilda = row[3], cargo = row[4], cargo = row[5])
    raise HTTPException(404, "Jogador não encontrado")



@router.patch("/jogador/{id_dono}")
async def att_jogador_parcial(id_dono: int, jog: Update_Jogador):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_dono FROM Jogador WHERE id_dono=%s", (id_dono))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Jogador não encontrado")
    fields = []
    values = []
    for campo, valor in jog.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    values.append(id_dono)
    try:
        cur.execute(f"UPDATE Jogador SET {', '.join(fields)} WHERE id_dono=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Jogador atualizado"}


@router.delete("/jogador/{id_dono}")
async def deletar_jogador(id_dono: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Jogador WHERE id_dono=%s", (id_dono,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Jogador removido"}
    