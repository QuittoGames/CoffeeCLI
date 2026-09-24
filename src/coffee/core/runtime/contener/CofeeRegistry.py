class CoffeeRegistry:
    components: dict[type, type] = {}

    @classmethod
    def register(cls, component: type) -> type:
        cls.components[component] = component
        return component

    @classmethod
    def contains(cls, component: type) -> bool:
        return component in cls.components

    @classmethod
    def get(cls, component: type) -> type | None:
        return cls.components.get(component)

    @classmethod
    def all(cls) -> tuple[type, ...]:
        return tuple(cls.components.keys())
