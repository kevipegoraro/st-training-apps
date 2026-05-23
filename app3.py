from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import streamlit as st


# ============================================================
# 1. DICTIONARY / HASH MAP
# ============================================================

def run_dictionary_example() -> dict:
    """
    Example:
    Count how many times each word appears in a list.

    Competitive programming use:
    - Frequency counting
    - Fast lookup
    - Mapping one value to another
    """

    words = ["apple", "banana", "apple", "orange", "banana", "apple"]

    frequency: dict[str, int] = {}

    for word in words:
        if word not in frequency:
            frequency[word] = 0

        frequency[word] += 1

    return {
        "input": words,
        "frequency_map": frequency,
        "apple_count": frequency.get("apple", 0),
        "grape_count": frequency.get("grape", 0),
    }


# ============================================================
# 2. SET
# ============================================================

def run_set_example() -> dict:
    """
    Example:
    Find unique numbers and intersection between two lists.

    Competitive programming use:
    - Remove duplicates
    - Check if an item exists quickly
    - Find common elements
    """

    numbers_a = [1, 2, 3, 4, 4, 5, 5]
    numbers_b = [4, 5, 6, 7, 8]

    set_a = set(numbers_a)
    set_b = set(numbers_b)

    return {
        "list_a": numbers_a,
        "list_b": numbers_b,
        "unique_a": sorted(set_a),
        "unique_b": sorted(set_b),
        "intersection": sorted(set_a.intersection(set_b)),
        "union": sorted(set_a.union(set_b)),
        "is_3_in_a": 3 in set_a,
        "is_10_in_a": 10 in set_a,
    }


# ============================================================
# 3. STACK
# ============================================================

def run_stack_example() -> dict:
    """
    Example:
    Check if parentheses are balanced.

    Competitive programming use:
    - Parentheses validation
    - Undo logic
    - DFS traversal
    - Last In, First Out behavior
    """

    expression = "{[()]}"

    stack: list[str] = []
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    is_balanced = True

    for char in expression:
        if char in "([{":
            stack.append(char)

        elif char in ")]}":
            if not stack:
                is_balanced = False
                break

            top = stack.pop()

            if top != pairs[char]:
                is_balanced = False
                break

    if stack:
        is_balanced = False

    return {
        "expression": expression,
        "final_stack": stack,
        "is_balanced": is_balanced,
    }


# ============================================================
# 4. BINARY SEARCH TREE
# ============================================================

@dataclass
class TreeNode:
    value: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def insert_bst(root: Optional[TreeNode], value: int) -> TreeNode:
    if root is None:
        return TreeNode(value=value)

    if value < root.value:
        root.left = insert_bst(root.left, value)
    elif value > root.value:
        root.right = insert_bst(root.right, value)

    return root


def search_bst(root: Optional[TreeNode], target: int) -> bool:
    if root is None:
        return False

    if root.value == target:
        return True

    if target < root.value:
        return search_bst(root.left, target)

    return search_bst(root.right, target)


def inorder_traversal(root: Optional[TreeNode]) -> list[int]:
    if root is None:
        return []

    return (
        inorder_traversal(root.left)
        + [root.value]
        + inorder_traversal(root.right)
    )


def run_binary_search_tree_example() -> dict:
    """
    Example:
    Insert numbers into a Binary Search Tree and search values.

    Competitive programming use:
    - Ordered data
    - Searching
    - Tree traversal
    - Recursive thinking
    """

    values = [50, 30, 70, 20, 40, 60, 80]

    root: Optional[TreeNode] = None

    for value in values:
        root = insert_bst(root, value)

    return {
        "inserted_values": values,
        "inorder_traversal_sorted": inorder_traversal(root),
        "search_60": search_bst(root, 60),
        "search_99": search_bst(root, 99),
    }


# ============================================================
# 5. MERGE SORT
# ============================================================

def merge_sort(numbers: list[int]) -> list[int]:
    if len(numbers) <= 1:
        return numbers

    middle = len(numbers) // 2

    left = merge_sort(numbers[:middle])
    right = merge_sort(numbers[middle:])

    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    result: list[int] = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def run_merge_sort_example() -> dict:
    """
    Example:
    Sort an array using Merge Sort.

    Competitive programming use:
    - Sorting
    - Divide and conquer
    - Stable sorting logic
    - Foundation for inversion count problems
    """

    numbers = [9, 3, 7, 1, 8, 2, 5]

    sorted_numbers = merge_sort(numbers)

    return {
        "original_numbers": numbers,
        "sorted_numbers": sorted_numbers,
    }


# ============================================================
# STREAMLIT APP
# ============================================================

def show_code_block(title: str, code: str) -> None:
    st.subheader(title)
    st.code(code, language="python")


def main() -> None:
    st.set_page_config(
        page_title="Competitive Programming Data Structures",
        layout="wide",
    )

    st.title("Competitive Programming Data Structures")
    st.caption(
        "Simple examples of common data structures and algorithms used in competitive programming."
    )

    tab_dict, tab_set, tab_stack, tab_tree, tab_merge = st.tabs(
        [
            "Dictionary / Hash Map",
            "Set",
            "Stack",
            "Binary Search Tree",
            "Merge Sort",
        ]
    )

    # --------------------------------------------------------
    # Dictionary / Hash Map
    # --------------------------------------------------------

    with tab_dict:
        st.header("Dictionary / Hash Map")

        st.write(
            """
            A dictionary stores data as key-value pairs.

            Common uses:
            - Count frequency
            - Fast search by key
            - Map one value to another
            """
        )

        show_code_block(
            "Example code",
            """
words = ["apple", "banana", "apple", "orange", "banana", "apple"]

frequency = {}

for word in words:
    if word not in frequency:
        frequency[word] = 0

    frequency[word] += 1

print(frequency)
""".strip(),
        )

        if st.button("Run dictionary example", key="run_dict"):
            result = run_dictionary_example()

            st.success("Dictionary example executed.")
            st.json(result)

            st.write("Frequency table:")
            rows = [
                {"Word": word, "Count": count}
                for word, count in result["frequency_map"].items()
            ]
            st.dataframe(rows, use_container_width=True, hide_index=True)

    # --------------------------------------------------------
    # Set
    # --------------------------------------------------------

    with tab_set:
        st.header("Set")

        st.write(
            """
            A set stores unique values.

            Common uses:
            - Remove duplicates
            - Check membership quickly
            - Find intersection and union
            """
        )

        show_code_block(
            "Example code",
            """
numbers_a = [1, 2, 3, 4, 4, 5, 5]
numbers_b = [4, 5, 6, 7, 8]

set_a = set(numbers_a)
set_b = set(numbers_b)

intersection = set_a.intersection(set_b)
union = set_a.union(set_b)

print(intersection)
print(union)
""".strip(),
        )

        if st.button("Run set example", key="run_set"):
            result = run_set_example()

            st.success("Set example executed.")
            st.json(result)

    # --------------------------------------------------------
    # Stack
    # --------------------------------------------------------

    with tab_stack:
        st.header("Stack")

        st.write(
            """
            A stack follows the Last In, First Out rule.

            Common uses:
            - Validate parentheses
            - Undo operations
            - Depth-first search
            - Expression parsing
            """
        )

        show_code_block(
            "Example code",
            """
expression = "{[()]}"

stack = []
pairs = {
    ")": "(",
    "]": "[",
    "}": "{",
}

is_balanced = True

for char in expression:
    if char in "([{":
        stack.append(char)

    elif char in ")]}":
        if not stack:
            is_balanced = False
            break

        top = stack.pop()

        if top != pairs[char]:
            is_balanced = False
            break

if stack:
    is_balanced = False

print(is_balanced)
""".strip(),
        )

        if st.button("Run stack example", key="run_stack"):
            result = run_stack_example()

            st.success("Stack example executed.")
            st.json(result)

            if result["is_balanced"]:
                st.info("The expression is balanced.")
            else:
                st.warning("The expression is not balanced.")

    # --------------------------------------------------------
    # Binary Search Tree
    # --------------------------------------------------------

    with tab_tree:
        st.header("Binary Search Tree")

        st.write(
            """
            A Binary Search Tree stores smaller values on the left and larger values on the right.

            Common uses:
            - Search values
            - Ordered traversal
            - Tree recursion
            """
        )

        show_code_block(
            "Example code",
            """
values = [50, 30, 70, 20, 40, 60, 80]

root = None

for value in values:
    root = insert_bst(root, value)

print(inorder_traversal(root))
print(search_bst(root, 60))
print(search_bst(root, 99))
""".strip(),
        )

        if st.button("Run binary search tree example", key="run_tree"):
            result = run_binary_search_tree_example()

            st.success("Binary Search Tree example executed.")
            st.json(result)

            st.write("Inorder traversal returns the values sorted:")
            st.dataframe(
                [{"Position": index, "Value": value}
                 for index, value in enumerate(result["inorder_traversal_sorted"], start=1)],
                use_container_width=True,
                hide_index=True,
            )

    # --------------------------------------------------------
    # Merge Sort
    # --------------------------------------------------------

    with tab_merge:
        st.header("Merge Sort")

        st.write(
            """
            Merge Sort is a divide-and-conquer sorting algorithm.

            Common uses:
            - Sorting arrays
            - Learning recursion
            - Inversion count problems
            """
        )

        show_code_block(
            "Example code",
            """
def merge_sort(numbers):
    if len(numbers) <= 1:
        return numbers

    middle = len(numbers) // 2

    left = merge_sort(numbers[:middle])
    right = merge_sort(numbers[middle:])

    return merge(left, right)
""".strip(),
        )

        if st.button("Run merge sort example", key="run_merge"):
            result = run_merge_sort_example()

            st.success("Merge Sort example executed.")
            st.json(result)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Original")
                st.write(result["original_numbers"])

            with col2:
                st.subheader("Sorted")
                st.write(result["sorted_numbers"])

    st.divider()

    st.subheader("How to run")

    st.code(
        """
pip install streamlit
streamlit run app.py
""".strip(),
        language="bash",
    )


if __name__ == "__main__":
    main()

#streamlit run app.py