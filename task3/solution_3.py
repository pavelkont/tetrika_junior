def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']

    def merge_intervals(intervals_list):
        intervals_pairs = [(intervals_list[i], intervals_list[i+1]) for i in range(0, len(intervals_list), 2)]
        intervals_pairs.sort(key=lambda x: x[0])
        merged = []
        for start, end in intervals_pairs:
            if not merged or start > merged[-1][1]:
                merged.append([start, end])
            else:
                if end > merged[-1][1]:
                    merged[-1][1] = end
        return merged

    def trim_intervals(intervals_list):
        trimmed = []
        for i in range(0, len(intervals_list), 2):
            start = max(intervals_list[i], lesson_start)
            end = min(intervals_list[i+1], lesson_end)
            if start < end:
                trimmed.extend([start, end])
        return trimmed

    pupil_trimmed = trim_intervals(pupil)
    tutor_trimmed = trim_intervals(tutor)

    pupil_intervals = merge_intervals(pupil_trimmed)
    tutor_intervals = merge_intervals(tutor_trimmed)

    i, j = 0, 0
    total = 0
    while i < len(pupil_intervals) and j < len(tutor_intervals):
        start_p, end_p = pupil_intervals[i]
        start_t, end_t = tutor_intervals[j]
        start_max = max(start_p, start_t)
        end_min = min(end_p, end_t)
        if start_max < end_min:
            total += end_min - start_max
        if end_p < end_t:
            i += 1
        else:
            j += 1

    return total
