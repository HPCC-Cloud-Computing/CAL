from calplus.exceptions import ProviderNotValidate


def validate_driver(check_function):
    """
    # TODO(daidv): in future, we should support check_function as an object
    and we will get all function start with test_*
    then check validation for all of them.
    It will be great help for callib user
    do NOT need add all of testcases in only a function
    :param check_function:
    :return:
    """
    def check_decorator(func):
        def func_wrapper(*args, **kwargs):
            check = check_function()
            if check:
                return func(*args, **kwargs)
            else:
                raise ProviderNotValidate()
        return func_wrapper
    return check_decorator
