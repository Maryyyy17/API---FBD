from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Item_Catalogo, Update_IC
from typing import List, Optional


router = APIRouter()

@router.post("/itemc")
async def criar_itemc(ic: Item_Catalogo ) :
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO itemc (id_item_catalogo, nome, raridade, descricao, is_exclusive) VALUES(%s,%s,%s,%s,%s)",
            (ic.id_item_catalogo, ic.nome, ic.raridade, ic.descricao, ic.is_exclusive )
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar um Item_Catalogo {e}")
    
    finally:
        cur.close()
        conn.close()
    return {"msg:" "Item_Catalogo criado com sucesso"}