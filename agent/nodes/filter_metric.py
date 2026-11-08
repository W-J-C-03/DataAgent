import yaml
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.prompt.prompt_loader import load_prompt
from app.core.log import logger


async def filter_metric(state:DataAgentState, runtime:Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "过滤指标信息"
    writer({"type": "progress", "step": step, "status": "running"})
    try:
        query = state['query']
        metric_infos = state['metric_infos']
        prompt = PromptTemplate(template=load_prompt("filter_metric_info"), input_variables=['query', 'metric_infos'])
        chain = prompt | llm | JsonOutputParser()
        result = await chain.ainvoke({
            "query": query,
            "table_infos": yaml.dump(metric_infos, allow_unicode=True, sort_keys=False),
        })
        filtered_metric_infos = [metric_info for metric_info in metric_infos if metric_info['name'] in result]
        writer({"type": "progress", "step": step, "status": "success"})
        logger.info(f"过滤指标信息成功：{len(filtered_metric_infos)} 个指标")
        return {"metric_infos":filtered_metric_infos}
    except Exception as e:
        logger.error(f"过滤指标信息失败：{e}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise
