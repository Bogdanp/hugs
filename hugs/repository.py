import types

from .parser import parse


class Repository:
    """Repositories hold sets of queries and commands.
    """

    def load_queries(self, *filenames):
        """Add queries and commands to this repository from one or
        more SQL files.

        Parameters:
          \*filenames(tuple[str]): A list of SQL filenames.

        Raises:
          ParseError: If any of the files can't be parsed.
        """
        functions = {}
        for filename in filenames:
            with open(filename, "r") as fp:
                data = fp.read()

            for expression in parse(data):
                source_code = expression.to_source_code()
                code = compile(source_code, filename, "exec")
                exec(code, {}, functions)

                function = functions[expression.name]
                function.__sql__ = expression.body
                setattr(self, expression.name, types.MethodType(function, self))
