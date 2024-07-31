import functools

"""
This file use as tool.
current tool
"""

description = """
# This is toll cli. 
current service exist is
{service_option}
your input:"""


def handle_migration():
    print("hallo world")


my_dict = dict([
    ("migration", handle_migration)
])


def main():
    while True:
        print("hallo world")
        user_option = functools.reduce(
            lambda accumulate_str, str_key: accumulate_str + f"\t-{str_key}\n",
            my_dict.keys()
        )
        user_message = input(description.format(service_option=user_option))
        user_data = my_dict.get(user_message)
        if user_data:
            user_data()
            break
        else:
            print(f"there is not service {user_message}")


if __name__ == "__main__":
    main()
    # for n in my_dict.keys():
    #     print(n)
