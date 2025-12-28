from base.data import Data
from base.verifier import Verifier
import re


def _fuzzy_match(prediction: str, reference: str) -> bool:
    """模糊匹配函数"""
    prediction = prediction.strip()
    reference = reference.strip()

    if prediction == reference:
        return True

    # 处理选项格式: (a) vs a
    if len(prediction) == 3 and prediction[0] == "(" and prediction[-1] == ")":
        return prediction[1].lower() == reference.lower()
    if len(reference) == 3 and reference[0] == "(" and reference[-1] == ")":
        return reference[1].lower() == prediction.lower()

    # 处理数字
    try:
        if float(prediction) == float(reference):
            return True
    except ValueError:
        pass

    # 处理引号问题
    if prediction.replace("'", "") == reference.replace("'", ""):
        return True

    # 处理方括号问题
    if f"[{reference}]" == prediction or f"[{prediction}]" == reference:
        return True

    # 处理问号问题
    if prediction.endswith("?") and prediction[:-1] == reference:
        return True

    return False


def _preprocess_answer(answer: str) -> str:
    """预处理答案文本"""
    if not answer:
        return ""

    processed = answer.strip().lower()
    last_box_index = processed.rfind("\\boxed{")

    if last_box_index == -1:
        return ""
    processed = processed[last_box_index:]

    # 在截取的子字符串中进行正则匹配
    box_pattern = r'\\boxed\{([^}]*)\}'
    match = re.search(box_pattern, processed)
    if match:
        return match.group(1).strip()

    return ""


class GPQAVerifier(Verifier):
    """GPQA任务的验证器"""

    def verify(self, data: Data, test_solution: str) -> float:
        try:
            # 提取和预处理模型答案
            test_answer = self.extract_answer(test_solution)

            # 获取并预处理参考答案
            ground_truth = data.answer.strip().lower()

            # 进行模糊匹配
            correct = _fuzzy_match(test_answer, ground_truth)

            return 1.0 if correct else 0.0
        except:
            return 0.0

    def extract_answer(self, test_solution: str) -> str:
        """从完整答案中提取最终答案"""

        return _preprocess_answer(test_solution)
