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
    return {"msg": "Dono criado com sucesso"}



@router.get("/dono", response_model = List[Dono])
async def listar_dono():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_dono, tipo, ativo, data_inativacao FROM Dono")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        Dono(id_dono = i[0], tipo = i[1], ativo = i[2], data_inativacao = i[3]

        ) for i in rows
    ]



@router.get("/dono/{id_dono}")
async def get_dono(id_dono: int) :
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id_dono, tipo, ativo, data_inativacao FROM Dono WHERE id_dono=%s",(id_dono,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return Dono(id_dono = row[0], tipo = row[1], ativo = row[2], data_inativacao = row[3])
    raise HTTPException(404, f"Dono não encontrado")



@router.put("/dono/{id_dono}")
async def att_dono(id_dono: int, dn: Update_Dono):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id_dono FROM Dono WHERE id_dono = %s", (id_dono,) 
    )

    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, f"Dono não encontrado")
    
    fields = []
    values = []

    for campo, valor in dn.dict(exclude_unset= True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)


    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado na atualização")
    
    try:
        cur.execute(
            f"UPDATE dono SET {','.join(fields)} WHERE id_dono=%s", values + [id_dono]
        )
        conn.commit()


    except Exception as e:
        conn.rollback()
        raise HTTPException (400, f"Erro ao atualizar departamento {e}")
    

    finally:
        cur.close()
        conn.close()

    return {"msg": "Departamento atualizado"}



@router.delete("/dono/{id_dono}")
async def deletar_dono(id_dono: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM DONO WHERE id_dono = %s", (id_dono,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Dono removido"}
