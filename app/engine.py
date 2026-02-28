from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_community.retrievers import WikipediaRetriever
from .schemas import DecisionRequest, DecisionResponse
from .prompts import DECIDER_SYSTEM, DECIDER_USER
from .logic import choose_frameworks

load_dotenv()

def get_chat_model():
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.3-70B-Instruct",
        task="text-generation",
        max_new_tokens=1200,
        temperature=0.5,
    )
    return ChatHuggingFace(llm=llm)



def run_level2(req: DecisionRequest):
    model = get_chat_model()

    retriever = WikipediaRetriever(top_k_results=2, lang="en")

    frameworks = choose_frameworks(req)  

    blocks = []
    for fw in frameworks:
        query = f"{fw} framework how to use steps decision making"
        docs = retriever.invoke(query)  
        text_parts = []

        for d in docs:
            if d.page_content:            
                text_parts.append(d.page_content)

        text = "\n\n".join(text_parts)[:2500]
    blocks.append(f"[{fw}]\n{text}")

    retrieved_context = "\n\n".join(blocks)[:12000]
    
    parser=PydanticOutputParser(pydantic_object=DecisionResponse)

    prompt = ChatPromptTemplate([
        ("system", DECIDER_SYSTEM),
        ("human", DECIDER_USER),
    ]).partial(format_instructions=parser.get_format_instructions())


    chain=prompt | model | parser

    raw = chain.invoke({
        "decision": req.decision,
        "domain": req.domain,
        "goal": req.goal,
        "context": req.context,
        "constraints": req.constraints,
        "options_considered": req.options_considered,
        "urgency": req.urgency,
        "risk_tolerance": req.risk_tolerance,
        "success_metrics": req.success_metrics,
        "retrieved_context": retrieved_context,
    })

    return raw