from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Item_Instancia, Update_II
from typing import List, Optional


router = APIRouter()

@router.post("/iitem")
async def criar_itemc(ii: Item_Instancia) :
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO iitem (id_instancia, status, data_criacao, id_catalogo) VALUES(%s,%s,%s,%s)",
            (ii.id_instancia, ii.status, ii.data_criacao, ii.id_catalogo )
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar um Item_Instancia {e}")
    
    finally:
        cur.close()
        conn.close()
    return {"msg:" "Item_Instancia criado com sucesso"}