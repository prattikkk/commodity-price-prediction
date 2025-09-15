import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

import predict

print('About to call predict_for_date with date within 30 days...')
result = predict.predict_for_date('ONION', 'BANGALORE', '2025-06-15', 7)  # 9 days after last date
print('Function completed:', result)
