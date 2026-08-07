import fitz
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = sys.argv[1]
start_page = int(sys.argv[2]) if len(sys.argv) > 2 else 0
end_page = int(sys.argv[3]) if len(sys.argv) > 3 else None

doc = fitz.open(path)
print(f"Total pages: {len(doc)}")
for i, page in enumerate(doc):
    if i < start_page:
        continue
    if end_page is not None and i >= end_page:
        break
    print(f"--- Page {i+1} ---")
    print(page.get_text())
