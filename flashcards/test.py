import re

s = "\\text{What is the characteristic of a divergent sequence?}"
result = re.search('{(.*)}', s).group(1)

print(result)