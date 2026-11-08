from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.core.log import logger


async def validate_sql(state:DataAgentState, runtime:Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "校验 SQL"
    writer({"type": "progress", "step": step, "status": "running"})
    try:
        sql = state['sql']
        dw_mysql_repository: DWMySQLRepository = runtime.context['dw_mysql_repository']
        try:
            await dw_mysql_repository.validate_sql(sql)
            writer({"type": "progress", "step": step, "status": "success"})
            logger.info(f"校验 SQL 成功")
            return {"error":None}
        except Exception as e:
            logger.info(f"SQL syntax error: {str(e)}")
            writer({"type": "progress", "step": step, "status": "success"})
            return {"error":str(e)}
    except Exception as e:
        logger.error(f"校验 SQL 失败：{e}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise
