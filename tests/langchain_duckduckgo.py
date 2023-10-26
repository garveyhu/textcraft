from langchain.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
print(search.run("Who is winner of FIFA worldcup 2018?"))