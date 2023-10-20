from langchain.tools import BaseTool

from textcraft.tools.label_tool import AliUnderstand


class ClassifyTool(BaseTool):
    name = "分类工具"
    description = (
        "分类工具"
    )

    def _run(self, text: str, run_manager=None) -> str:
        return self.run_for_classify(text)
    
    async def _arun(
            self,
            text: str,
            run_manager=None,
    ) -> str:
        pass

    def run_for_classify(self, text):
        labels = "传统业务知识，信用卡业务知识，公共业务知识，金融知识，保险知识，其他知识"
        return AliUnderstand().get_label(text, labels)
    
if __name__ == "__main__":
    classify = ClassifyTool()
    sentence = "某股份制银行推出的1年期、2年期、3年期的礼仪存单，利率分别是2.25%、2.85%、3.50%，每个期限的礼仪存单利率只比同期限的大额存单利率低0.05个百分点。"
    label = classify.run_for_classify(sentence)
    print(label)