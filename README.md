# 蓝印洗次 · 水洗时长交叉实验

比较同版同纸两种水洗方案，产出签发洗次。

**模拟客户**　栖浦蓝印工社，三位印刷师

**现有流程**　原来沿用手写纸签，容易抄错纸号、把水温混进效果、签发的参数追不到试条。

**业务交接**　同纸和负片的配对测量 → 质量印刷师 → 可追溯的锁版洗次工签。

## 一日工作剧本

1. 09:00 查 CY-032 桥影负片。
2. 09:10 核对雁皮棉纸和 60/120 秒对照。
3. 09:20 读逐条水温与密度。
4. 09:35 将水温差 5°C 的 S07 隔离。
5. 10:10 运行六对精确置换。
6. 10:20 核验双侧 p 与掉色。
7. 10:25 定版 120 秒。

## 算法和演示边界

穷举各对密度差的符号，按绝对总差计算双侧精确随机化概率，同时展示增益中位数。

每次分析只纳入 6 至 16 对通过复核的试条，掉色不得越过本批限值。演示数据为合成试印记录。

## 快速启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

- 前端浏览器地址为 `http://127.0.0.1:18440`。
- FastAPI 文档地址为 `http://127.0.0.1:19440/docs`。
- PostgreSQL 本地端口为 `17940`。后端与后台 worker 共用数据库事务和 Redis 健康探测。
- 开发 HTML、CSS、ES modules 后运行 `docker compose up -d --build frontend`。Python 代码修改后运行 `docker compose up -d --build backend worker`。
- `SEED_DEMO` 控制自动填充。可改三项宿主端口、`DEMO_PASSWORD`、`JWT_SECRET`、`POSTGRES_PASSWORD`。持久卷保存业务数据和队列状态。停机并保留数据使用 `docker compose down`。
- 技术栈为 Python 3.11、FastAPI、PostgreSQL 16、Redis 7、Nginx 与原生浏览器 JS。后端业务模块、SQL 迁移都在 `backend/`。界面和交互在 `frontend/`。

| 账号 | 密码 | 典型权限 |
|---|---|---|
| operator@demo.local | Demo2026! | 登记试条 |
| reviewer@demo.local | Demo2026! | 纳入与隔离试条、计算、签发工签 |
| viewer@demo.local | Demo2026! | 查阅记录和经计算的指标 |

共享角色和任务状态枚举分别位于 `backend/core.py` 的 `ROLES`、`JOB_STATES` 和 `frontend/base.js` 的 `roles`、`jobStates`。数据库检查约束与服务状态以相应 SQL 和模块为准。

许可证见 LICENSE。
