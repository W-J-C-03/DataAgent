# DataAgent —— 基于LangGraph的智能数据分析Agent
> ⚠️ 本仓库为学习演示项目，**并非开箱即用可部署版本**。
> 仅存放核心业务逻辑代码，剥离本地环境配置、密钥、完整web服务。
> 完整系统在本地开发环境完成验证，部分边界case尚未完善。

## 技术栈
Python、LangGraph、Qdrant、Elasticsearch、MySQL、FastAPI、SSE

## 主要实现
1. 基于StateGraph构建Text-to-SQL规划工作流，面向数仓自然语言问数场景，覆盖关键词抽取→三路并发元数据召回→信息合并过滤→SQL生成→语法校验与执行全链路，流式返回查询结果与图表数据。
2. 利用conditional_edges实现SQL自纠错闭环：SQL校验或执行失败时，自动路由到反思纠错节点，LLM根据报错信息迭代改写SQL，实现具备Self-Correction能力的Agent流程。
3. 搭建混合索引的元数据RAG：表、字段、指标基础元数据存入MySQL；字段与指标描述在Qdrant构建稠密向量索引；字段枚举取值在ES建立倒排索引，用于WHERE条件精确匹配；搭配Query Expansion查询扩展，并行检索三类索引，提升Schema召回准确率。
4. 集成LLM意图过滤与Schema压缩：三路召回结果汇总后，由LLM二次过滤无关表和字段，自动识别、补全主外键关联，精简送入大模型的上下文，缓解长上下文幻觉，降低Token消耗。

## 关键模块
- graph/: Text-to-SQL状态机、节点定义、纠错分支路由

## 运行说明
1. 代码仅保留核心逻辑，需自行部署MySQL、Qdrant、Elasticsearch以及配置LLM API
2. 支持单独调试各个节点，分步验证召回、SQL生成、纠错逻辑，无需一次性跑通全链路

