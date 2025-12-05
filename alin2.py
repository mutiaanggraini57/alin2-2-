import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr, spearmanr
from PIL import Image, ImageEnhance

# -------------------------------------------------
# TRANSLATIONS (3 languages)
# -------------------------------------------------
translations = {
    "en": {
        "app_title": "Statistical Analysis App",
        "upload_dataset": "Upload your dataset",
        "no_file": "Please upload your survey dataset to start analysis.",
        "select_columns": "Select two numeric columns",
        "select_method": "Select correlation method",
        "pearson": "Pearson",
        "spearman": "Spearman",
        "calculate": "Calculate Correlation",
        "result_title": "Correlation Results ({})",
        "coef": "Correlation Coefficient (r): {:.3f}",
        "p_value": "p-value: {:.4f}",
        "weak": "Weak correlation",
        "moderate": "Moderate correlation",
        "strong": "Strong correlation",
        "positive": "Positive",
        "negative": "Negative",
        "interpretation": "Interpretation: {} – {}",
        "scatter_title": "Scatter Plot with Trendline",
        "photo_section": "Group Photo Processor",
        "upload_photo": "Upload a group photo",
        "rotation": "Rotate",
        "brightness": "Brightness",
        "contrast": "Contrast",
    },
    "id": {
        "app_title": "Aplikasi Analisis Statistik",
        "upload_dataset": "Unggah dataset Anda",
        "no_file": "Silahkan upload file dataset survey Anda untuk mulai analisis.",
        "select_columns": "Pilih dua kolom numerik",
        "select_method": "Pilih metode korelasi",
        "pearson": "Pearson",
        "spearman": "Spearman",
        "calculate": "Hitung Korelasi",
        "result_title": "Hasil Korelasi ({})",
        "coef": "Koefisien Korelasi (r): {:.3f}",
        "p_value": "p-value: {:.4f}",
        "weak": "Korelasi Lemah",
        "moderate": "Korelasi Sedang",
        "strong": "Korelasi Kuat",
        "positive": "Positif",
        "negative": "Negatif",
        "interpretation": "Interpretasi: {} – {}",
        "scatter_title": "Scatter Plot dengan Trendline",
        "photo_section": "Pemrosesan Foto Grup",
        "upload_photo": "Unggah foto grup",
        "rotation": "Rotasi",
        "brightness": "Kecerahan",
        "contrast": "Kontras",
    },
    "cn": {
        "app_title": "统计分析应用",
        "upload_dataset": "上传您的数据集",
        "no_file": "请上传调查数据集以开始分析。",
        "select_columns": "选择两个数值列",
        "select_method": "选择相关性方法",
        "pearson": "皮尔逊",
        "spearman": "斯皮尔曼",
        "calculate": "计算相关性",
        "result_title": "相关结果 ({})",
        "coef": "相关系数 (r): {:.3f}",
        "p_value": "p 值: {:.4f}",
        "weak": "弱相关",
        "moderate": "中等相关",
        "strong": "强相关",
        "positive": "正相关",
        "negative": "负相关",
        "interpretation": "解释: {} – {}",
        "scatter_title": "带趋势线的散点图",
        "photo_section": "小组照片处理",
        "upload_photo": "上传小组照片",
        "rotation": "旋转",
        "brightness": "亮度",
        "contrast": "对比度",
    }
}

# -------------------------------------------------
# LANGUAGE SWITCHER
# -------------------------------------------------
lang = st.sidebar.selectbox("Language", ["en", "id", "cn"])
t = translations[lang]

st.title(t["app_title"])

# -------------------------------------------------
# TABS (Main analysis + Photo processing)
# -------------------------------------------------
tab1, tab2 = st.tabs(["📊 Analysis", "📸 " + t["photo_section"]])

# -------------------------------------------------
# TAB 1 — STATISTICAL ANALYSIS
# -------------------------------------------------
with tab1:
    uploaded = st.file_uploader(t["upload_dataset"], type=["csv", "xlsx"])

    if uploaded is None:
        st.warning(t["no_file"])
    else:
        # Load dataset
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)

        # Filter numeric columns
        numeric_cols = df.select_dtypes(include=["int", "float"]).columns.tolist()

        if len(numeric_cols) < 2:
            st.error("Dataset must contain numeric (Likert-scale) columns!")
        else:
            col1 = st.selectbox(t["select_columns"] + " (1)", numeric_cols)
            col2 = st.selectbox(t["select_columns"] + " (2)", numeric_cols)

            method = st.radio(t["select_method"], [t["pearson"], t["spearman"]])

            if st.button(t["calculate"]):
                x = df[col1]
                y = df[col2]

                if method == t["pearson"]:
                    r, p = pearsonr(x, y)
                    m = "Pearson"
                else:
                    r, p = spearmanr(x, y)
                    m = "Spearman"

                st.subheader(t["result_title"].format(m))
                st.write(t["coef"].format(r))
                st.write(t["p_value"].format(p))

                # Interpretation logic
                direction = t["positive"] if r >= 0 else t["negative"]

                if abs(r) < 0.3:
                    strength = t["weak"]
                elif abs(r) < 0.7:
                    strength = t["moderate"]
                else:
                    strength = t["strong"]

                st.success(t["interpretation"].format(direction, strength))

                # Scatter plot
                fig = px.scatter(df, x=col1, y=col2, trendline="ols",
                                 title=t["scatter_title"])
                st.plotly_chart(fig)


# -------------------------------------------------
# TAB 2 — PHOTO PROCESSOR
# -------------------------------------------------
with tab2:
    img_file = st.file_uploader(t["upload_photo"], type=["jpg", "png", "jpeg"])

    if img_file:
        img = Image.open(img_file)

        # Controls
        rotate_deg = st.slider(t["rotation"], -180, 180, 0)
        brightness_val = st.slider(t["brightness"], 0.5, 2.0, 1.0)
        contrast_val = st.slider(t["contrast"], 0.5, 2.0, 1.0)

        # Processed image
        edited = img.rotate(rotate_deg)
        edited = ImageEnhance.Brightness(edited).enhance(brightness_val)
        edited = ImageEnhance.Contrast(edited).enhance(contrast_val)

        colA, colB = st.columns(2)
        with colA:
            st.image(img, caption="Original")
        with colB:
            st.image(edited, caption="Processed")