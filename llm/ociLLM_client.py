import oci
import os
from dotenv import load_dotenv
from llm.base import LLMClient

load_dotenv()

class ociLLMClient(LLMClient):
    def __init__(self):
        config_profile = os.getenv("OCI_PROFILE", "DEFAULT")
        config_file = os.path.expanduser(os.getenv("OCI_CONFIG_FILE", "~/.oci/config"))
        self.config = oci.config.from_file(config_file, config_profile)

        self.compartment_id = os.getenv("OCI_COMPARTMENT_ID")
        self.MODEL_ID = os.getenv("OCI_MODEL_ID")
        self.ENDPOINT = os.getenv(
            "OCI_GENAI_ENDPOINT",
            "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
        )

        if not self.config:
            raise ValueError("OCI config is not configured at this location")

        self.client = oci.generative_ai_inference.GenerativeAiInferenceClient(
            config=self.config,
            service_endpoint=self.ENDPOINT,
            retry_strategy=oci.retry.NoneRetryStrategy(),
            timeout=(10, 240),
        )

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        system_prompt = (system_prompt or "").strip()
        user_prompt = (user_prompt or "").strip()

        if not user_prompt:
            raise ValueError("User prompt is empty")

        messages = []

        # Add system message (optional but recommended)
        if system_prompt:
            system_content = oci.generative_ai_inference.models.TextContent(
                text=system_prompt
            )

            system_message = oci.generative_ai_inference.models.Message(
                role=oci.generative_ai_inference.models.Message.ROLE_SYSTEM,
                content=[system_content],
            )

            messages.append(system_message)

        # Add user message
        user_content = oci.generative_ai_inference.models.TextContent(
            text=user_prompt
        )

        user_message = oci.generative_ai_inference.models.Message(
            role=oci.generative_ai_inference.models.Message.ROLE_USER,
            content=[user_content],
        )

        messages.append(user_message)

        # Build request
        chat_request = oci.generative_ai_inference.models.GenericChatRequest(
            api_format=oci.generative_ai_inference.models.BaseChatRequest.API_FORMAT_GENERIC,
            messages=messages,
            max_tokens=2900,
            temperature=0.5,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=1,
            top_k=0,
        )

        chat_detail = oci.generative_ai_inference.models.ChatDetails(
            compartment_id=self.compartment_id,
            serving_mode=oci.generative_ai_inference.models.OnDemandServingMode(
                model_id=self.MODEL_ID
            ),
            chat_request=chat_request,
        )

        response = self.client.chat(chat_detail)

        text = (
            response.data.chat_response.choices[0]
            .message.content[0]
            .text.strip()
        )

        return text