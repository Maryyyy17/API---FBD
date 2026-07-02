from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Guilda, Update_Guilda
from typing import List, Optional


router = APIRouter()

@router.post("/guilda")
async def criar_itemc(gld: Guilda) :
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