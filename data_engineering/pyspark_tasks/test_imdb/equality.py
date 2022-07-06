from pyspark import Row


def _df_to_list_of_dicts(df):
    """Converts input DataFrame to the list of the dictionaries.

    Args:
        df (DataFrame): Spark DataFrame

    Returns:
        list: list of the converted dicts.
    """
    return list(map(Row.asDict, df.collect()))


def dfs_equal(actual, expected):
    """Asserts that actual equal to expected.

    Args:
        actual(DataFrame): Spark DataFrame
        expected(DataFrame): Spark DataFrame

    Returns:
        bool: result of comparison True or False

    """
    actual_content = _df_to_list_of_dicts(actual)
    expected_content = _df_to_list_of_dicts(expected)
    if len(actual_content) != len(expected_content):
        return False
    results = []
    for actual_item in actual_content:
        results.append(actual_item in expected_content)
    return all(results)
