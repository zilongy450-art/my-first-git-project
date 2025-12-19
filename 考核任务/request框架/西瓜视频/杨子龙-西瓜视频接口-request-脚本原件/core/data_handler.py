import re
import json  # 新增：用于把 dict 转成 JSON 字符串（兜底）

from utils.logger import logger


class DataHandler:
    """
    数据处理工具类
    """

    def __init__(self):
        self.variables = {}

    def set_variable(self, key, value):
        """
        设置变量

        Args:
            key (str): 变量名
            value (str): 变量值
        """
        self.variables[key] = value
        logger.info(f"设置变量: {key} = {value}")
        logger.debug(f"当前所有变量: {self.variables}")

    def get_variable(self, key):
        """
        获取变量值

        Args:
            key (str): 变量名

        Returns:
            str: 变量值
        """
        value = self.variables.get(key, '')
        logger.debug(f"获取变量: {key} = {value}")
        return value

    def replace_variables(self, text):
        """
        替换文本中的变量占位符，支持${variable_name}和{{variable_name}}两种格式，兼容全角字符

        Args:
            text (str): 包含变量占位符的文本

        Returns:
            str: 替换变量后的文本
        """
        if not isinstance(text, str):
            return text

        logger.debug(f"替换变量前的文本: {text}")

        # 处理全角字符转换为半角字符
        text = text.replace('｛', '{').replace('｝', '}')

        # 匹配 ${variable_name} 格式的变量占位符
        pattern1 = r'\$\{([^}]+)\}'
        matches1 = re.findall(pattern1, text)

        # 匹配 {{variable_name}} 格式的变量占位符
        pattern2 = r'\{\{([^}]+)\}\}'
        matches2 = re.findall(pattern2, text)

        result = text
        # 处理 ${variable_name} 格式
        for match in matches1:
            variable_value = self.get_variable(match)
            if variable_value:
                result = result.replace('${' + match + '}', variable_value)
                logger.debug(f"替换变量 {match} 为 {variable_value}")
            else:
                logger.warning(f"变量 {match} 未找到")

        # 处理 {{variable_name}} 格式
        for match in matches2:
            variable_value = self.get_variable(match)
            if variable_value:
                result = result.replace('{{' + match + '}}', variable_value)
                logger.debug(f"替换变量 {match} 为 {variable_value}")
            else:
                logger.warning(f"变量 {match} 未找到")

        logger.debug(f"替换变量后的文本: {result}")
        return result

    def extract_value(self, response_data, extract_key):
        """
        从响应数据中提取值，支持多值提取（用分号分隔）
        支持语法:
          - "var1=key1; var2=key2"
          - "var1=path[0].field; var2=path2.field"
          - "var1=regex:正则表达式"
          - "var1=regex:..., var2=..."
        """
        if not extract_key:
            logger.debug("提取键为空，返回空字符串")
            return ''

        extract_key = str(extract_key).strip()
        logger.debug(f"开始提取值，提取规则: {extract_key}")

        # 如果包含 ';' 或 '='，按多条规则处理，返回 dict
        if ';' in extract_key or '=' in extract_key:
            results = {}
            # 多条规则用 ; 分隔，比如 "a=b; c=regex:xxx"
            rules = [r.strip() for r in extract_key.split(';') if r.strip()]
            for rule in rules:
                if '=' in rule:
                    # 支持别名赋值，如 "list_id1=regex:..."
                    alias, actual_key = rule.split('=', 1)
                    alias = alias.strip()
                    actual_key = actual_key.strip()
                    value = self._extract_single_value(response_data, actual_key)
                    if value != '':
                        results[alias] = value
                        logger.info(f"提取变量 {alias} = {value}")
                    else:
                        logger.warning(f"未能提取到变量 {alias} (规则: {actual_key})")
                else:
                    # 没有别名时，使用自身作为键名
                    key = rule.strip()
                    value = self._extract_single_value(response_data, key)
                    if value != '':
                        results[key] = value
                        logger.info(f"提取变量 {key} = {value}")
                    else:
                        logger.warning(f"未能提取到变量 {key}")
            return results
        else:
            # 保持原有单值提取逻辑，返回一个字符串
            return self._extract_single_value(response_data, extract_key)

    def _extract_single_value(self, response_data, extract_key):
        """
        从响应数据中提取值

        Args:
            response_data (dict|list|str): 响应数据（可以是 JSON 对象或字符串）
            extract_key (str): 提取键 / 正则 或 JSON 路径

        Returns:
            str: 提取到的值（字符串），提取失败返回空字符串
        """
        if not extract_key:
            logger.debug("提取键为空，返回空字符串")
            return ''

        logger.debug(f"开始提取值，提取键: {extract_key}")
        logger.debug(f"响应数据: {response_data}")

        try:
            # 处理正则表达式提取 (支持大小写 regex: / REGEX: 等)
            if extract_key.lower().startswith('regex:'):
                pattern = extract_key[len('regex:'):]  # 去掉前缀
                logger.debug(f"使用正则表达式提取: {pattern}")

                # ★★ 关键修复点：优先对 html 字段做正则匹配 ★★
                if isinstance(response_data, dict):
                    if 'html' in response_data and isinstance(response_data['html'], str):
                        # 这里拿到的就是你日志里那整段 HTML，没有 \n、\t 的转义问题
                        text = response_data['html']
                    else:
                        # 兜底：整个 dict 转成 JSON 字符串
                        try:
                            text = json.dumps(response_data, ensure_ascii=False)
                        except Exception:
                            text = str(response_data)
                elif isinstance(response_data, str):
                    text = response_data
                else:
                    text = str(response_data)

                # 给个 DOTALL 标志，万一以后你用 .*
                match = re.search(pattern, text, re.S)
                if match:
                    extracted_value = match.group(1) if match.groups() else match.group(0)
                    logger.info(f"正则表达式提取成功: {extract_key} -> {extracted_value}")
                    return str(extracted_value)
                else:
                    logger.warning(f"正则表达式 {pattern} 未匹配到内容")
                    return ''

            # 处理 JSON 路径提取
            else:
                logger.debug(f"使用JSON路径提取: {extract_key}")

                # 将 extract_key 按照数组索引和对象属性分离
                parts = re.findall(r'[^.\[\]]+|\[\d+\]', extract_key)
                value = response_data

                for part in parts:
                    if part.startswith('[') and part.endswith(']'):
                        # 处理数组索引 [index]
                        index = int(part[1:-1])
                        if isinstance(value, list) and 0 <= index < len(value):
                            value = value[index]
                        else:
                            logger.warning(f"JSON路径 {extract_key} 数组索引越界或类型错误")
                            return ''
                    else:
                        # 处理普通键访问
                        if isinstance(value, dict) and part in value:
                            value = value[part]
                        else:
                            logger.warning(f"JSON路径 {extract_key} 未找到键 {part}")
                            return ''

                extracted_value = str(value)
                logger.info(f"JSON路径提取成功: {extract_key} -> {extracted_value}")
                return extracted_value

        except Exception as e:
            logger.error(f"提取值失败: {str(e)}")
            return ''

    def clear_global_vars(self):
        """
        清空全局变量
        """
        self.variables.clear()
        logger.debug("清空全局变量")

    def get_all_variables(self):
        """
        获取所有变量

        Returns:
            dict: 所有变量
        """
        logger.debug(f"获取所有变量: {self.variables}")
        return self.variables
