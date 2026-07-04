from pydantic import BaseModel
from typing import Optional
from datetime import date



class Dono(BaseModel):
    id_dono: int
    tipo: str
    ativo: bool
    data_inativacao : Optional[date]

class Update_Dono(BaseModel):
    tipo: str
    ativo: bool
    data_inativacao : Optional[date]



class Item_Catalogo (BaseModel):
    id_item_catalogo: int
    nome:str
    raridade: str
    descricao: str
    is_exclusivo : bool

class Update_IC (BaseModel) :
    nome:str
    raridade: str
    descricao: str
    is_exclusivo : bool



class Receita (BaseModel) :
    id_receita : int
    nome: str
    id_resultado: int

class UpdateReceita (BaseModel):
    nome: str
    id_resultado: int




class Item_Instancia (BaseModel):
    id_instancia: int
    status: str
    data_criacao: date
    id_catalogo: int

class Update_II (BaseModel):
    status: str
    data_criacao: date
    id_catalogo: int




class Guilda(BaseModel):
    id_dono: int
    nome: Optional[str]
    data_criacao: Optional[date]

class Update_Guilda(BaseModel):
    nome:str
    data_criacao: date



class Jogador(BaseModel):
    id_dono: int
    nome: str
    email: str
    id_guilda : int
    cargo: str

class Update_Jogador (BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    id_guilda : Optional[int] = None
    cargo:Optional[str] = None