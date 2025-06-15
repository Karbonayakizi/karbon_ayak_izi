import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.markdown(
    """
    <style>
    .stApp {
        background-color: #8FBC8F;  /* Yaprak yeşili */
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.image("k.PNG", use_container_width=True)

ELEKTRIK_CO2_PER_KWH = 0.44  # kg CO₂ / kWh
INTERNET_CO2_PER_SAAT = 0.071  # kg CO₂ / saat

st.title("DÜNYA'YA BIRAKTIĞIN İZİ GÖR")
st.write("Günlük yaşam ve dijital alışkanlıklarına göre karbon ayak izini hesapla.")

# ULAŞM
st.header("Ulaşım Bilgileri")
ulasim_turu = st.selectbox("Ulaşım türünü seçin:", ["Araç", "Toplu Taşıma", "Yayan", "Bisiklet"])
ulasim_karbon = 0.0
if ulasim_turu == "Araç":
    arac_turu = st.selectbox("Araç türü:", ["Benzinli", "Dizel", "Elektrikli"])
    km = st.number_input("Günlük km:", step=1.0)
    kats = {"Benzinli": 0.192, "Dizel": 0.171, "Elektrikli": 0.04}
    ulasim_karbon = km * kats[arac_turu] * 365
elif ulasim_turu == "Toplu Taşıma":
    km = st.number_input("Günlük toplu taşıma km:", step=1.0)
    ulasim_karbon = km * 0.105 * 365

# BESLENM
st.header("Beslenme")
tur = st.selectbox("Beslenme türünüz:", ["Vegan", "Vejetaryen", "Omnivor"])
kirmizi, tavuk, sebze = 0.0, 0.0, 0.0
if tur == "Vegan":
    sebze = st.number_input("Günlük sebze porsiyonu:", step=1.0)
elif tur == "Vejetaryen":
    tavuk = st.number_input("Günlük tavuk porsiyonu:", step=1.0)
    sebze = st.number_input("Günlük sebze porsiyonu:", step=1.0)
else:
    kirmizi = st.number_input("Günlük kırmızı et porsiyonu:", step=1.0)
    tavuk = st.number_input("Günlük tavuk porsiyonu:", step=1.0)
    sebze = st.number_input("Günlük sebze porsiyonu:", step=1.0)

# ELEKTRİK-SU
st.header("Ev Tüketimleri")
elektrik_fatura = st.number_input("Aylık elektrik faturası (TL):", step=1.0)
elektrik_kwh = elektrik_fatura / 2.5 * 12
elektrik_karbon = elektrik_kwh * ELEKTRIK_CO2_PER_KWH

su_fatura = st.number_input("Aylık su faturası (TL):", step=1.0)
su_m3 = su_fatura / 10 * 12
su_karbon = su_m3 * 0.3

# Geri Dönüşüm
st.header("Geri Dönüşüm")
geri = st.radio("Geri dönüşüm yapıyor musunuz?", ["Evet", "Hayır"])
indir = 0.9 if geri == "Evet" else 1.0

# Uçak & İnternet 
st.header("Seyahat ve Dijital")
ucak_saat = st.number_input("Yıllık uçak saati:", step=1.0)
ucak_karbon = ucak_saat * 90

internet_saat = st.number_input("Yıllık ekran/internet saati:", step=10.0)
internet_karbon = internet_saat * INTERNET_CO2_PER_SAAT

# Toplam Hesaplama 
kirmizi_kg = kirmizi * 7 * 365
tavuk_kg = tavuk * 3 * 365
sebze_kg = sebze * 0.5 * 365

toplam = (ulasim_karbon + kirmizi_kg + tavuk_kg + sebze_kg +
          elektrik_karbon + su_karbon + ucak_karbon + internet_karbon) * indir

st.subheader(f"Yıllık karbon ayak iziniz: {toplam:.2f} kg CO₂")

# CO2 karşılığı hesapları
agac_kg_co2 = 21  # Bir ağacın yılda temizlediği kg CO2
agac_sayisi = toplam / agac_kg_co2

araba_km_eq = toplam / 0.2  # 1 km araç 0.2 kg CO2 yayar

st.write("---")
st.markdown("**CO₂’nin Karşılığı Ne?**")
st.write(f"- Bu, yaklaşık **{agac_sayisi:.1f} adet ağacın 1 yılda temizleyebileceği** kadar CO₂’ye eşdeğer.")



def grafik_ciz(x):
    y = np.array([2021, 2022, 2023, 2024, 2025])
    ort = np.array([500000, 510000, 520000, 530000, 540000]) / 84
    plt.figure(figsize=(8, 5))
    plt.plot(y, ort, marker='o', label="Türkiye ortalaması")
    plt.hlines(x, y.min(), y.max(), colors="red", linestyles="--", label="Sizin iziniz")
    plt.xlabel("Yıl")
    plt.ylabel("kg CO₂")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

grafik_ciz(toplam)