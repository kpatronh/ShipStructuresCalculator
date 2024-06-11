class Material:
    def __init__(self, name, properties) -> None:
        self.name = name
        self.properties = properties
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(name={self.name}, properties={self.properties})"
    
    def __str__(self) -> str:
        return self.name


class Steel(Material):
    def __init__(self, name, properties) -> None:
        super().__init__(name, properties)

if __name__ == "__main__":
    def test1():
        material = Steel(name='steel_A131',properties=dict(yield_strength=235e6,
                                                            poisson_ratio=0.3,
                                                            young_modulus=2.1e11))
        print(material)
        print(repr(material))
    
    test1()