def detect_trends(all_company_data):
    word_freq = {}

    for data in all_company_data:
        words = data.lower().split()

        for word in words:
            if len(word) > 4:
                word_freq[word] = word_freq.get(word, 0) + 1

    trends = [k for k, v in word_freq.items() if v >= 2]

    return trends[:10]