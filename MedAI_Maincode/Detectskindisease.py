import requests
import gradio as gr
from PIL import Image
import io
import numpy as np
import os

trans_disease = {
    "acne": "mụn",
    "actinic_keratosis": "chứng dày sừng quang hóa",
    "alopecia_androgenetica": "chứng rụng tóc nội tiết tố androgen",
    "alopecia_areata": "chứng rụng tóc từng vùng",
    "bullous_dermatosis": "bệnh da bọng nước",
    "chloasma": "nám da",
    "corn": "chứng chai da",
    "dermatofibroma": "u xơ da",
    "eczema_dermatitis": "viêm da chàm",
    "erysipelas": "viêm quầng",
    "erythema_multiforme": "ban đỏ đa dạng",
    "folliculitis": "viêm nang lông",
    "furuncle": "mụn nhọt",
    "haemangioma": "bệnh u máu",
    "herpes": "mụn rộp",
    "herpes_simplex": "nhiễm trùng do virus Herpes Simplex",
    "iga_vasculitis": "viêm mạch máu Iga",
    "keloid": "sẹo lồi",
    "keratosis_follicularism": "bệnh nang lông dày sừng",
    "lichen_planus": "bệnh lichen phẳng",
    "lupus_erythematosus": "bệnh ban đỏ",
    "molluscum_contagiosum": "u mềm lây",
    "nevus": "nốt ruồi",
    "paronychia": "viêm quanh móng",
    "pityriasis_alba": "bệnh vẩy phấn trắng",
    "pityriasis_rosea": "bệnh vảy phấn hồng",
    "prurigo_nodularis": "bệnh sẩn ngứa",
    "psoriasis": "bệnh vẩy nến",
    "rosacea": "bệnh trứng cá đỏ rosacea",
    "sebaceous_cyst": "u nang bã nhờn",
    "sebaceousnevus": "bớt tuyến bã",
    "seborrheic_dermatitis": "viêm da tiết bã",
    "seborrheic_keratosis": "chứng dày sừng tiết bã",
    "skin_tag": "mụn thịt dư",
    "stasis_dermatitis": "viêm da ứ đọng",
    "syringoma": "u ống tuyến mồ hôi",
    "tinea_capitis": "nấm da đầu",
    "tinea_corporis": "nấm cơ thể",
    "tinea_cruris": "nấm bẹn",
    "tinea_manuum": "",
    "tinea_pedis": "nấm chân",
    "tinea_unguium": "nấm móng tay móng chân",
    "tinea_versicolor": "bệnh lang ben",
    "urticaria": "phát ban",
    "urticaria_papular": "nổi mề đay",
    "varicella": "thủy đậu",
    "verruca_plana": "mụn cóc phẳng",
    "verruca_vulgaris": "mụn cóc thông thường",
    "vitiligo": "bệnh bạch biến"
}
trans_body = {
    "head": "đầu",
    "neck": "cổ",
    "hand": "tay",
    "arm": "cánh tay",
    "leg": "chân",
    "foot": "bàn chân",
    "back": "lưng",
    "chest": "ngực",
    "abdomen": "bụng",
    "face": "mặt",
    "ear": "tai",
    "eye": "mắt",
    "nose": "mũi",
    "mouth": "miệng",
    "lip": "môi",
    "cheek": "má",
    "tongue": "lưỡi",
    "throat": "cổ họng",
    "forehead": "trán",
    "chin": "cằm",
    "unknown" : "bộ phận chưa rõ"
}
def create_skin_tab(skinkey="2cff2aab49msh5191ef59693cc02p1091a7jsnd7100bb29621"):
    
    def detect_skin_disease(image):
        try:

            # Convert NumPy array to image file-like object
            img = Image.fromarray((image * 255).astype('uint8'))
            img_byte_array = io.BytesIO()
            img.save(img_byte_array, format='PNG')
            img_byte_array.seek(0)

            url = "https://detect-skin-disease.p.rapidapi.com/facebody/analysis/detect-skin-disease"
            # files = {"image": img_byte_array}
            files = {"image": ("image.png", img_byte_array, "image/png")}
            headers = {
                "X-RapidAPI-Key": skinkey,
                "X-RapidAPI-Host": "detect-skin-disease.p.rapidapi.com"
            }
            response = requests.post(url, files=files, headers=headers)
            response_json = response.json()
        
            output = ""

            if 'data' in response_json:
                body_part = response_json['data'].get('body_part')
                results = response_json['data'].get('results_english')

                if body_part is not None:
                    vnese_body = trans_body[body_part]
                    output += f"Phần của cơ thể: {vnese_body} ({body_part})\n"
                    
                if results is not None:
                    output += " Kết quả phân tích:      "

                # Sort the results by probability percentage in descending order
                sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

                for disease, probability in sorted_results:
                    probability_percent = probability * 100
                    vnese_disease = trans_disease.get(disease, disease)
                    if probability_percent >= 10:
                        output += f"{vnese_disease} : {probability_percent:.2f}%\n"

                return output
            else:
                return "Không có dữ liệu phản hồi từ API."
        except Exception as e:
            return f"Error: {str(e)}"

    
    css = """
    .textboxskin {
        font-sxxxxize: 50px; !important;
    }
    """
    with gr.Blocks(css=css) as demo:
        gr.Markdown("Hãy tải ảnh lên và nhấn **Xử Lý** để chẩn đoán bệnh ngoài da.")
        with gr.Row():
          inp = gr.Image(type="numpy",height=512, width=512,
          value=os.path.join(os.path.dirname(__file__), "../Image/thuydau.jpg"))
          out = gr.Label(label="Kết Quả Dự Đoán",elem_classes="textboxskin")
        btn = gr.Button("Xử Lý")
        btn.click(fn=detect_skin_disease, inputs=[inp], outputs=out)
    return demo
