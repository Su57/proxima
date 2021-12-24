from typing import MutableSequence, List, Dict, Any

from src.exceptions import ProximaException
from src.core.web.schemas import TreeSchema


class TreeUtil:
    """ 树状结构工具类 """

    @classmethod
    def build_tree(cls, elements: MutableSequence[TreeSchema]) -> List[Dict[str, Any]]:
        """
        根据列表构建树结构。该列表的每个元素都需要拥有AbstractTreeSchema中的属性id、parent_id
        :param elements: 元素列表
        :return: 树列表
        """
        schemas: List[TreeSchema] = []
        for e in elements:
            # 从最高层级的对象开始进行遍历
            if e.parent_id is None:
                cls._recursion(e, elements)
                schemas.append(e)
        if len(schemas) == 0:
            raise ProximaException(description="找不到根节点")
        result: List[Dict[str, Any]] = []

        for schema in schemas:
            result.append(schema.dict(by_alias=True))
        return result

    @classmethod
    def _recursion(cls, node: TreeSchema, elements: MutableSequence[TreeSchema]) -> None:
        """
        递归处理。获取某个node的所有子节点。当前节点处理完后，应当将其从序列中移除以减少递归次数
        :param node: 当前节点
        :param elements: 所有节点
        :return:
        """
        elements.remove(node)
        for e in elements:
            # 获取当前所有子节点，并对子节点进行同样的操作
            if e.parent_id == node.id:
                node.children.append(e)
                cls._recursion(e, elements)
