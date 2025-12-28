from base.data import Data
from base.verifier import Verifier
import re
import collections


def _extract_sorted_words(answer_str, original_words):
    # Create regex pattern for words
    word_pattern = "|".join([f"\\b{w}\\b" for w in original_words])
    regex = re.compile(word_pattern)

    # Strict match pattern first
    strict_match = re.search(r'(?<=[the|The] answer is )(.*)(?=.)', answer_str)
    if strict_match:
        result = strict_match.group(1).strip()
        # Find all matching words in strict match
        strict_matches = regex.findall(result)
        if strict_matches:
            # Remove duplicates while preserving order
            strict_matches.reverse()
            ordered_words = reversed(collections.OrderedDict(zip(strict_matches, [None] * len(strict_matches))))
            return " ".join(ordered_words)

    # Fallback to flexible pattern
    flexible_matches = regex.findall(answer_str)
    if flexible_matches:
        # Remove duplicates while preserving order
        flexible_matches.reverse()
        ordered_words = reversed(collections.OrderedDict(zip(flexible_matches, [None] * len(flexible_matches))))
        return " ".join(ordered_words)

    return ""


class BBHWordSortingVerifier(Verifier):
    """
    Verifier for Word Sorting tasks
    """

    def verify(self, data: Data, test_solution: str):
        try:
            # 从输入中提取原始词列表
            original_words = data.question.split("List:")[1].split('\n')[0].strip().split()

            test_answer = self.extract_answer(test_solution, original_words)
            ground_truth = data.answer

            # 标准化答案格式：移除多余空格
            test_answer = ' '.join(test_answer.split())
            ground_truth = ' '.join(ground_truth.split())

            correct = test_answer == ground_truth
            if correct:
                acc_score = 1.0
            else:
                acc_score = 0

            return acc_score
        except:
            return False

    def extract_answer(self, test_solution: str, original_words):
        answer_str = test_solution
        return _extract_sorted_words(answer_str=answer_str, original_words=original_words)
