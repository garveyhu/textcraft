from langchain.tools import BaseTool

from textcraft.summarize.spark_summarize import SparkSummarizer


class TitleTool(BaseTool):
    name = "标题生成工具"
    description = "给文本生成标题"

    def _run(self, text: str, run_manager=None) -> str:
        return self.run_for_title(text)

    async def _arun(
        self,
        text: str,
        run_manager=None,
    ) -> str:
        pass

    def run_for_title(self, text):
        return SparkSummarizer().summarize_text(text)
