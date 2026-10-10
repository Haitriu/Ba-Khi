import streamlit as st
from google import genai
import base64
import json
from PIL import Image
from pathlib import Path

# 1. Cấu hình giao diện Web
NONLA_ICON_PATH = Path(__file__).with_name("non-la.svg")
NONLA_ICON_DATA = base64.b64encode(NONLA_ICON_PATH.read_bytes()).decode("ascii")
st.set_page_config(page_title="Việt Phục Remix", page_icon=str(NONLA_ICON_PATH), layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp, .stApp p, .stApp span, .stApp label, .stMarkdown { color: #2b2b2b !important; }
    .stApp { background-color: #FAEDCD !important; }
    h1, h2, h3 { color: #8B4513 !important; font-family: 'Times New Roman', serif; }
    h1 { text-align: center; border-bottom: 2px dashed #D4A373; padding-bottom: 10px; margin-bottom: 30px !important; }
    
    [data-testid="stSidebar"] { background-color: #FEFAE0 !important; border-right: 2px solid #D4A373; }
    
    /* Làm trắng nền ô nhập liệu */
    .stSelectbox>div>div, .stTextInput>div>div, .stFileUploader>div>div, .stTextArea>div>div { 
        background-color: #ffffff !important; border: 2px solid #D4A373 !important; border-radius: 8px !important; 
    }
    
    input, textarea, div[data-baseweb="select"] * { color: #2b2b2b !important; }
    ::placeholder { color: #888888 !important; opacity: 1 !important; }
    
    .stButton>button { 
        background-color: #8B4513 !important; border: none !important; border-radius: 8px !important; 
        padding: 10px 20px !important; box-shadow: 4px 4px 0px 0px #D4A373 !important; 
        transition: all 0.2s ease-in-out !important; color: #ffffff !important; font-weight: bold !important;
    }
    .stButton>button:hover { transform: translate(-2px, -2px) !important; box-shadow: 6px 6px 0px 0px #D4A373 !important; background-color: #A0522D !important; }
    
    .outfit-card { background-color: #ffffff; border: 2px solid #343A40; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 5px 5px 0px 0px #D4A373; }
    .info-box { background-color: #FEFAE0; padding: 15px; border-left: 4px solid #8B4513; border-radius: 4px; margin-top: 15px; }
    .warning-box { background-color: #FFE5E5; padding: 15px; border-left: 4px solid #D90429; border-radius: 4px; margin-top: 15px; margin-bottom: 15px; color: #D90429; font-weight: 500;}
    .success-box { background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745; border-radius: 4px; margin-bottom: 20px; color: #155724;}
    .analysis-box { background-color: #e2eafc; padding: 15px; border-left: 4px solid #3a86ff; border-radius: 4px; margin-bottom: 20px; color: #03045e; font-style: italic;}
</style>
""", unsafe_allow_html=True)

st.markdown(
    f'<h1><img src="data:image/svg+xml;base64,{NONLA_ICON_DATA}" '
    'alt="Nón lá Việt Nam" width="42" height="42" '
    'style="vertical-align: middle; margin-right: 8px;">'
    'Trợ lý AI: Việt Phục Remix</h1>',
    unsafe_allow_html=True,
)

API_KEY = "AQ.Ab8RN6LrLrXR46YP7k5fRlXMwZnlKfpRB42bT7G8N1VFEf3kRg"
client = genai.Client(api_key=API_KEY)

col_input, col_output = st.columns([1, 2], gap="large")

with col_input:
    st.subheader("📝 1. Bối cảnh & Nhu cầu")
    
    gioi_tinh = st.radio("Giới tính của bạn:", ["Nam", "Nữ", "Khác"], horizontal=True)
    su_kien = st.text_input("Sự kiện bạn tham gia:", placeholder="Ví dụ: Lễ bảo vệ đồ án, Đi chùa, Đi bar, Tập gym...")
    thoi_tiet = st.text_input("Thời tiết hiện tại:", placeholder="Ví dụ: Nóng 35 độ, Mưa rào, Se lạnh mùa thu...")
    phong_cach = st.radio("Phong cách phối đồ:", ["Truyền thống 100%", "Cách tân hiện đại", "Tự do phá cách (Mix đồ Âu/Sneaker)"])
    mau_sac_yeu_thich = st.text_input("Màu sắc ưu tiên (Tùy chọn):", placeholder="Ví dụ: Đỏ đô, Trắng, Đen...")
    
    st.subheader("📸 2. Stylist Nhìn Dáng")
    uploaded_file = st.file_uploader("Tải ảnh toàn thân của bạn lên", type=["jpg", "jpeg", "png"])
    
    img = None
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Ảnh bạn đã tải lên", use_container_width=True)
        st.success("Đã nhận ảnh! AI sẽ 'soi' dáng và tone da của bạn ngay bây giờ.")
    
    submit_btn = st.button("Trổ tài Tư vấn! 🚀", use_container_width=True)

with col_output:
    if submit_btn:
        if not su_kien.strip() or not thoi_tiet.strip():
            st.warning("Vui lòng nhập đầy đủ thông tin Sự kiện và Thời tiết nhé!")
        else:
            with st.spinner("⏳ Stylist đang phân tích bối cảnh và 'soi' hình ảnh..."):
                try:
                    # 🟢 THÊM TRƯỜNG "phu_kien" VÀO KHUÔN MẪU JSON
                    khuon_mau_json = """
                    Bạn là Stylist kiêm Chuyên gia Văn hóa cho ứng dụng Việt Phục Remix (Giọng điệu Gen Z). 
                    Hãy phân tích Input của người dùng và hình ảnh đính kèm (nếu có):
                    
                    BƯỚC 1: PHÂN TÍCH HÌNH ẢNH (QUAN TRỌNG)
                    - Nếu có ảnh, hãy phân tích kỹ: Tone da (sáng, ngăm, ấm, lạnh...) và Dáng người (gầy, mũm mĩm, cân đối, cao...).
                    - Ghi kết quả phân tích vào trường "image_analysis" và dùng thông tin này để tư vấn.
                    
                    BƯỚC 2: ĐÁNH GIÁ SỰ KIỆN & THỜI TIẾT
                    - Nếu 'khong_nen' (Đi bar, thể thao, bơi lội...) hoặc thời tiết khắc nghiệt: Đặt "is_suitable": false. Trả về "outfits": [].
                    - Nếu 'rat_hop' / 'hop': Đặt "is_suitable": true. Đề xuất 3 bộ Việt phục RÕ RỆT.
                    - Nếu 'can_nhac': Đặt "is_suitable": true. Đề xuất tối đa 3 bộ, BẮT BUỘC ghi điểm cần lưu ý vào "warnings_vi".
                    
                    BƯỚC 3: ĐÁNH GIÁ PHONG CÁCH
                    - Cảnh báo nếu phong cách mâu thuẫn với sự kiện vào trường "warnings_vi".
                    - Chỉ sử dụng: Áo Ngũ Thân, Áo Tấc, Nhật Bình, Áo Dài, Áo Tứ Thân, Áo Giao Lĩnh.
                    
                    TRẢ VỀ DUY NHẤT ĐỊNH DẠNG JSON SAU:
                    {
                      "is_suitable": boolean,
                      "image_analysis": "Phân tích chi tiết dáng người, tone da từ ảnh và đưa ra mẹo chọn đồ cơ bản (Nếu không có ảnh, trả về null)",
                      "overall_assessment": "Nhận xét về sự kiện, thời tiết, phong cách (Giọng Gen Z)",
                      "outfits": [
                        {
                          "title": "Tên trang phục",
                          "rationale": "Lý do khuyên mặc (Bao gồm cả việc nó che khuyết điểm/tôn dáng như thế nào dựa trên ảnh)",
                          "phu_kien": "Gợi ý phụ kiện đi kèm (nón lá, quạt, ngọc bội, giày...) hoặc họa tiết phù hợp (hoa sen, rồng, hạc...) (1 câu ngắn gọn)",
                          "origin": "Bối cảnh lịch sử ra đời (1-2 câu)",
                          "meaning": "Ý nghĩa văn hóa (1-2 câu)",
                          "warnings_vi": "Cảnh báo (nếu an toàn 100% thì trả về null)"
                        }
                      ]
                    }
                    """
                    
                    user_prompt = f"Giới tính: {gioi_tinh}. Sự kiện: {su_kien}. Thời tiết: {thoi_tiet}. Phong cách: {phong_cach}. Màu sắc: {mau_sac_yeu_thich}."
                    
                    prompt_contents = [user_prompt]
                    if img is not None:
                        prompt_contents.append(img)
                    
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt_contents,
                        config=genai.types.GenerateContentConfig(
                            temperature=0.2,
                            response_mime_type="application/json",
                            system_instruction=khuon_mau_json, 
                        ),
                    )
                    
                    data = json.loads(response.text)
                    is_suitable = data.get("is_suitable", True)
                    image_analysis = data.get("image_analysis")
                    overall_assessment = data.get("overall_assessment", "")
                    outfits = data.get("outfits", [])
                    
                    st.subheader("✨ Gợi ý Styling của bạn")
                    
                    if not is_suitable:
                        st.markdown(f'''<div class="warning-box">
                        <h4 style="margin-top:0; color:#D90429;">🛑 Ải chà chà... Bối cảnh này căng à nha!</h4>
                        {overall_assessment}
                        </div>''', unsafe_allow_html=True)
                        st.info("💡 Khuyên thật lòng: Hãy lưu Việt phục cho một dịp khác trang trọng và phù hợp hơn nhé bro!")
                    else:
                        if image_analysis:
                            st.markdown(f'''<div class="analysis-box"><b>👁️ AI Soi Dáng:</b> {image_analysis}</div>''', unsafe_allow_html=True)
                            
                        st.markdown(f'''<div class="success-box"><b>📝 Nhận xét từ AI:</b> {overall_assessment}</div>''', unsafe_allow_html=True)
                        
                        for idx, outfit in enumerate(outfits):
                            warning_html = ""
                            if outfit.get("warnings_vi"):
                                warning_html = f'''<div class="warning-box"><b>⚠️ Lưu ý sương sương:</b> {outfit.get("warnings_vi")}</div>'''
                            
                            # 🟢 HIỂN THỊ TRƯỜNG PHỤ KIỆN LÊN GIAO DIỆN
                            phu_kien = outfit.get("phu_kien", "Không có gợi ý phụ kiện đặc biệt.")
                                
                            html_card = f'''<div class="outfit-card">
<h3>Lựa chọn {idx + 1}: {outfit.get('title', '')}</h3>
<p style="font-size: 16px; font-style: italic;">"{outfit.get('rationale', '')}"</p>
<p style="font-size: 15px; color: #444;"><b>💍 Phụ kiện & Họa tiết:</b> {phu_kien}</p>
{warning_html}
<div class="info-box">
<p style="margin-bottom: 5px;"><b>📜 Bối cảnh ra đời:</b> {outfit.get('origin', '')}</p>
<p style="margin-bottom: 0;"><b>🌸 Ý nghĩa văn hóa:</b> {outfit.get('meaning', '')}</p>
</div>
</div>'''
                            st.markdown(html_card, unsafe_allow_html=True)
                        
                except Exception as e:
                    error_msg = str(e)
                    if "503" in error_msg or "UNAVAILABLE" in error_msg:
                        st.warning("⚠️ Lỗi 503 (Quá tải máy chủ): Hiện tại bộ não AI của Google đang có quá nhiều người truy cập cùng lúc trên toàn thế giới nên phản hồi hơi chậm. Bạn thông cảm đợi khoảng 30 giây rồi bấm nút thử lại nhé!")
                    else:
                        st.error(f"⚠️ Úi, có lỗi nhỏ xảy ra trong quá trình xử lý. Chi tiết: {error_msg}")