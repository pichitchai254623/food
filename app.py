import streamlit as st
import pandas as pd

# ตั้งค่าหน้าตาของเว็บ (ต้องเป็นคำสั่งแรกสุด)
st.set_page_config(page_title="แนะนำเมนูอาหารเย็น", page_icon="🍽️", layout="wide")

# โหลดข้อมูลจาก CSV
@st.cache_data
def load_data():
    file_path = "cleaned_data.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

# ส่วนติดต่อผู้ใช้
st.title("🍽️ แนะนำเมนูอาหารเย็นตามงบประมาณ")
st.markdown("เลือกช่วงราคาที่ต้องการเพื่อดูร้านอาหารที่เหมาะกับคุณ! 💰")

# เลือกช่วงราคา
price_options = sorted(df['price_level'].unique())
selected_price = st.selectbox("💵 เลือกช่วงราคาที่ต้องการ:", price_options)

# กรองข้อมูลตามช่วงราคาที่เลือก
filtered_df = df[df['price_level'] == selected_price]

# แสดงผลลัพธ์
st.subheader("🏪 ร้านอาหารที่แนะนำ")
if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"### 🍜 {row['name']}")
            st.markdown(f"**ประเภทอาหาร:** {row['cuisine']}")

            # ตรวจสอบว่า address เป็น NaN หรือ None หรือไม่
            address = row.get('address')
            if isinstance(address, str) and address != "NaN" and address.strip():  # ตรวจสอบว่าเป็นสตริงและไม่ว่างเปล่า
                st.markdown(f"📍 **ที่อยู่:** {address}")
            else:
                st.markdown("📍 **ที่อยู่:** ไม่พบข้อมูลที่อยู่")

            st.markdown("---")
else:
    st.warning("ไม่พบร้านอาหารในช่วงราคาที่เลือก 🚫")

# วิธีรันแอป
st.sidebar.markdown("## ℹ️ วิธีใช้งาน")
st.sidebar.write("1️⃣ เลือกช่วงราคาที่ต้องการ 💰")
st.sidebar.write("2️⃣ ดูรายการร้านอาหารที่แนะนำ 🍽️")
st.sidebar.write("3️⃣ เพลิดเพลินกับอาหารมื้อเย็นของคุณ! 😋")

#run -streamlit run app.py
