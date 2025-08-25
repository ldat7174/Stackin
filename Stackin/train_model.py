import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score 
from django.conf import settings
import django

# Thiết lập Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stackin.settings")
django.setup()

# Đường dẫn CSV (dùng BASE_DIR)
csv_path = os.path.join(settings.BASE_DIR, 'data.csv')
print(f"📂 Đường dẫn file CSV: {csv_path}")

# Kiểm tra file tồn tại
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"File CSV không tồn tại: {csv_path}")

# Đọc CSV tối ưu 
df = pd.read_csv(csv_path, dtype=float)  # Chuyển sang float để tối ưu
print(f"Cột hiện có: {list(df.columns)}")

# Kiểm tra cột label
label_column = 'label'
if label_column not in df.columns:
    raise ValueError(f"Cột '{label_column}' không tồn tại trong dữ liệu.")

# Tách X và y
X = df.drop(label_column, axis=1)
y = df[label_column]

# Train/test split nhanh
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y # stratify=y: Đảm bảo các nhãn được cân bằng
)

# Train Logistic Regression nhanh
model = LogisticRegression(solver='liblinear')  # solver nhẹ, phù hợp dataset nhỏ
model.fit(X_train, y_train)

# Dự đoán & đánh giá
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {acc:.2f}")

# Optional: lưu model để dùng lại
import joblib
model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
joblib.dump(model, model_path)
print(f"📦 Model đã lưu: {model_path}")
