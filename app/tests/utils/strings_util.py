import itertools


def generate_all_possible_combination(string_to_change: str) -> list:
    """
    Nice utils to generate all the possible combination of
    upper and lower case

    :param string_to_change:
    :return: list
    :rtype:
    """
    return list(
        {
            "".join(x)
            for x in itertools.product(
                *zip(string_to_change.upper(), string_to_change.lower())
            )
        }
    )
