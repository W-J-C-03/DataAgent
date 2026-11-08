from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.entities.metric_info import MetricInfo
from app.entities.value_info import ValueInfo
from app.prompt.prompt_loader import load_prompt
from app.core.log import logger


async def recall_value(state:DataAgentState, runtime:Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "召回字段取值"
    writer({"type": "progress", "step": step, "status": "running"})
    try:
        keywords = state['keywords']
        query = state['query']
        value_es_repository = runtime.context['value_es_repository']
        prompt = PromptTemplate(template=load_prompt("extend_keywords_for_value_recall"), input_variables=['query'])
        output_parser = JsonOutputParser()
        chain = prompt | llm | output_parser
        result = await chain.ainvoke({'query': query})
        keywords = set(keywords+result)
        value_info_map: dict[str, ValueInfo] = {}
        for keyword in keywords:
            current_value_infos: list[ValueInfo] = await value_es_repository.search(keyword)
            for value_info in current_value_infos:
                if value_info.id not in value_info_map:
                    value_info_map[value_info.id] = value_info
        retrieved_value_infos: list[ValueInfo] = list(value_info_map.values())
        writer({"type": "progress", "step": step, "status": "success"})
        logger.info(f"召回字段取值成功：{len(retrieved_value_infos)} 个取值")
        return {'retrieved_value_infos': retrieved_value_infos}
    except Exception as e:
        logger.error(f"召回字段取值失败：{e}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise