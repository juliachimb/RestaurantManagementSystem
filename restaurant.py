from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Optional


# ========== КОНСТАНТЫ ==========
MIN_QUANTITY = 1
MIN_PRICE = 0
MAX_DISCOUNT = 100
MIN_DISCOUNT = 0


# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
def validate_positive(value, name="Значение", allow_zero=False):
    """Проверяет, что значение больше 0 (или равно 0, если allow_zero=True)"""
    if allow_zero:
        if value < MIN_PRICE:
            raise ValueError(f"{name} не может быть отрицательным, получено {value}")
    else:
        if value <= MIN_PRICE:
            raise ValueError(f"{name} должно быть больше {MIN_PRICE}, получено {value}")


def validate_range(value, min_val, max_val, name="Значение"):
    """Проверяет, что значение в диапазоне"""
    if not (min_val <= value <= max_val):
        raise ValueError(f"{name} должно быть от {min_val} до {max_val}, получено {value}")


# ========== Базовый класс для всех элементов меню ==========
class MenuItem(ABC):
    """Абстрактный класс для всех элементов меню (блюда, напитки, сеты)"""

    def __init__(self, name: str, price: float, allow_zero_price=False):
        validate_positive(price, "Цена", allow_zero=allow_zero_price)
        if not name or not name.strip():
            raise ValueError("Название не может быть пустым")
        self._name = name
        self._price = price
        self._is_available = True

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> float:
        return self._price

    def is_available(self) -> bool:
        return self._is_available

    def set_availability(self, available: bool):
        self._is_available = available

    @abstractmethod
    def get_description(self) -> str:
        pass

    def __str__(self) -> str:
        availability = "доступно" if self._is_available else "недоступно"
        return f"{self._name} --- {self._price} руб. ({availability})"


# ========== Класс Блюдо ==========
class Dish(MenuItem):
    """Класс для блюд"""

    def __init__(self, name: str, price: float, description: str = "", calories: Optional[int] = None):
        super().__init__(name, price, allow_zero_price=False)
        self._description = description
        self._calories = calories

    def get_description(self) -> str:
        desc = self._description
        if self._calories:
            desc += f" ({self._calories} ккал)"
        return desc if desc else "Без описания"

    def set_description(self, description: str):
        self._description = description.strip()

    def set_calories(self, calories: int):
        validate_positive(calories, "Калорийность")
        self._calories = calories


# ========== Класс Напиток ==========
class Drink(MenuItem):
    """Класс для напитков"""

    def __init__(self, name: str, price: float, volume_ml: int, is_alcoholic: bool = False):
        super().__init__(name, price, allow_zero_price=False)
        self._volume_ml = volume_ml
        self._is_alcoholic = is_alcoholic

    def get_description(self) -> str:
        volume_info = f"{self._volume_ml} мл"
        alcohol_info = " (алкогольный)" if self._is_alcoholic else ""
        return volume_info + alcohol_info

    def get_volume(self) -> int:
        return self._volume_ml

    def is_alcoholic(self) -> bool:
        return self._is_alcoholic


# ========== Класс Сет-меню ==========
class SetMenu(MenuItem):
    """Класс для сет-меню (набор из нескольких блюд)"""

    def __init__(self, name: str, base_price: float = 0):
        # Разрешаем нулевую цену для сета, она будет пересчитана
        super().__init__(name, base_price, allow_zero_price=True)
        self._items: List[MenuItem] = []
        self._discount_percent = 0.0

    def add_item(self, item: MenuItem):
        self._items.append(item)
        self._update_price()

    def remove_item(self, item: MenuItem):
        self._items.remove(item)
        self._update_price()

    def set_discount(self, percent: float):
        validate_range(percent, MIN_DISCOUNT, MAX_DISCOUNT, "Скидка")
        self._discount_percent = percent
        self._update_price()

    def _update_price(self):
        """Пересчитывает цену сета на основе блюд и скидки"""
        total = sum(item.get_price() for item in self._items)
        self._price = total * (1 - self._discount_percent / 100)

    def get_price(self) -> float:
        return self._price

    def get_description(self) -> str:
        if not self._items:
            return "Пустой сет"
        items_list = ", ".join(item.get_name() for item in self._items)
        discount_info = f" (скидка {self._discount_percent}%)" if self._discount_percent > 0 else ""
        return f"Состав: {items_list}{discount_info}"

    def get_items(self) -> List[MenuItem]:
        return self._items.copy()


# ========== Класс Заказ ==========
class Order:
    """Класс для заказа"""

    def __init__(self):
        self._items: List[tuple[MenuItem, int]] = []
        self._created_at = datetime.now()
        self._status = "создан"

    def add_item(self, item: MenuItem, quantity: int = 1):
        """Добавляет блюдо в заказ"""
        validate_positive(quantity, "Количество")
        if not item.is_available():
            raise ValueError(f"{item.get_name()} сейчас недоступно")
        self._items.append((item, quantity))

    def remove_item(self, item: MenuItem):
        """Удаляет блюдо из заказа"""
        self._items = [i for i in self._items if i[0] != item]

    def get_total(self) -> float:
        """Рассчитывает итоговую сумму заказа"""
        return sum(item.get_price() * qty for item, qty in self._items)

    def get_items(self) -> List[tuple[MenuItem, int]]:
        """Возвращает копию списка позиций"""
        return self._items.copy()

    def update_status(self, status: str):
        """Обновляет статус заказа"""
        self._status = status

    def get_status(self) -> str:
        """Возвращает текущий статус"""
        return self._status

    def __str__(self) -> str:
        created = self._created_at.strftime('%Y-%m-%d %H:%M')
        lines = [f"Заказ от {created}"]
        for item, qty in self._items:
            item_total = item.get_price() * qty
            lines.append(f"- {item.get_name()} x{qty} --- {item_total} руб.")
        lines.append(f"Итого: {self.get_total()} руб.")
        lines.append(f"Статус: {self._status}")
        return "\n".join(lines)

