import pandas as pd
import numpy as np

# Вероятности цветов
colors = ["синий", "зеленый", "красный", "желтый"]
probabilities = [0.50, 0.25, 0.05, 0.20]

# Генерация 100 случайных цветов
np.random.seed(42)  # Для воспроизводимости результатов
random_colors = np.random.choice(colors, size=100, p=probabilities)

# Создание DataFrame
df = pd.DataFrame({"Цвет": random_colors})

# Сохранение в Excel
df.to_excel("colors.xlsx", index=False, engine='openpyxl')