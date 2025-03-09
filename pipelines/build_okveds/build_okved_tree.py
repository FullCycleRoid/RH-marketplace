import pickle

from requests import Session

from pipelines.connector import SessionFactory
from src.classificators.models import OkvedNode


def build_tree(data, session):
    nodes = {}

    if data:
        for code, description in data.items():
            parts = code.split('.')
            parent = None

            for i in range(len(parts)):
                current_code = '.'.join(parts[:i + 1])

                if current_code not in nodes:
                    description = description.lower()
                    node = OkvedNode(code=current_code, description=description.capitalize())
                    nodes[current_code] = node

                    if parent:
                        parent.child_nodes.append(node)
                        node.parent = parent

                    session.add(node)
                    parent = node
                else:
                    parent = nodes[current_code]

        session.commit()


def load_okveds(filename):
    with open(filename, "rb") as file:
        loaded_data = pickle.load(file)

    return loaded_data


if __name__ == "__main__":
    filename = "okved_data.pkl"
    data = load_okveds(filename)

    _session: Session = SessionFactory
    with _session() as session:
        build_tree(data, session)