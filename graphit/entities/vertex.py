class Vertex():
    def __init__(self, id: str):
        self.id = id

    def __lt__(self, other: object) -> bool:
        return self.id < other.id

    def __gt__(self, other: object) -> bool:
        return self.id > other.id
    
    def __repr__(self) -> str:
        return f"(Vertice {self.id})"
    
    def get_id(self) -> id:
        return self.id
    