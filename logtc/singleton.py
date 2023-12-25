def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            print(f"Create new instance {class_}")
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance
