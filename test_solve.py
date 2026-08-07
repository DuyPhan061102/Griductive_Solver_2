from game.game_engine import GameEngine

e = GameEngine()
e.load_puzzle("puzzles/3x3_lv1.json")

print("=== Initial State ===")
for c in e.board.cards:
    print(f"  {c.cell_id} {c.name}: revealed={c.is_revealed}, status={c.true_status}")

print("\n=== Auto-solving step by step ===")
step_count = 0
while not e.is_finished and step_count < 20:
    # Show revealed state
    revealed = [c.name for c in e.board.cards if c.is_revealed]
    unsolved = [c.name for c in e.board.cards if not c.is_revealed]
    print(f"\nRevealed: {revealed}")
    print(f"Unsolved: {unsolved}")
    
    # Classify all
    classifications = e.agent.classify_all()
    print(f"Classifications: {classifications}")
    
    result = e.auto_solve_step()
    if result is None:
        print("No more provable verdicts!")
        break
    
    ch = result["character"]
    vd = result["verdict"]
    step_count += 1
    print(f"=> Step {step_count}: {ch} -> {vd}")

print(f"\nFinal: Solved={e.is_finished}")
