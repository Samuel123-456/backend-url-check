from ..providers import GoogleProvider
from ..prompts import LINK_ANALYSIS_SYSTEM_PROMPT, USER_LINK_ANALYSIS_PROMPT
from langchain_core.messages import SystemMessage
from ..outputs import LinkAnalysisOutput
from langchain_core.prompts import ChatPromptTemplate



class CheckURLChain:


    @staticmethod
    def run(url: str) -> LinkAnalysisOutput:

        model = GoogleProvider.get_model()
        prompts = [
            SystemMessage(content=LINK_ANALYSIS_SYSTEM_PROMPT), 
            ("human", USER_LINK_ANALYSIS_PROMPT)
        ]
        prompt_template = ChatPromptTemplate.from_messages(prompts)
        """Run the chain to analyze the given URL and return the analysis output."""

        # Format the user prompt with the provided URL
        prompt = prompt_template.format_messages(url_solicitada=url, texto_contextual="")

        # # Get the model's response
        model_output = model.with_structured_output(LinkAnalysisOutput)
        response =  model_output.invoke(prompt)

        return response.model_dump_json()