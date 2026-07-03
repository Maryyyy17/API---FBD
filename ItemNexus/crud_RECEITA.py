from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Receita, UpdateReceita
from typing import List, Optional


router = APIRouter()

@router.post("/receita")
async def criar_itemc(rct: Receita ) :
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO receita (id, nome, id_resultado) VALUES(%s,%s,%s)",
            (rct.id, rct.nome, rct.id_resultado )
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar uma Receita {e}")
    
    finally:
        cur.close()
        conn.close()
    return {"msg:" "Receita criado com sucesso"}


@router.get("/receita", response_model = List[Receita])
async def listar_receita():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, id_resultado FROM Receita ")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        Receita(
            id = i[0], nome = i[1], id_resultado = i[2]
        ) for i in rows
    ]


@router.get("/receita/{id}", response_model = Receita)
async def get_receita(id : int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, id_resultado FROM Receita WHERE id = %s", (id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Receita( id = row[0], nome = row[1], id_resultado = row[2])
    raise HTTPException (404, "Receita não encontrada")


@router.patch("/receita/{id}")
async def att_receita_parcial(id: int, rct: UpdateReceita):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM Receita WHERE id = %s", (id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Departamento não encontrado")
    fields = []
    values = []
    for campo, valor in rct.dict(exclude_unset = True).items():
        fields.append(f"{campo} = %s")
        values.append(valor)

    if not fields:
        cur.close()
        conn.close()
        raise HTTPException (400, "Nenhum campo informado para atualização")
    values.append(id)
    try:
        cur.execute("UPDATE Receita SET {', '.join(fields)} WHERE dnumero=%s", values)
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    
    finally:
        cur.close()
        conn.close()

    return {"msg": "Receita Atualizada"}


@router.delete("/receita/{id}")
async def deletar_receita(id:int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Receita WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Receita removida"}
