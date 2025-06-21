import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# Настройка страницы
st.set_page_config(page_title="Анализ цветов", page_icon="🎨")
st.title("🎨 Анализ распределения цветов")
st.write("Загрузите Excel-файл с одним столбцом цветов (синий, зеленый, красный, желтый)")

# Цветовая схема
COLOR_MAP = {
    'синий': '#1f77b4',
    'зеленый': '#2ca02c',
    'красный': '#d62728',
    'желтый': '#ffcc00'
}

def process_file(uploaded_file):
    """Обработка загруженного файла"""
    try:
        # Чтение файла
        df = pd.read_excel(uploaded_file)
        
        # Проверка структуры
        if len(df.columns) != 1:
            st.error("Ошибка: Файл должен содержать только один столбец")
            return None
            
        # Обработка данных
        color_col = df.columns[0]
        colors = df[color_col].astype(str).str.strip().str.lower()
        
        return colors
    except Exception as e:
        st.error(f"Ошибка обработки файла: {e}")
        return None

# Загрузка файла
uploaded_file = st.file_uploader("Выберите файл", type=['xlsx', 'xls'])

if uploaded_file is not None:
    # Обработка файла
    colors = process_file(uploaded_file)
    
    if colors is not None:
        # Подсчет цветов
        color_counts = colors.value_counts().reset_index()
        color_counts.columns = ['Цвет', 'Количество']
        
        # Фильтрация цветов
        valid_colors = color_counts[color_counts['Цвет'].isin(COLOR_MAP.keys())]
        invalid_colors = color_counts[~color_counts['Цвет'].isin(COLOR_MAP.keys())]
        
        # Отображение результатов
        st.subheader("Результаты подсчета")
        st.dataframe(valid_colors)
        
        # Предупреждение о недопустимых цветах
        if not invalid_colors.empty:
            st.warning(f"Обнаружены недопустимые цвета: {', '.join(invalid_colors['Цвет'])}")
        
        # Визуализация
        if not valid_colors.empty:
            # Столбчатая диаграмма
            fig_bar = px.bar(
                valid_colors,
                x='Цвет',
                y='Количество',
                color='Цвет',
                color_discrete_map=COLOR_MAP,
                title='Распределение цветов'
            )
            st.plotly_chart(fig_bar)
            
            # Круговой график
            fig_pie = px.pie(
                valid_colors,
                names='Цвет',
                values='Количество',
                color='Цвет',
                color_discrete_map=COLOR_MAP,
                title='Процентное соотношение'
            )
            st.plotly_chart(fig_pie)
            
            # Статистика
            total = valid_colors['Количество'].sum()
            st.write(f"**Всего записей:** {total}")
            for _, row in valid_colors.iterrows():
                percentage = (row['Количество'] / total) * 100
                st.write(f"- {row['Цвет']}: {row['Количество']} ({percentage:.1f}%)")
        else:
            st.warning("Допустимые цвета не найдены")

# Генерация примера файла
st.markdown("---")
st.subheader("Тестирование")
if st.button("Создать пример файла для тестирования"):
    colors_list = list(COLOR_MAP.keys())
    probs = [0.5, 0.25, 0.05, 0.2]
    sample = np.random.choice(colors_list, size=100, p=probs)
    sample_df = pd.DataFrame({"Цвет": sample})
    
    # Создание файла в памяти
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        sample_df.to_excel(writer, index=False)
    
    # Кнопка скачивания
    st.download_button(
        label="📥 Скачать пример файла",
        data=output.getvalue(),
        file_name="sample_colors.xlsx",
        mime="application/vnd.ms-excel"
    )
    
    # Показать предпросмотр
    st.write("Первые 10 строк примера файла:")
    st.dataframe(sample_df.head(10))