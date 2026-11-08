import yaml
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState, TableInfoState
from app.prompt.prompt_loader import load_prompt
from app.core.log import logger


async def filter_table(state:DataAgentState, runtime:Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "过滤表信息"
    writer({"type": "progress", "step": step, "status": "running"})
    try:
        query = state["query"]
        table_infos: list[TableInfoState] = state["table_infos"]
        prompt = PromptTemplate(template=load_prompt("filter_table_info"), input_variables=['query', 'table_infos'])
        chain = prompt | llm | JsonOutputParser()
        result = await chain.ainvoke({
            "query": query,
            "table_infos": yaml.dump(table_infos, allow_unicode=True, sort_keys=False),
        })
        # 调用大模型是因为要借助大模型来判断哪些字段需要或者不需要
        filtered_table_infos: list[TableInfoState] = []
        for table_info in table_infos:
            if table_info['name'] in result:
                table_info['columns'] = [column_info for column_info in table_info['columns'] if column_info['name'] in result[table_info['name']]]
                filtered_table_infos.append(table_info)
        writer({"type": "progress", "step": step, "status": "success"})
        logger.info(f"过滤表信息成功：{len(filtered_table_infos)} 张表")
        return {"table_infos":filtered_table_infos}
    except Exception as e:
        logger.error(f"过滤表信息失败：{e}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise