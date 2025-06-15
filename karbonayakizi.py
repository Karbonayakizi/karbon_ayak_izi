import matplotlib.pyplot as plt
import numpy as np

def kullanici_ulasim_verisi_al():
    print("Ulaşım türünü seçin:")
    print("1. Araç")
    print("2. Toplu Taşıma")
    print("3. Yayan")
    print("4. Bisiklet")
    ulasim_turu = input("Seçiminiz (1-4): ")

    ulasim_karbon = 0

    if ulasim_turu == "1":
        print("Araç türünü seçin:")
        print("1. Benzinli")
        print("2. Dizel")
        print("3. Elektrikli")
        arac_turu = input("Seçiminiz (1-3): ")
        km = float(input("Günlük araçla gidilen km: "))
        katsayilar = {
            "1": 0.192,  # Benzinli (kg CO2/km)
            "2": 0.171,  # Dizel
            "3": 0.04    # Elektrikli (ortalama)
        }
        ulasim_karbon = km * katsayilar.get(arac_turu, 0.192)

    elif ulasim_turu == "2":
        km = float(input("Günlük toplu taşıma ile gidilen km: "))
        ulasim_karbon = km * 0.105  # Ortalama toplu taşıma kg CO2/km

    elif ulasim_turu == "3":
        km = float(input("Günlük yayan gidilen km: "))
        ulasim_karbon = 0.0  # Yaya karbon ayak izi sıfır

    elif ulasim_turu == "4":
        km = float(input("Günlük bisikletle gidilen km: "))
        ulasim_karbon = 0.0  # Bisiklet karbon ayak izi sıfır

    else:
        print("Geçersiz seçim, sıfır kabul edildi.")

    return ulasim_karbon * 365  # Yıllık hesap

def kullanici_beslenme_verisi_al():
    print("\nBeslenme türünüzü seçin:")
    print("1. Vegan")
    print("2. Vejetaryen")
    print("3. Omnivor (Et tüketen)")

    tur = input("Seçiminiz (1-3): ")

    if tur == "1":
        kirmizi_et = 0
        tavuk_et = 0
        sebze = float(input("Günlük sebze porsiyonu sayısı: "))
    elif tur == "2":
        kirmizi_et = 0
        tavuk_et = float(input("Günlük tavuk porsiyonu sayısı: "))
        sebze = float(input("Günlük sebze porsiyonu sayısı: "))
    else:
        kirmizi_et = float(input("Günlük kırmızı et porsiyonu sayısı: "))
        tavuk_et = float(input("Günlük tavuk porsiyonu sayısı: "))
        sebze = float(input("Günlük sebze porsiyonu sayısı: "))

    return kirmizi_et, tavuk_et, sebze

def elektrik_faturadan_kwh(fatura_tl):
    ortalama_kwh_fiyat = 2.5  # TL/kWh (örnek)
    return fatura_tl / ortalama_kwh_fiyat

def su_faturadan_m3(fatura_tl):
    ortalama_m3_fiyat = 10  # TL/m3 (örnek)
    return fatura_tl / ortalama_m3_fiyat

def karbon_hesapla(ulasim_kg, kirmizi_et, tavuk_et, sebze, elektrik_kwh, su_m3, geri_donusum_var, ucak_saat):
    # kg CO2 yıllık tahmini değerler
    kirmizi_et_kg = kirmizi_et * 7.0 * 365  # et porsiyonu başına 7 kg CO2, yıllık
    tavuk_et_kg = tavuk_et * 3.0 * 365
    sebze_kg = sebze * 0.5 * 365

    elektrik_kg = elektrik_kwh * 0.5  # kWh başına 0.5 kg CO2
    su_kg = su_m3 * 0.3  # m3 başına 0.3 kg CO2

    # Uçak seyahati: saat başına yaklaşık 90 kg CO2
    ucak_kg = ucak_saat * 90

    toplam = (ulasim_kg + kirmizi_et_kg + tavuk_et_kg + sebze_kg + elektrik_kg + su_kg + ucak_kg)

    if geri_donusum_var:
        toplam *= 0.9  # %10 indirim

    return toplam

def kullanici_geri_donusum_verisi_al():
    cevap = input("Geri dönüşüm yapıyor musunuz? (evet/hayır): ").strip().lower()
    return cevap == "evet"

def kullanici_ucak_seyahati_al():
    saat = float(input("Yıllık uçak seyahati (saat olarak): "))
    return saat

def grafik_ciz(yillik_karbon):
    yillar = np.array([2021, 2022, 2023, 2024, 2025])
    # Türkiye'nin yıllık toplam karbon emisyon verileri (örnek)
    toplam_emisyon = np.array([500000, 510000, 520000, 530000, 540000])  # milyon ton CO2
    # Kişi başı emisyon hesaplama
    kisi_basi_emisyon = toplam_emisyon / 84  # Türkiye nüfusu yaklaşık 84 milyon

    plt.figure(figsize=(10,6))
    plt.plot(yillar, kisi_basi_emisyon, label="Türkiye Ortalama Karbon Ayak İzi", color="blue", marker="o")
    plt.hlines(y=yillik_karbon, xmin=yillar.min(), xmax=yillar.max(), colors="red", linestyles="--", label="Sizin Karbon Ayak İziniz")
    plt.title("Yıllara Göre Türkiye Ortalama Karbon Ayak İzi ve Sizin Karbon Ayak İziniz")
    plt.xlabel("Yıl")
    plt.ylabel("Karbon Ayak İzi (kg CO2)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    print("Karbon Ayak İzi Hesaplama Programına Hoşgeldiniz!\n")

    ulasim_karbon_gunluk = kullanici_ulasim_verisi_al()

    kirmizi_et, tavuk_et, sebze = kullanici_beslenme_verisi_al()

    fatura_tl = float(input("\nAylık elektrik faturanızın tutarını TL cinsinden giriniz: "))
    elektrik_kwh = elektrik_faturadan_kwh(fatura_tl)
    print(f"Tahmini yıllık elektrik kullanımı: {elektrik_kwh*12:.2f} kWh")

    fatura_su_tl = float(input("\nAylık su faturanızın tutarını TL cinsinden giriniz: "))
    su_m3 = su_faturadan_m3(fatura_su_tl)
    print(f"Tahmini yıllık su tüketimi: {su_m3*12:.2f} m3")

    geri_donusum_var = kullanici_geri_donusum_verisi_al()

    ucak_saat = kullanici_ucak_seyahati_al()

    toplam_karbon = karbon_hesapla(
        ulasim_karbon_gunluk,
        kirmizi_et,
        tavuk_et,
        sebze,
        elektrik_kwh*12,
        su_m3*12,
        geri_donusum_var,
        ucak_saat
    )

    print(f"\nYıllık karbon ayak iziniz: {toplam_karbon:.2f} kg CO2")

    grafik_ciz(toplam_karbon)