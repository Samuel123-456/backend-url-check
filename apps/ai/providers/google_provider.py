from langchain.chat_models import init_chat_model, BaseChatModel
from langchain_core.prompts import ChatPromptTemplate


class GoogleProvider:

    @staticmethod
    def get_model() -> BaseChatModel:
        """Initialize and return the Google Gemini model."""

        model = init_chat_model(
            model="gemini-2.5-flash",
            model_provider="google_genai",
            temperature=0,
            # base_url="http://172.17.0.1:11434"
            api_key="AIzaSyBvjcM05-J9RNUZ5iuhO1gQj01AfeEkfa8" # API KEY FOR TESTS
        )

        return model