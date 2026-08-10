import json
import os

def write_puzzle(filename, name, size, initial_revealed, cards_data):
    """Ghi cấu trúc màn chơi ra file JSON chuẩn."""
    cols = [chr(ord('A') + i) for i in range(size)]
    puzzle = {
        "name": name,
        "size": size,
        "columns": cols,
        "initially_revealed": initial_revealed,
        "cards": cards_data
    }
    
    os.makedirs("puzzles", exist_ok=True)
    filepath = os.path.join("puzzles", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(puzzle, f, ensure_ascii=False, indent=2)
    print(f"✅ Đã tạo/ghi đè file: {filepath}")

def generate_all_puzzles():
    print("🚀 Bắt đầu khởi tạo dữ liệu 6 màn chơi Griductive...")

    # =========================================================================
    # THẺ 1: 3x3 Level 1 — Small Village
    # =========================================================================
    cards_1 = [
        {"cell": "A1", "name": "Alice", "occupation": "Teacher", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Alice và Daniel có cùng trạng thái.", "args": {"person1": "Alice", "person2": "Daniel"}}},
        {"cell": "B1", "name": "Brian", "occupation": "Builder", "status": "Criminal",
         "clue": {"type": "SAME", "text": "Brian và Emma có cùng trạng thái.", "args": {"person1": "Brian", "person2": "Emma"}}},
        {"cell": "C1", "name": "Chloe", "occupation": "Doctor", "status": "Innocent",
         "clue": {"type": "EXACTLY", "text": "Cột C có đúng 0 Tội phạm.", "args": {"region": "col_C", "count": 0}}},
        {"cell": "A2", "name": "Daniel", "occupation": "Farmer", "status": "Innocent",
         "clue": {"type": "DIFFERENT", "text": "Daniel và Grace có trạng thái khác nhau.", "args": {"person1": "Daniel", "person2": "Grace"}}},
        {"cell": "B2", "name": "Emma", "occupation": "Chef", "status": "Criminal",
         "clue": {"type": "EXACTLY", "text": "Cột B có đúng 2 Tội phạm.", "args": {"region": "col_B", "count": 2}}},
        {"cell": "C2", "name": "Felix", "occupation": "Police Officer", "status": "Innocent",
         "clue": {"type": "DIFFERENT", "text": "Felix và Grace có trạng thái khác nhau.", "args": {"person1": "Felix", "person2": "Grace"}}},
        {"cell": "A3", "name": "Grace", "occupation": "Artist", "status": "Criminal",
         "clue": {"type": "SAME", "text": "Grace và Emma có cùng trạng thái.", "args": {"person1": "Grace", "person2": "Emma"}}},
        {"cell": "B3", "name": "Henry", "occupation": "Mechanic", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Henry và Ivy có cùng trạng thái.", "args": {"person1": "Henry", "person2": "Ivy"}}},
        {"cell": "C3", "name": "Ivy", "occupation": "Librarian", "status": "Innocent",
         "clue": {"type": "EXACTLY", "text": "Hàng 3 có đúng 1 Tội phạm.", "args": {"region": "row_3", "count": 1}}}
    ]
    write_puzzle("3x3_lv1.json", "Small Village", 3, ["Alice", "Felix"], cards_1)

    # =========================================================================
    # THẺ 2: 3x3 Level 2 — Town Center
    # =========================================================================
    cards_2 = [
        {"cell": "A1", "name": "Arthur", "occupation": "Architect", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Arthur và David có cùng trạng thái.", "args": {"person1": "Arthur", "person2": "David"}}},
        {"cell": "B1", "name": "Ben", "occupation": "Baker", "status": "Criminal",
         "clue": {"type": "SAME", "text": "Ben và Eva có cùng trạng thái.", "args": {"person1": "Ben", "person2": "Eva"}}},
        {"cell": "C1", "name": "Clara", "occupation": "Dentist", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Clara và Ian có cùng trạng thái.", "args": {"person1": "Clara", "person2": "Ian"}}},
        {"cell": "A2", "name": "David", "occupation": "Driver", "status": "Innocent",
         "clue": {"type": "DIFFERENT", "text": "David và George có trạng thái khác nhau.", "args": {"person1": "David", "person2": "George"}}},
        {"cell": "B2", "name": "Eva", "occupation": "Engineer", "status": "Criminal",
         "clue": {"type": "EXACTLY", "text": "Cột B có đúng 2 Tội phạm.", "args": {"region": "col_B", "count": 2}}},
        {"cell": "C2", "name": "Fred", "occupation": "Florist", "status": "Innocent",
         "clue": {"type": "DIFFERENT", "text": "Fred và George có trạng thái khác nhau.", "args": {"person1": "Fred", "person2": "George"}}},
        {"cell": "A3", "name": "George", "occupation": "Guard", "status": "Criminal",
         "clue": {"type": "SAME", "text": "George và Eva có cùng trạng thái.", "args": {"person1": "George", "person2": "Eva"}}},
        {"cell": "B3", "name": "Hannah", "occupation": "Hairdresser", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Hannah và Ian có cùng trạng thái.", "args": {"person1": "Hannah", "person2": "Ian"}}},
        {"cell": "C3", "name": "Ian", "occupation": "IT Consultant", "status": "Innocent",
         "clue": {"type": "EXACTLY", "text": "Hàng 3 có đúng 1 Tội phạm.", "args": {"region": "row_3", "count": 1}}}
    ]
    write_puzzle("3x3_lv2.json", "Town Center", 3, ["Arthur", "Fred"], cards_2)

    # =========================================================================
    # THẺ 3: 4x4 Level 1 — Capital District
    # =========================================================================
    cards_3 = [
        {"cell": "A1", "name": "Arthur", "occupation": "Architect", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Arthur và Diana có cùng trạng thái.", "args": {"person1": "Arthur", "person2": "Diana"}}},
        {"cell": "B1", "name": "Alex", "occupation": "Baker", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Alex và Chloe có cùng trạng thái.", "args": {"person1": "Alex", "person2": "Chloe"}}},
        {"cell": "C1", "name": "Chloe", "occupation": "Dentist", "status": "Innocent",
         "clue": {"type": "EXACTLY", "text": "Cột C có đúng 0 Tội phạm.", "args": {"region": "col_C", "count": 0}}},
        {"cell": "D1", "name": "Daniel", "occupation": "Doctor", "status": "Criminal",
         "clue": {"type": "EXACTLY", "text": "Cột D có đúng 3 Tội phạm.", "args": {"region": "col_D", "count": 3}}},
        {"cell": "A2", "name": "Diana", "occupation": "Designer", "status": "Innocent",
         "clue": {"type": "EXACTLY", "text": "Hàng 2 có đúng 2 Tội phạm.", "args": {"region": "row_2", "count": 2}}},
        {"cell": "B2", "name": "Emma", "occupation": "Engineer", "status": "Criminal",
         "clue": {"type": "EXACTLY", "text": "Cột B có đúng 1 Tội phạm.", "args": {"region": "col_B", "count": 1}}},
        {"cell": "C2", "name": "Felix", "occupation": "Florist", "status": "Innocent",
         "clue": {"type": "DIFFERENT", "text": "Felix và Emma có trạng thái khác nhau.", "args": {"person1": "Felix", "person2": "Emma"}}},
        {"cell": "D2", "name": "Fiona", "occupation": "Farmer", "status": "Criminal",
         "clue": {"type": "SAME", "text": "Fiona và Daniel có cùng trạng thái.", "args": {"person1": "Fiona", "person2": "Daniel"}}},
        {"cell": "A3", "name": "Grace", "occupation": "Guard", "status": "Criminal",
         "clue": {"type": "SAME", "text": "Grace và Emma có cùng trạng thái.", "args": {"person1": "Grace", "person2": "Emma"}}},
        {"cell": "B3", "name": "Henry", "occupation": "Hairdresser", "status": "Innocent",
         "clue": {"type": "EXACTLY", "text": "Hàng 3 có đúng 2 Tội phạm.", "args": {"region": "row_3", "count": 2}}},
        {"cell": "C3", "name": "Ivy", "occupation": "IT Consultant", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Ivy và Noah có cùng trạng thái.", "args": {"person1": "Ivy", "person2": "Noah"}}},
        {"cell": "D3", "name": "Jack", "occupation": "Judge", "status": "Criminal",
         "clue": {"type": "SAME", "text": "Jack và Fiona có cùng trạng thái.", "args": {"person1": "Jack", "person2": "Fiona"}}},
        {"cell": "A4", "name": "Kate", "occupation": "King", "status": "Innocent",
         "clue": {"type": "EXACTLY", "text": "Hàng 4 có đúng 0 Tội phạm.", "args": {"region": "row_4", "count": 0}}},
        {"cell": "B4", "name": "Leo", "occupation": "Librarian", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Leo và Kate có cùng trạng thái.", "args": {"person1": "Leo", "person2": "Kate"}}},
        {"cell": "C4", "name": "Maya", "occupation": "Mechanic", "status": "Innocent",
         "clue": {"type": "NEIGHBOR_COUNT", "text": "Hàng xóm Kate có 1 tội phạm.", "args": {"cell": "A4", "count": 1}}},
        {"cell": "D4", "name": "Noah", "occupation": "Nurse", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Noah và Alex có cùng trạng thái.", "args": {"person1": "Noah", "person2": "Alex"}}}
    ]
    write_puzzle("4x4_lv1.json", "Capital District", 4, ["Arthur", "Chloe"], cards_3)

    # =========================================================================
    # THẺ 4: 4x4 Level 2 — Custom City
    # =========================================================================
    cards_4 = [
        {"cell": "A1", "name": "Alex", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Hàng 4 có duy nhất 1 người Vô tội và đó là người ở Cột 1 (Cột A).", "args": {"clues": [{"type": "FACT", "args": {"person": "Mary", "status": "Innocent"}}, {"type": "EXACTLY", "args": {"region": "row_4", "count": 3}}]}}},
        {"cell": "B1", "name": "Beth", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "EXACTLY", "text": "Cột 2 (Cột B) của tôi có chính xác 2 Tội phạm.", "args": {"region": "col_B", "count": 2}}},
        {"cell": "C1", "name": "Carl", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Cả Beth và Gwen có cùng thân phận.", "args": {"person1": "Beth", "person2": "Gwen"}}},
        {"cell": "D1", "name": "Dave", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "AND", "text": "Có 1 hàng và 1 cột chỉ toàn Vô tội.", "args": {"clues": [{"type": "OR", "args": {"clues": [{"type": "EXACTLY", "args": {"region": f"row_{i}", "count": 0}} for i in range(1, 5)]}}, {"type": "OR", "args": {"clues": [{"type": "EXACTLY", "args": {"region": f"col_{c}", "count": 0}} for c in "ABCD"]}}]}}},
        {"cell": "A2", "name": "Emma", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Ivan và Luke có cùng thân phận với nhau.", "args": {"person1": "Ivan", "person2": "Luke"}}},
        {"cell": "B2", "name": "Finn", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "FACT", "text": "Emma là 1 trong những hàng xóm Vô tội của tôi.", "args": {"person": "Emma", "status": "Innocent"}}},
        {"cell": "C2", "name": "Gwen", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "AND", "text": "Tôi là 1 trong 2 Tội phạm ở Cột 3 (Cột C).", "args": {"clues": [{"type": "FACT", "args": {"person": "Gwen", "status": "Criminal"}}, {"type": "EXACTLY", "args": {"region": "col_C", "count": 2}}]}}},
        {"cell": "D2", "name": "Hugh", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Hàng 2 chỉ có đúng 1 Tội phạm và không ở 2 cột trước (Cột A, B).", "args": {"clues": [{"type": "EXACTLY", "args": {"region": "row_2", "count": 1}}, {"type": "FACT", "args": {"person": "Emma", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Finn", "status": "Innocent"}}]}}},
        {"cell": "A3", "name": "Ivan", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "GLOBAL_TOTAL", "text": "Có tổng cộng 6 Tội phạm.", "args": {"count": 6}}},
        {"cell": "B3", "name": "Jane", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "FACT", "text": "Dave là Tội phạm.", "args": {"person": "Dave", "status": "Criminal"}}},
        {"cell": "C3", "name": "Kyle", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "FACT", "text": "Gwen là Tội phạm.", "args": {"person": "Gwen", "status": "Criminal"}}},
        {"cell": "D3", "name": "Luke", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Paul là hàng xóm Tội phạm duy nhất của tôi.", "args": {"clues": [{"type": "FACT", "args": {"person": "Paul", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Hugh", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Kyle", "status": "Innocent"}}]}}},
        {"cell": "A4", "name": "Mary", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "FACT", "text": "Nate là Tội phạm.", "args": {"person": "Nate", "status": "Criminal"}}},
        {"cell": "B4", "name": "Nate", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "EXACTLY", "text": "Hàng 4 có đúng 3 Tội phạm.", "args": {"region": "row_4", "count": 3}}},
        {"cell": "C4", "name": "Opal", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "FACT", "text": "Carl Vô tội.", "args": {"person": "Carl", "status": "Innocent"}}},
        {"cell": "D4", "name": "Paul", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "FACT", "text": "Hugh Vô tội.", "args": {"person": "Hugh", "status": "Innocent"}}}
    ]
    write_puzzle("4x4_lv2.json", "Custom City", 4, ["Alex", "Mary"], cards_4)

    # =========================================================================
    # THẺ 5: 5x5 Level 1 — Metropolis A
    # =========================================================================
    cards_5 = [
        {"cell": "A1", "name": "Alice", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "AND", "text": "Hàng của tôi và cột của tôi mỗi bên có chính xác hai Tội phạm.", "args": {"clues": [{"type": "EXACTLY", "args": {"region": "row_1", "count": 2}}, {"type": "EXACTLY", "args": {"region": "col_A", "count": 2}}]}}},
        {"cell": "B1", "name": "Ben", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "FACT", "text": "Gina là Tội phạm.", "args": {"person": "Gina", "status": "Criminal"}}},
        {"cell": "C1", "name": "Chloe", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "EXACTLY", "text": "Người ở cả bốn góc của lưới đều là Tội phạm.", "args": {"region": "corners", "count": 4}}},
        {"cell": "D1", "name": "Dan", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Gina và Iris có cùng trạng thái với nhau.", "args": {"person1": "Gina", "person2": "Iris"}}},
        {"cell": "E1", "name": "Evan", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "EXACTLY", "text": "Tất cả người trên 2 đường chéo đều là Tội phạm.", "args": {"region": "all_diagonals", "count": 9}}},
        {"cell": "A2", "name": "Finn", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Gina và Quinn có cùng trạng thái.", "args": {"person1": "Gina", "person2": "Quinn"}}},
        {"cell": "B2", "name": "Gina", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "OR", "text": "Hàng 4 có thứ tự Tội phạm và Vô tội xen kẽ nhau.", "args": {"clues": [{"type": "AND", "args": {"clues": [{"type": "FACT", "args": {"person": "Pete", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Quinn", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Rose", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Sam", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Tara", "status": "Criminal"}}]}}, {"type": "AND", "args": {"clues": [{"type": "FACT", "args": {"person": "Pete", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Quinn", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Rose", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Sam", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Tara", "status": "Innocent"}}]}}]}}},
        {"cell": "C2", "name": "Harry", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Cột 3 có chính xác một Tội phạm, và người đó nằm ở Hàng 3.", "args": {"clues": [{"type": "EXACTLY", "args": {"region": "col_C", "count": 1}}, {"type": "FACT", "args": {"person": "Mona", "status": "Criminal"}}]}}},
        {"cell": "D2", "name": "Iris", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "FACT", "text": "Owen Vô tội.", "args": {"person": "Owen", "status": "Innocent"}}},
        {"cell": "E2", "name": "Jack", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Iris và Sam có cùng trạng thái.", "args": {"person1": "Iris", "person2": "Sam"}}},
        {"cell": "A3", "name": "Kael", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Hai người đứng ngay trên và dưới tôi đều Vô tội.", "args": {"clues": [{"type": "FACT", "args": {"person": "Finn", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Pete", "status": "Innocent"}}]}}},
        {"cell": "B3", "name": "Liam", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "EXACTLY", "text": "Hàng 2 có chính xác hai Tội phạm.", "args": {"region": "row_2", "count": 2}}},
        {"cell": "C3", "name": "Mona", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "NO_ADJACENT", "text": "Không có bất kỳ hai Tội phạm nào trong toàn bộ lưới này nằm sát cạnh nhau theo chiều ngang hay dọc.", "args": {}}},
        {"cell": "D3", "name": "Noah", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "FACT", "text": "Kael Vô tội.", "args": {"person": "Kael", "status": "Innocent"}}},
        {"cell": "E3", "name": "Owen", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Jack và Noah đều Vô tội.", "args": {"clues": [{"type": "FACT", "args": {"person": "Jack", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Noah", "status": "Innocent"}}]}}},
        {"cell": "A4", "name": "Pete", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "EXACTLY", "text": "Cột 2 có chính xác hai Tội phạm.", "args": {"region": "col_B", "count": 2}}},
        {"cell": "B4", "name": "Quinn", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "FACT", "text": "Vera Vô tội.", "args": {"person": "Vera", "status": "Innocent"}}},
        {"cell": "C4", "name": "Rose", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Quinn và Sam có cùng trạng thái với nhau.", "args": {"person1": "Quinn", "person2": "Sam"}}},
        {"cell": "D4", "name": "Sam", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "FACT", "text": "Tara là Tội phạm.", "args": {"person": "Tara", "status": "Criminal"}}},
        {"cell": "E4", "name": "Tara", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "PATTERN_MATCH", "text": "Cột 5 có bố cục phân bố Tội phạm và Vô tội giống y hệt như Cột 1.", "args": {"region1": "col_E", "region2": "col_A"}}},
        {"cell": "A5", "name": "Ugo", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "GLOBAL_TOTAL", "text": "Có tổng cộng chính xác chín Tội phạm trong này.", "args": {"count": 9}}},
        {"cell": "B5", "name": "Vera", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "FACT", "text": "Xander Vô tội.", "args": {"person": "Xander", "status": "Innocent"}}},
        {"cell": "C5", "name": "Will", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Hàng 2 và Hàng 4 có số lượng Tội phạm bằng y hệt nhau.", "args": {"clues": [{"type": "EXACTLY", "args": {"region": "row_2", "count": 2}}, {"type": "EXACTLY", "args": {"region": "row_4", "count": 2}}]}}},
        {"cell": "D5", "name": "Xander", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "DIAGONAL", "text": "Những người trên đường chéo từ tôi đều Vô tội.", "args": {"direction": "anti", "count": 0}}},
        {"cell": "E5", "name": "Yuri", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "PATTERN_MATCH", "text": "Hàng 5 có bố cục phân bố Tội phạm và Vô tội giống y hệt như Hàng 1.", "args": {"region1": "row_5", "region2": "row_1"}}}
    ]
    write_puzzle("5x5_lv1.json", "Metropolis A", 5, ["Harry", "Chloe"], cards_5)

    # =========================================================================
    # THẺ 6: 5x5 Level 2 — Metropolis B
    # =========================================================================
    cards_6 = [
        {"cell": "A1", "name": "Alice", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "AND", "text": "Mỗi hàng và mỗi cột trong này chứa chính xác hai Tội phạm.", "args": {"clues": [{"type": "EXACTLY", "args": {"region": f"row_{i}", "count": 2}} for i in range(1, 6)] + [{"type": "EXACTLY", "args": {"region": f"col_{c}", "count": 2}} for c in "ABCDE"]}}},
        {"cell": "B1", "name": "Ben", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "AND", "text": "Liam và Quinn đều Vô tội.", "args": {"clues": [{"type": "FACT", "args": {"person": "Liam", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Quinn", "status": "Innocent"}}]}}},
        {"cell": "C1", "name": "Chloe", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Hai Tội phạm của Cột 3 nằm ngay cạnh nhau.", "args": {"clues": [{"type": "EXACTLY", "args": {"region": "col_C", "count": 2}}, {"type": "OR", "args": {"clues": [{"type": "AND", "args": {"clues": [{"type": "FACT", "args": {"person": "Chloe", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Harry", "status": "Criminal"}}]}}, {"type": "AND", "args": {"clues": [{"type": "FACT", "args": {"person": "Harry", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Mona", "status": "Criminal"}}]}}, {"type": "AND", "args": {"clues": [{"type": "FACT", "args": {"person": "Mona", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Rose", "status": "Criminal"}}]}}, {"type": "AND", "args": {"clues": [{"type": "FACT", "args": {"person": "Rose", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Will", "status": "Criminal"}}]}}]}}]}}},
        {"cell": "D1", "name": "Dan", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "FACT", "text": "Noah là Tội phạm.", "args": {"person": "Noah", "status": "Criminal"}}},
        {"cell": "E1", "name": "Evan", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Rose và Will đều Vô tội.", "args": {"clues": [{"type": "FACT", "args": {"person": "Rose", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Will", "status": "Innocent"}}]}}},
        {"cell": "A2", "name": "Finn", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "DIAGONAL", "text": "Đường chéo còn lại có 2 Tội phạm.", "args": {"direction": "main", "count": 2}}},
        {"cell": "B2", "name": "Gina", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "OR", "text": "Tất cả người trên 1 trong 2 đường chéo đều là Tội phạm.", "args": {"clues": [{"type": "DIAGONAL", "args": {"direction": "main", "count": 5}}, {"type": "DIAGONAL", "args": {"direction": "anti", "count": 5}}]}}},
        {"cell": "C2", "name": "Harry", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "FACT", "text": "Gina là Tội phạm.", "args": {"person": "Gina", "status": "Criminal"}}},
        {"cell": "D2", "name": "Iris", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Evan là Vô tội duy nhất ở góc.", "args": {"clues": [{"type": "FACT", "args": {"person": "Evan", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Alice", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Ugo", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Yuri", "status": "Criminal"}}]}}},
        {"cell": "E2", "name": "Jack", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "FACT", "text": "Iris Vô tội.", "args": {"person": "Iris", "status": "Innocent"}}},
        {"cell": "A3", "name": "Kael", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "FACT", "text": "Người ở chính giữa là Tội phạm.", "args": {"person": "Mona", "status": "Criminal"}}},
        {"cell": "B3", "name": "Liam", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Hai Tội phạm của Hàng 3 là Mona và Noah.", "args": {"clues": [{"type": "FACT", "args": {"person": "Mona", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Noah", "status": "Criminal"}}, {"type": "EXACTLY", "args": {"region": "row_3", "count": 2}}]}}},
        {"cell": "C3", "name": "Mona", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "AND", "text": "Alice và Yuri là 2 Tội phạm xa nhất về khoảng cách.", "args": {"clues": [{"type": "FACT", "args": {"person": "Alice", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Yuri", "status": "Criminal"}}]}}},
        {"cell": "D3", "name": "Noah", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "FACT", "text": "Sam là Tội phạm.", "args": {"person": "Sam", "status": "Criminal"}}},
        {"cell": "E3", "name": "Owen", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Có duy nhất 1 hàng các Tội phạm không đứng liền kề nhau.", "args": {"clues": [{"type": "FACT", "args": {"person": "Ugo", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Yuri", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Vera", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Will", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Xander", "status": "Innocent"}}]}}},
        {"cell": "A4", "name": "Pete", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Hai Tội phạm của Hàng 4 là Sam và Tara.", "args": {"clues": [{"type": "FACT", "args": {"person": "Sam", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Tara", "status": "Criminal"}}, {"type": "EXACTLY", "args": {"region": "row_4", "count": 2}}]}}},
        {"cell": "B4", "name": "Quinn", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "FACT", "text": "Vera Vô tội.", "args": {"person": "Vera", "status": "Innocent"}}},
        {"cell": "C4", "name": "Rose", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "SAME", "text": "Will và Kael có cùng thân phận.", "args": {"person1": "Will", "person2": "Kael"}}},
        {"cell": "D4", "name": "Sam", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "FACT", "text": "Gina là Tội phạm.", "args": {"person": "Gina", "status": "Criminal"}}},
        {"cell": "E4", "name": "Tara", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "FACT", "text": "Ben là Tội phạm.", "args": {"person": "Ben", "status": "Criminal"}}},
        {"cell": "A5", "name": "Ugo", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "AND", "text": "Yuri và tôi là hai Tội phạm duy nhất ở Hàng 5.", "args": {"clues": [{"type": "FACT", "args": {"person": "Ugo", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Yuri", "status": "Criminal"}}, {"type": "EXACTLY", "args": {"region": "row_5", "count": 2}}]}}},
        {"cell": "B5", "name": "Vera", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Xander là hàng xóm duy nhất là Vô tội của Yuri.", "args": {"clues": [{"type": "FACT", "args": {"person": "Xander", "status": "Innocent"}}, {"type": "FACT", "args": {"person": "Sam", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Tara", "status": "Criminal"}}]}}},
        {"cell": "C5", "name": "Will", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "DIFFERENT", "text": "Sam và Jack khác nhau về thân phận.", "args": {"person1": "Sam", "person2": "Jack"}}},
        {"cell": "D5", "name": "Xander", "occupation": "Citizen", "status": "Innocent",
         "clue": {"type": "AND", "text": "Hai Tội phạm ở Cột 5 là Tara và Yuri.", "args": {"clues": [{"type": "FACT", "args": {"person": "Tara", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Yuri", "status": "Criminal"}}, {"type": "EXACTLY", "args": {"region": "col_E", "count": 2}}]}}},
        {"cell": "E5", "name": "Yuri", "occupation": "Citizen", "status": "Criminal",
         "clue": {"type": "AND", "text": "Tara và tôi là hai Tội phạm duy nhất ở Cột 5.", "args": {"clues": [{"type": "FACT", "args": {"person": "Yuri", "status": "Criminal"}}, {"type": "FACT", "args": {"person": "Tara", "status": "Criminal"}}, {"type": "EXACTLY", "args": {"region": "col_E", "count": 2}}]}}}
    ]
    write_puzzle("5x5_lv2.json", "Metropolis B", 5, ["Alice", "Ugo"], cards_6)

    print("🎉 Hoàn tất! Tất cả 6 file puzzle trong thư mục 'puzzles/' đã sẵn sàng.")

if __name__ == "__main__":
    generate_all_puzzles()