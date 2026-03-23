import unittest
from restaurant import Order, Dish, Drink, SetMenu


class TestOrder(unittest.TestCase):
    """Класс для тестирования Order"""
    
    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        # Создаем тестовые блюда
        self.borscht = Dish("Борщ", 350.0)
        self.ceasar = Dish("Салат Цезарь", 280.0)
        self.wine = Drink("Красное вино", 600.0, 150, is_alcoholic=True)
        
        # Создаем пустой заказ
        self.order = Order()
    
    # ========== ТЕСТ 1 ==========
    def test_order_creation(self):
        """Проверяем, что новый заказ пустой"""
        self.assertEqual(self.order.get_status(), "создан")
        self.assertEqual(len(self.order.get_items()), 0)
        self.assertEqual(self.order.get_total(), 0.0)
    
    # ========== ТЕСТ 2 ==========
    def test_add_single_item(self):
        """Добавление одного блюда в заказ"""
        self.order.add_item(self.borscht, 2)
        items = self.order.get_items()
        
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0][0], self.borscht)
        self.assertEqual(items[0][1], 2)
    
    # ========== ТЕСТ 3 ==========
    def test_calculate_total(self):
        """Расчет суммы заказа"""
        self.order.add_item(self.borscht, 2)   # 2 * 350 = 700
        self.order.add_item(self.wine, 1)      # 1 * 600 = 600
        self.assertEqual(self.order.get_total(), 1300.0)
    
    # ========== ТЕСТ 4 ==========
    def test_add_unavailable_item(self):
        """Попытка добавить недоступное блюдо"""
        self.borscht.set_availability(False)
        
        with self.assertRaises(ValueError):
            self.order.add_item(self.borscht, 1)
        
        self.assertEqual(len(self.order.get_items()), 0)
    
    # ========== ТЕСТ 5 ==========
    def test_add_zero_quantity(self):
        """Попытка добавить блюдо с нулевым количеством"""
        with self.assertRaises(ValueError):
            self.order.add_item(self.borscht, 0)
    
    # ========== ТЕСТ 6 ==========
    def test_remove_item(self):
        """Удаление блюда из заказа"""
        self.order.add_item(self.borscht, 2)
        self.order.add_item(self.wine, 1)
        
        self.assertEqual(len(self.order.get_items()), 2)
        
        self.order.remove_item(self.borscht)
        
        items = self.order.get_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0][0], self.wine)
    
    # ========== ТЕСТ 7 ==========
    def test_update_status(self):
        """Изменение статуса заказа"""
        self.assertEqual(self.order.get_status(), "создан")
        
        self.order.update_status("готовится")
        self.assertEqual(self.order.get_status(), "готовится")
        
        self.order.update_status("готов")
        self.assertEqual(self.order.get_status(), "готов")


if __name__ == "__main__":
    unittest.main()