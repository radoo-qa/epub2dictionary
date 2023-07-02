from typing import Dict

def book2dict(book_path, chapter_identifier='Chapter'):
    current_idx: int = 0
    chapters_idx: list[int] = []
    chapters_dict: dict[int, str] = {}

    with open(book_path, 'r') as file:
        read_file = file.read()
        count_chapters = read_file.count(chapter_identifier)
        for i in range(count_chapters):
            current_idx = read_file.find('Chapter', current_idx+1)
            chapters_idx.append(current_idx)

        for idx in range(len(chapters_idx)):
            if idx != len(chapters_idx) - 1:
                chapters_dict[idx+1] = read_file[chapters_idx[idx]:chapters_idx[idx+1]]
            else: chapters_dict[idx+1] = read_file[chapters_idx[idx]:]

    return chapters_dict
