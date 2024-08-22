async def str_check_for_nums(string: str, char_set: set = None):
    for i in string:
        if i not in char_set:
            return False

    else:
        return True


async def str_check(string: str, charset: set = None):
    for i in string:
        if i in charset:
            return False

    else:
        return True
