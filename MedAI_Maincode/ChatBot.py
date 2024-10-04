import requests
import gradio as gr
key = "f914daada5mshde035a916247607p148638jsn0abe47d56130"

  # Hướng dẫn hệ thống ban đầu
# system_message = {
#     "role": "system",
#     "content": (
#       "Bạn là một trợ lý tư vấn chăm sóc sức khỏe tên là Dr.Hera. "
#         "Hãy hỏi rõ về triệu chứng khi người dùng gặp một vấn đề nào đó, "
#         "hãy cung cấp thông tin hoặc lời khuyên khi người dùng nói về một căn bệnh nào đó. "
#         "Lưu ý người dùng của bạn là một người Việt Nam không có kiến thức về y tế, "
#         "do đó bạn phải cung cấp các lời khuyên chính xác, ngắn gọn, đầy đủ đối với các câu hỏi liên quan đến sức khỏe. "
#         "Trả lời rằng bạn không thể hỗ trợ các vấn đề không liên quan đến sức khỏe khi nhận các câu hỏi không liên quan đến sức khỏe. "

#   )}
system_message = '''Bạn là một trợ lý tư vấn chăm sóc sức khỏe tên là Dr.Mimi.
Hãy hỏi rõ về triệu chứng khi người dùng gặp một vấn đề nào đó,
hãy cung cấp thông tin hoặc lời khuyên khi người dùng nói về một căn bệnh nào đó.
Lưu ý người dùng của bạn là một người Việt Nam không có kiến thức về y tế,
do đó bạn phải cung cấp các lời khuyên chính xác, ngắn gọn, đầy đủ đối với các câu hỏi liên quan đến sức khỏe.
Trả lời rằng bạn không thể hỗ trợ các vấn đề không liên quan đến sức khỏe khi nhận các câu hỏi không liên quan đến sức khỏe.
Chỉ được trả lời bằng Tiếng Việt.
Token tối đa của mỗi câu trả lời là 400 tokens. Hãy làm câu trả lời hoàn chỉnh về mặt nội dung và cấu trúc.'''


def chatbotfnc(message, history):
  url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4-2"
    # Thêm tin nhắn của người dùng vào lịch sử hội thoại

  conversation_history = [ ]
  for human, assistant in history:
      conversation_history.append({"role": "user", "content": human })
      conversation_history.append({"role": "assistant", "content":assistant})
  conversation_history.append({"role": "user", "content": message})

    # Payload chứa lịch sử hội thoại
  payload = {
    "messages": conversation_history,
    "system_prompt": system_message,
    "temperature": 0.7,  # Điều chỉnh temperature
    "top_k": 50,         # Điều chỉnh top_k
    "top_p": 0.9,        # Điều chỉnh top_p
    "max_tokens": 500,
    "web_access": False
    }


  headers = {
    "x-rapidapi-key": key,
    "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
    "Content-Type": "application/json"
    }

  try:
    response = requests.post(url, json=payload, headers=headers)
    # response.raise_for_status()  # Kiểm tra lỗi HTTP
    result = response.json()

    # Kiểm tra xem phản hồi có chứa khóa 'result' hay không
    if 'result' in result:
        hera_response = result['result']
        return hera_response
    else:
      return result['error']

  except requests.exceptions.RequestException as e :
    return f"Lỗi kết nối hoặc HTTP: {e} "

def create_Chatbot_tab(chatkey="Fix bug key"):

  Chatbot_tab = gr.ChatInterface(fn=chatbotfnc, examples=["Tôi bị đau dạ dày mạn tính vừa rồi tôi ăn xoài chua,tôi nên làm gì đây?", "Tôi khó thở vì covid tôi nên làm gì đây", "Tôi bị đau dạ dày lâu năm"], title="Bs.Mimi",                        description = "Trợ lý ảo - tư vấn sức khỏe", theme = "soft", submit_btn = "Gửi", retry_btn = "Thử lại",
                        undo_btn = "Quay lại", clear_btn = "Xóa toàn bộ", stop_btn = "Tạm dừng")
  return Chatbot_tab
