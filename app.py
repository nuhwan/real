from flask import Flask, request, jsonify, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# 구글 시트 인증 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/guilP/attendance_app/service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open("sheet").sheet1  # 스프레드시트 이름을 정확히 지정

# 기본 경로 엔드포인트 추가
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attendance', methods=['POST'])
def attendance():
    try:
        data = request.json
        student_id = data['student_id']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 디버깅 메시지 추가
        print(f"Received student_id: {student_id} at {timestamp}")

        # 시트에 데이터 추가
        sheet.append_row([student_id, timestamp])
        print("Data appended to Google Sheet")

        return jsonify({"status": "success", "student_id": student_id, "timestamp": timestamp})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
