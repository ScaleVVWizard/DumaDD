import logging
from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel, Field

logger = logging.getLogger("app.items")
router = APIRouter(prefix="/items", tags=["items"])

class Item(BaseModel):
    name: str = Field(..., title="Название", example="Телефон")
    price: float = Field(..., gt=0, title="Цена", example=199.99)
    is_offer: bool | None = Field(None, title="Акционный товар")

fake_db: dict[int, dict] = {1: {"name": "Foo", "price": 50.2}}
_next_id = 2

def _name_exists(name: str, exclude_id: int | None = None) -> bool:
    return any(it["name"].lower() == name.lower() for i, it in fake_db.items() if i != exclude_id)

@router.get("/{item_id}")
def read_item(
    item_id: int = Path(..., title="ID товара", ge=1),
    q: str | None = Query(None, title="Поисковый запрос", max_length=50),
):
    if item_id not in fake_db:
        logger.warning(f"Товар с ID {item_id} не найден")
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item": fake_db[item_id], "q": q}

@router.post("/", response_model=Item, status_code=201)
def create_item(item: Item):
    global _next_id
    if _name_exists(item.name):
        logger.warning(f"Попытка создать дубликат: {item.name}")
        raise HTTPException(status_code=400, detail="Item with this name already exists")
    fake_db[_next_id] = item.model_dump()
    _next_id += 1
    logger.info(f"Создан новый товар: {item.name}")
    return item

@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        logger.warning(f"Попытка обновить несуществующий товар ID {item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    if _name_exists(item.name, exclude_id=item_id):
        raise HTTPException(status_code=400, detail="Item with this name already exists")
    fake_db[item_id] = item.model_dump()
    logger.info(f"Обновлен товар ID {item_id}")
    return item