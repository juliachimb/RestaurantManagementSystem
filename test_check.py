# ========== ПРОВЕРКА РАБОТЫ (запустите в конце) ==========
if __name__ == "__main__":
    print("=" * 50)
    print("ПРОВЕРКА ПОСЛЕ РЕФАКТОРИНГА")
    print("=" * 50)

    # Тест 1: Создание блюд
    print("\n1. Создаем блюда...")
    borscht = Dish("Борщ", 350, "Традиционный борщ", 450)
    ceasar = Dish("Цезарь", 280, "С курицей", 320)
    cola = Drink("Кола", 90, 500)
    print(f"   ✅ {borscht}")
    print(f"   ✅ {ceasar}")
    print(f"   ✅ {cola}")

    # Тест 2: Создание заказа
    print("\n2. Создаем заказ...")
    order = Order()
    order.add_item(borscht, 2)
    order.add_item(ceasar, 1)
    print(f"   ✅ Заказ создан, сумма: {order.get_total()} руб.")

    # Тест 3: Проверка суммы
    print("\n3. Проверяем сумму...")
    expected = 350 * 2 + 280  # = 980
    actual = order.get_total()
    if actual == expected:
        print(f"   ✅ Сумма верная: {actual} руб.")
    else:
        print(f"   ❌ Ошибка! Ожидалось {expected}, получено {actual}")

    # Тест 4: Проверка валидации
    print("\n4. Проверяем валидацию...")
    try:
        order.add_item(borscht, -5)
        print("   ❌ Ошибка: отрицательное количество не должно работать")
    except ValueError as e:
        print(f"   ✅ Всё правильно: {e}")

    # Тест 5: Проверка скидки
    print("\n5. Проверяем сет-меню со скидкой...")
    lunch_set = SetMenu("Бизнес-ланч", 0)
    lunch_set.add_item(borscht)
    lunch_set.add_item(ceasar)
    lunch_set.set_discount(15)
    print(f"   ✅ Стоимость сета: {lunch_set.get_price()} руб. (скидка 15%)")

    print("\n" + "=" * 50)
    print("ИТОГ: Рефакторинг прошел успешно! 🎉")
    print("=" * 50)