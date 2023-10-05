"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list[str] | None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation, digits and other symbols
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    text = text.lower()
    text = "".join(c for c in text if c.isalpha())
    return list(text)


def calculate_frequencies(tokens: list[str] | None) -> dict[str, float] | None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    frequency = {}
    for i in tokens:
        frequency[i] = tokens.count(i) / len(tokens)
    return frequency


def create_language_profile(language: str, text: str) -> dict[str, str | dict[str, float]] | None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :return: a dictionary with two keys – name, freq
    """
    tokenized = tokenize(text)
    frequencies = calculate_frequencies(tokenized)
    profile = dict({"name": language, "freq": frequencies})
    return profile


def calculate_mse(predicted: list, actual: list) -> float | None:
    """
    Calculates mean squared error between predicted and actual values
    :param predicted: a list of predicted values
    :param actual: a list of actual values
    :return: the score
    """
    results = 0
    for i in range(len(predicted)):
        diff = predicted[i] - actual[i]
        square = diff**2
        results += square
    mse = results/len(predicted)
    return float(mse)


def compare_profiles(
        unknown_profile: dict[str, str | dict[str, float]],
        profile_to_compare: dict[str, str | dict[str, float]]
) -> float | None:
    """
    Compares profiles and calculates the distance using symbols
    :param unknown_profile: a dictionary of an unknown profile
    :param profile_to_compare: a dictionary of a profile to compare the unknown profile to
    :return: the distance between the profiles
    """
    stats1 = unknown_profile.get('freq')
    stats2 = profile_to_compare.get('freq')
    union = set(stats1) | set(stats2)
    for i in union:
        if i not in stats1:
            stats1[i] = 0
    for i in union:
        if i not in stats2:
            stats2[i] = 0
    stats1_sorted = dict(sorted(stats1.items()))
    stats2_sorted = dict(sorted(stats2.items()))
    frequency1 = list(stats1_sorted.values())
    frequency2 = list(stats2_sorted.values())
    mse = (calculate_mse(frequency1, frequency2))
    return float(mse)


def detect_language(
        unknown_profile: dict[str, str | dict[str, float]],
        profile_1: dict[str, str | dict[str, float]],
        profile_2: dict[str, str | dict[str, float]],
) -> str | None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary of a profile to determine the language of
    :param profile_1: a dictionary of a known profile
    :param profile_2: a dictionary of a known profile
    :return: a language
    """
    res1 = compare_profiles(profile_1, unknown_profile)
    res2 = compare_profiles(profile_2, unknown_profile)
    if res1 > res2:
        lang = profile_1.get('name')
    elif res1 == res2:
        res1_name = profile_1.get('name')
        res2_name = profile_2.get('name')
        if res1_name > res2_name:
            lang = res1_name
        else:
            lang = res2_name
    else:
        lang = profile_2.get('name')
    return lang