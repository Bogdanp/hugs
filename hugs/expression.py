from collections import namedtuple
from itertools import chain


_TEMPLATE = """\
def {name}(self, __cursor{args}):
    {doc!r}
    return __cursor.execute({body!r}{params})
"""


class Expression(namedtuple("Expression", ("name", "args", "kwargs", "doc", "body"))):
    """A SQL expression plus some metadata.

    Parameters:
      name(str): The name of the expression.
      args(tuple[str]): The positional argument names.
      kwargs(tuple[str]): The keyword-only argument names.
      doc(str): The docstring.
      body(str): The full body of the expression.
    """

    def __new__(cls, name, args=(), kwargs=(), doc="", body=""):
        return super().__new__(cls, name, args, kwargs, doc, body)

    def to_source_code(self):
        args, params = "", ""
        for name in self.args:
            args += f", {name}"

        if self.kwargs:
            args += ", *"

        for name in self.kwargs:
            args += f", {name}"

        if self.args or self.kwargs:
            params = ", {"
            for name in chain(self.args, self.kwargs):
                params += f"{name!r}: {name},"

            params += "}"

        return _TEMPLATE.format(
            name=self.name,
            doc=self.doc,
            body=self.body,
            args=args,
            params=params,
        )
