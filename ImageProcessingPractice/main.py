import image_utils as iu

def main():
    image = None

    while True:
        print("\n--- МЕНЮ ОПЦИЙ ---")
        print("1. Выбрать изображение из файла")
        print("2. Сделать снимок с веб-камеры")
        print("3. Показать текущее изображение")
        print("4. Показать канал (R/G/B)")
        print("5. Преобразовать изображение в оттенки серого")
        print("6. Повернуть изображение")
        print("7. Нарисовать синий прямоугольник")
        print("8. Выйти из программы")

        opcion = input("Выберите опцию: ")

        if opcion == "1":
            image = iu.select_image()
        elif opcion == "2":
            image = iu.capture_from_webcam()
        elif opcion == "3":
            if image is not None:
                iu.show_image(image, "Current image")
            else:
                print("Изображение не загружено.")
        elif opcion == "4":
            if image is not None:
                canal = input("Введите канал для отображения (R/G/B): ").upper()
                iu.show_channel(image, canal)
            else:
                print("Изображение не загружено.")
        elif opcion == "5":
            if image is not None:
                image = iu.convert_to_grayscale(image)
                iu.show_image(image, "Изображение в оттенках серого")
            else:
                print("Изображение не загружено.")
        elif opcion == "6":
            if image is not None:
                try:
                    angulo = float(input("Введите угол поворота: "))
                    image = iu.rotate_image(image, angulo)
                    iu.show_image(image, f"Изображение повернуто на {angulo} градусов")
                except ValueError:
                    print("Неверный ввод. Введите число для угла.")
            else:
                print("Изображение не загружено.")
        elif opcion == "7":
            if image is not None:
                try:
                    x1 = int(input("Введите координату x1: "))
                    y1 = int(input("Введите координату y1: "))
                    x2 = int(input("Введите координату x2: "))
                    y2 = int(input("Введите координату y2: "))
                    image = iu.draw_rectangle(image, x1, y1, x2, y2)
                    iu.show_image(image, "Изображение с синим прямоугольником")
                except ValueError:
                    print("Неверный ввод. Введите целые числа для координат.")
            else:
                print("Изображение не загружено.")
        elif opcion == "8":
            print("Выход из программы...")
            break
        else:
            print("Неверная опция. Попробуйте снова.")

if __name__ == "__main__":
    main()
