# 🔐 Env Manager

AI环境变量管理工具，支持.env文件生成、验证、文档生成。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenAI-API-green?logo=openai" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

## ✨ 特性

- 📝 从描述生成.env
- 📋 生成.env.example
- ✅ .env验证
- 📖 环境变量文档
- 📦 项目模板
- 📂 .env文件加载/保存

## 🚀 快速开始

```bash
pip install openai

python manager.py
```

## 📖 使用

```python
from env_manager import create_manager

manager = create_manager()

# 从描述生成
env = manager.generate_from_description("FastAPI项目，使用PostgreSQL")

# 生成.example
example = manager.generate_example(env_content)

# 验证
result = manager.validate_env(env_content, ["DATABASE_URL", "SECRET_KEY"])

# 生成文档
docs = manager.generate_docs(env_content)

# 项目模板
template = manager.generate_template("fastapi")

# 加载/保存
env_vars = manager.load_env_file(".env")
manager.save_env_file(env_vars, ".env")
```

## 📦 支持的项目模板

| 类型 | 说明 |
|------|------|
| fastapi | FastAPI配置 |
| flask | Flask配置 |
| django | Django配置 |
| react | React配置 |
| node | Node.js配置 |

## 📁 项目结构

```
env-manager/
├── manager.py     # 环境变量管理器核心
└── README.md
```

## 📄 许可证

MIT License
