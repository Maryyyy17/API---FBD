from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Guilda, Update_Guilda
from typing import List, Optional


router = APIRouter()

@router.post("/guilda")
async def criar_guilda(gld: Guilda) :
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO guilda (id_dono, nome, data_criacao) VALUES(%s,%s,%s)",
            (gld.id_dono, gld.nom, gld.data_criacao )
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar uma Guilda {e}")
    
    finally:
        cur.close()
        conn.close()
    return {"msg:" "Guilda criado com sucesso"}


@router.get("/guilda", response_model = List[Guilda])
async def listar_guilda():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_dono, nome, data_criacao FROM GUILDA")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        Guilda(
            id_dono =i[0], nome =i[1], data_criacao=i[2]
        ) for i in rows
    ]


@router.get("/guilda/{id_dono}", response_model=Guilda)
async def get_guilda(id_dono : int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_dono, nome, data_criacao FROM GUILDA WHERE id_dono=%s", (id_dono))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Guilda(id_dono =i[0], nome =i[1], data_criacao=i[2])
    raise HTTPException(404, "Guida não encontrada")


@router.patch("/guilda/{id_dono}")
async def att_guilda_parcial(id_dono: int, gld: Update_Guilda):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_dono FROM GUILDA WHERE id_dono=%s", (id_dono,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Guilda não encontrada")
    fields = []
    values = []
    for campo, valor in gld.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    values.append(id_dono)
    try:
        cur.execute(f" UPDATE Guilda SET {', '.join(fields)} WHERE id_dono=%s", values)
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Guilda atualizada"}


@router.delete("/guilda/{id_dono}")
async def deletar_guilda(id_dono: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Guilda WHERE id_dono =%s", (id_dono))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Guilda removida"}