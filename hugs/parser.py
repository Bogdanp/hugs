from .errors import ParseError
from .expression import Expression


class _LineIter:
    def __init__(self, data):
        self.lines = data.split("\n")

    def peek(self):
        try:
            return self.lines[0]
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.lines.pop(0)
        except IndexError:
            raise StopIteration


def parse(data):
    """Parse a string and return a list of hugs expressions.

    Parameters:
      data(str): The input string.

    Raises:
      ParseError

    Returns:
      generator[Expression]
    """
    lines = _LineIter(data)
    for line in lines:
        if line.rstrip() == "---":
            yield _parse_expression(lines)


def _parse_expression(lines):
    """Parse a single expression from a line iterator.

    Parameters:
      lines(LineIter)

    Raises:
      ParseError

    Returns:
      Expression
    """
    metadata, body = {}, []
    while True:
        try:
            if lines.peek().rstrip() == "---":
                break

            line = next(lines)
            body.append(line)
            for keyword in ("name", "args", "kwargs", "doc"):
                marker = f"-- {keyword}:"
                if line.startswith(marker):
                    metadata[keyword] = line[len(marker):].strip()
        except StopIteration:
            break

    body = "\n".join(body).strip()
    if "name" not in metadata:
        raise ParseError(f"expression {body!r} doesn't have a name")

    for keyword in ("args", "kwargs"):
        if keyword in metadata:
            metadata[keyword] = tuple(name.strip() for name in metadata[keyword].split(","))

    return Expression(body=body, **metadata)
