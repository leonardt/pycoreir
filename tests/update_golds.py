import shutil
test_pairs = [
    ("ice40_test.json", "ice40_test_gold.json"),
    ("mapParallel_test.json", "mapParallel_test_gold.json")
]

for output, gold in test_pairs:
    shutil.copy(output, gold)
