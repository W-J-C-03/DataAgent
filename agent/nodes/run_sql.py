from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


async def run_sql(state:DataAgentState, runtime:Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "执行 SQL"
    writer({"type": "progress", "step": step, "status": "running"})
    try:
        sql = state["sql"]
        dw_mysql_repository = runtime.context['dw_mysql_repository']
        result = await dw_mysql_repository.run(sql)
        writer({"type": "progress", "step": step, "status": "success"})
        logger.info(f"执行 SQL 成功")
        writer({"type": "progress", "data": result})
    except Exception as e:
        logger.error(f"执行 SQL 失败：{e}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise
