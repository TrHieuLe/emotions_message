import pandas as pd
from pyvi import ViTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# === 1. Đọc dữ liệu từ file Excel ===
duong_dan_file = "cam_xuc.xlsx"  # Đổi tên file nếu khác
df = pd.read_excel(duong_dan_file)
df.columns = ['ID', 'Emotion', 'Sentence']

# === 2. Tách từ tiếng Việt ===
df['Sentence_tok'] = df['Sentence'].apply(lambda x: ViTokenizer.tokenize(str(x)))

# === 3. Vector hóa văn bản ===
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['Sentence_tok'])
y = df['Emotion']

# === 4. Chia dữ liệu train/test và huấn luyện ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = MultinomialNB()
model.fit(X_train, y_train)

# === 5. Đánh giá mô hình ===
y_pred = model.predict(X_test)
print("=== Báo cáo phân loại ===")
print(classification_report(y_test, y_pred))

# 6. Lưu model và vectorizer
with open("emotion_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Đã lưu mô hình vào 'emotion_model.pkl' và vectorizer vào 'vectorizer.pkl'")