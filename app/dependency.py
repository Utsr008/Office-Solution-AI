import re

from collections import defaultdict, deque


def resolve_dependencies(calculations):


    names = {
        calc["name"]
        for calc in calculations
    }


    dependencies = defaultdict(list)

    for calc in calculations:

        references = re.findall(
            r"\[([^\]]+)\]",
            calc["formula"]
        )

        for ref in references:

           
            if ref in names:

                if ref not in dependencies[calc["name"]]:
                    dependencies[calc["name"]].append(ref)

   

    indegree = {
        name: len(dependencies[name])
        for name in names
    }

   

    reverse = defaultdict(list)

    for calculation, deps in dependencies.items():

        for dependency in deps:

            reverse[dependency].append(
                calculation
            )

  

    queue = deque(
        sorted(
            name
            for name in names
            if indegree[name] == 0
        )
    )

    order = []


    while queue:

        current = queue.popleft()

        order.append(current)

        for child in sorted(reverse[current]):

            indegree[child] -= 1

            if indegree[child] == 0:

                queue.append(child)

    

    if len(order) != len(names):

        raise ValueError(
            "Circular dependency detected"
        )

    return order


def topological_order(calculations):

    """
    Alias for compatibility with code that
    expects a topological_order() function.
    """

    return resolve_dependencies(calculations)