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