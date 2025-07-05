import cv2
from tkinter import filedialog, Tk

def select_image():
    root = Tk()
    root.withdraw()  # Скрыть главное окно Tkinter
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    root.destroy()
    if file_path:
        image = cv2.imread(file_path)
        if image is None:
            print("Ошибка при загрузке изображения.")
            return None
        print(f"Изображение загружено: {file_path}")
        return image
    else:
        print("Файл изображения не выбран.")
        return None

def capture_from_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось открыть камеру.")
        return None

    print("Нажмите 'Пробел' для захвата, 'Esc' для выхода без захвата.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка при получении изображения с камеры.")
            break

        cv2.imshow("Webcam - Press 'Space' to Capture", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Esc
            print("Захват отменен.")
            break
        elif key == 32:  # Space
            cv2.destroyAllWindows()
            cap.release()
            print("Изображение успешно захвачено с камеры.")
            return frame

    cap.release()
    cv2.destroyAllWindows()
    return None

def show_image(image, window_name="Image"):
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_channel(image, channel):
    channels = cv2.split(image)
    if channel == "R":
        blank = cv2.merge([channels[2], channels[2], channels[2]])
        show_image(blank, "Red Channel")
    elif channel == "G":
        blank = cv2.merge([channels[1], channels[1], channels[1]])
        show_image(blank, "Green Channel")
    elif channel == "B":
        blank = cv2.merge([channels[0], channels[0], channels[0]])
        show_image(blank, "Blue Channel")
    else:
        print("Неверный канал. Используйте R, G или B.")

def convert_to_grayscale(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def rotate_image(image, angle):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def draw_rectangle(image, x1, y1, x2, y2):
    img_copy = image.copy()
    cv2.rectangle(img_copy, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Синий цвет в BGR
    return img_copy
