from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Dono, Update_Dono
from typing import List, Optional


router = APIRouter()

@router.post("/dono")
async def criar_dono(dn: Dono) :
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO dono (id_dono, tipo, ativo, data_inativacao) VALUES(%s,%s,%s,%s)",
            (dn.id_dono, dn.tipo, dn.ativo, dn.data_inativacao)
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar um Dono {e}")
    
    finally:
        cur.close()
        conn.close()
    return {"msg:" "Dono criado com sucesso"}


@router.get("/dono")
async def listar_dono():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id_dono, tipo, ativo, data_inativacao FROM Dono "
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        Dono(
            id_dono = i[0],
            tipo = i[1],
            ativo = i[2],
            data_inativacao = i[3]
        ) for i in rows

    ] 


@router.get("/dono/{id_dono}")
async def listar_dono_by_id(id_dono: int) :
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id_dono, tipo, ativo, data_inativacao FROM Dono WHERE id_dono=%s"
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return Dono(id_dono = i[0], tipo = i[1], ativo = i[2], data_inativacao = i[3])
    raise HTTPException(404, f"Dono não encontrado")



