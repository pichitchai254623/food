import streamlit as st
import pandas as pd
import ast  # ใช้สำหรับแปลง string เป็น dictionary

# ตั้งค่าหน้าตาของเว็บ (ต้องเป็นคำสั่งแรกสุด)
st.set_page_config(page_title="แนะนำเมนูอาหารเย็น", page_icon="🍽️", layout="wide")

# โหลดข้อมูลจาก CSV
@st.cache_data
def load_data():
    file_path = "cleaned_data.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

# ฟังก์ชันแปลงที่อยู่จาก JSON string เป็นข้อความที่อ่านง่าย
def format_address(address):
    try:
        address_dict = ast.literal_eval(address)  # แปลง string เป็น dictionary
        street = address_dict.get("street", "")
        sub_district = address_dict.get("subDistrict", {}).get("name", "")
        district = address_dict.get("district", {}).get("name", "")
        city = address_dict.get("city", {}).get("name", "")
        return f"{street}, ตำบล{sub_district}, อำเภอ{district}, {city}"
    except (ValueError, SyntaxError):
        return "ไม่พบข้อมูลที่อยู่"

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
            
            # แปลงที่อยู่ให้อยู่ในรูปแบบที่อ่านง่าย
            formatted_address = format_address(row['address'])
            st.markdown(f"📍 **ที่อยู่:** {formatted_address}")

            st.markdown("---")
else:
    st.warning("ไม่พบร้านอาหารในช่วงราคาที่เลือก 🚫")

# วิธีรันแอป
st.sidebar.markdown("## ℹ️ วิธีใช้งาน")
st.sidebar.write("1️⃣ เลือกช่วงราคาที่ต้องการ 💰")
st.sidebar.write("2️⃣ ดูรายการร้านอาหารที่แนะนำ 🍽️")
st.sidebar.write("3️⃣ เพลิดเพลินกับอาหารมื้อเย็นของคุณ! 😋")
