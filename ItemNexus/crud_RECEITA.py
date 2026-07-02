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