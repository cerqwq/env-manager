"""
Env Manager - AI环境变量管理工具
支持.env文件生成、验证、文档生成
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class EnvManager:
    """
    AI环境变量管理工具
    支持：生成、验证、文档、模板
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def generate_from_description(self, description: str) -> str:
        """从描述生成.env"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请根据以下项目描述生成.env文件：

描述：{description}

要求：
1. 包含常用环境变量
2. 添加注释说明
3. 使用合理的默认值
4. 敏感值留空"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        return response.choices[0].message.content

    def generate_example(self, env_content: str) -> str:
        """生成.env.example"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请根据以下.env文件生成.env.example：

{env_content}

要求：
1. 移除敏感值
2. 保留注释
3. 使用占位符"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        return response.choices[0].message.content

    def validate_env(self, env_content: str, required: List[str] = None) -> Dict:
        """验证.env"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        required_text = ", ".join(required) if required else "无"

        prompt = f"""请验证以下.env文件：

{env_content}

必需变量：{required_text}

请返回JSON格式：
{{
    "valid": true/false,
    "missing": ["缺失的变量"],
    "empty": ["空值的变量"],
    "issues": ["问题1", "问题2"],
    "suggestions": ["建议1", "建议2"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"validation": content}

    def generate_docs(self, env_content: str) -> str:
        """生成环境变量文档"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请为以下.env文件生成文档：

{env_content}

要求：
1. 每个变量的说明
2. 类型和默认值
3. 是否必需
4. 使用示例"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def generate_template(self, project_type: str) -> str:
        """生成项目模板"""
        templates = {
            "fastapi": """
# FastAPI Configuration
APP_NAME=MyApp
APP_VERSION=1.0.0
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=sqlite:///./app.db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000"]
""",
            "flask": """
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///app.db

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=
MAIL_PASSWORD=
""",
            "django": """
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://user:pass@localhost/dbname

# Static Files
STATIC_URL=/static/
MEDIA_URL=/media/
""",
            "react": """
# React Configuration
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_VERSION=1.0.0

# Environment
NODE_ENV=development
PORT=3000
""",
            "node": """
# Node.js Configuration
NODE_ENV=development
PORT=3000

# Database
MONGODB_URI=mongodb://localhost:27017/myapp

# JWT
JWT_SECRET=your-jwt-secret
JWT_EXPIRE=30d

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
"""
        }

        return templates.get(project_type, f"# {project_type} Configuration\n# Add your environment variables here\n")

    def load_env_file(self, path: str) -> Dict:
        """加载.env文件"""
        env_vars = {}
        if Path(path).exists():
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        return env_vars

    def save_env_file(self, env_vars: Dict, path: str):
        """保存.env文件"""
        with open(path, 'w', encoding='utf-8') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")


def create_manager(**kwargs) -> EnvManager:
    """创建环境变量管理器"""
    return EnvManager(**kwargs)


if __name__ == "__main__":
    manager = create_manager()

    print("Env Manager")
    print()

    # 测试
    template = manager.generate_template("fastapi")
    print(template)
