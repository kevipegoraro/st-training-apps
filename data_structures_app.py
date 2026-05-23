from __future__ import annotations

import bisect
import heapq
import random
import string
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from typing import Optional

import streamlit as st


# ============================================================
# GLOBAL RANDOM DATASETS
# ============================================================

RANDOM_SEED = 42
DATASET_SIZE = 1000

random.seed(RANDOM_SEED)


def generate_random_words(size: int) -> list[str]:
    words = []

    for _ in range(size):
        length = random.randint(3, 10)
        word = "".join(random.choices(string.ascii_lowercase, k=length))
        words.append(word)

    return words


def generate_random_pairs(size: int) -> list[tuple[int, int]]:
    return [
        (random.randint(1, 1000), random.randint(1, 1000))
        for _ in range(size)
    ]


def generate_random_edges(nodes_count: int, edges_count: int) -> list[tuple[int, int, int]]:
    edges = []

    for _ in range(edges_count):
        u = random.randint(1, nodes_count)
        v = random.randint(1, nodes_count)

        while v == u:
            v = random.randint(1, nodes_count)

        weight = random.randint(1, 100)
        edges.append((u, v, weight))

    return edges


DATA_NUMBERS = [random.randint(1, 10_000) for _ in range(DATASET_SIZE)]
DATA_WORDS = generate_random_words(DATASET_SIZE)
DATA_PAIRS = generate_random_pairs(DATASET_SIZE)
DATA_GRAPH_NODES = 100
DATA_GRAPH_EDGES = generate_random_edges(DATA_GRAPH_NODES, DATASET_SIZE)


# ============================================================
# BASIC HELPERS
# ============================================================

def show_dataset_preview() -> None:
    with st.expander("Dataset preview"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Numbers")
            st.write(DATA_NUMBERS[:20])

        with col2:
            st.write("Words")
            st.write(DATA_WORDS[:20])

        with col3:
            st.write("Pairs")
            st.write(DATA_PAIRS[:10])


def show_result(result: dict) -> None:
    st.json(result)


# ============================================================
# 1. VECTOR, STRING, PAIR
# ============================================================

def example_vector_string_pair() -> dict:
    numbers = DATA_NUMBERS
    words = DATA_WORDS
    pairs = DATA_PAIRS

    vector_sum = sum(numbers)
    vector_max = max(numbers)
    vector_min = min(numbers)
    first_10_sorted = sorted(numbers[:10])

    longest_word = max(words, key=len)
    words_starting_with_a = [word for word in words if word.startswith("a")]

    pairs_sorted_by_first_then_second = sorted(pairs[:20])
    pair_with_biggest_sum = max(pairs, key=lambda pair: pair[0] + pair[1])

    return {
        "vector_size": len(numbers),
        "vector_sum": vector_sum,
        "vector_min": vector_min,
        "vector_max": vector_max,
        "first_10_numbers": numbers[:10],
        "first_10_sorted": first_10_sorted,
        "string_count": len(words),
        "longest_word": longest_word,
        "words_starting_with_a_count": len(words_starting_with_a),
        "sample_words_starting_with_a": words_starting_with_a[:10],
        "first_20_pairs_sorted": pairs_sorted_by_first_then_second,
        "pair_with_biggest_sum": pair_with_biggest_sum,
    }


# ============================================================
# 2. STACK, QUEUE, DEQUE
# ============================================================

def example_stack_queue_deque() -> dict:
    sample = DATA_NUMBERS[:20]

    stack: list[int] = []
    for value in sample:
        stack.append(value)

    stack_popped = []
    while stack:
        stack_popped.append(stack.pop())

    queue = deque()
    for value in sample:
        queue.append(value)

    queue_popped = []
    while queue:
        queue_popped.append(queue.popleft())

    double_ended_queue = deque(sample)
    deque_operations = {
        "initial_front": double_ended_queue[0],
        "initial_back": double_ended_queue[-1],
    }

    double_ended_queue.appendleft(999)
    double_ended_queue.append(888)

    deque_as_list = list(double_ended_queue)

    deque_operations["after_appendleft_and_append"] = (
        deque_as_list[:5] + ["..."] + deque_as_list[-5:]
    )

    deque_operations["pop_front"] = double_ended_queue.popleft()
    deque_operations["pop_back"] = double_ended_queue.pop()

    return {
        "input_sample": sample,
        "stack_lifo_result": stack_popped,
        "queue_fifo_result": queue_popped,
        "deque_operations": deque_operations,
    }


# ============================================================
# 3. MAP, SET, UNORDERED_MAP
# ============================================================

def example_map_set_unordered_map() -> dict:
    numbers = DATA_NUMBERS
    words = DATA_WORDS

    ordered_map_like = dict(sorted(Counter(numbers).items()))
    set_unique_numbers = set(numbers)
    unordered_map_like = Counter(words)

    most_common_words = unordered_map_like.most_common(10)

    return {
        "numbers_count": len(numbers),
        "unique_numbers_count": len(set_unique_numbers),
        "first_10_unique_sorted_numbers": sorted(set_unique_numbers)[:10],
        "map_like_first_10_items_sorted_by_key": list(ordered_map_like.items())[:10],
        "unordered_map_like_word_frequency_top_10": most_common_words,
        "word_lookup_example": {
            "word": words[0],
            "frequency": unordered_map_like[words[0]],
        },
    }


# ============================================================
# 4. PRIORITY QUEUE
# ============================================================

def example_priority_queue() -> dict:
    numbers = DATA_NUMBERS

    min_heap = []
    for value in numbers:
        heapq.heappush(min_heap, value)

    smallest_10 = [heapq.heappop(min_heap) for _ in range(10)]

    max_heap = []
    for value in numbers:
        heapq.heappush(max_heap, -value)

    largest_10 = [-heapq.heappop(max_heap) for _ in range(10)]

    tasks = [
        (random.randint(1, 100), f"task_{index}")
        for index in range(20)
    ]

    task_heap = []
    for priority, task_name in tasks:
        heapq.heappush(task_heap, (priority, task_name))

    first_5_tasks_by_priority = [heapq.heappop(task_heap) for _ in range(5)]

    return {
        "smallest_10_numbers": smallest_10,
        "largest_10_numbers": largest_10,
        "task_sample": tasks,
        "first_5_tasks_by_priority": first_5_tasks_by_priority,
    }


# ============================================================
# 5. GRAPH ADJACENCY LIST
# ============================================================

def build_adjacency_list(nodes_count: int, edges: list[tuple[int, int, int]]) -> dict[int, list[tuple[int, int]]]:
    graph: dict[int, list[tuple[int, int]]] = defaultdict(list)

    for u, v, weight in edges:
        graph[u].append((v, weight))
        graph[v].append((u, weight))

    return graph


def bfs(graph: dict[int, list[tuple[int, int]]], start: int) -> list[int]:
    visited = set()
    order = []
    queue = deque([start])
    visited.add(start)

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor, _weight in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def example_graph_adjacency_list() -> dict:
    graph = build_adjacency_list(DATA_GRAPH_NODES, DATA_GRAPH_EDGES)

    degree_by_node = {
        node: len(neighbors)
        for node, neighbors in graph.items()
    }

    top_10_highest_degree = sorted(
        degree_by_node.items(),
        key=lambda item: item[1],
        reverse=True,
    )[:10]

    bfs_order = bfs(graph, start=1)

    return {
        "nodes_count": DATA_GRAPH_NODES,
        "edges_count": len(DATA_GRAPH_EDGES),
        "neighbors_of_node_1_first_10": graph[1][:10],
        "top_10_nodes_by_degree": top_10_highest_degree,
        "bfs_from_node_1_first_30": bfs_order[:30],
        "reachable_nodes_from_1": len(bfs_order),
    }


# ============================================================
# 6. DSU / UNION FIND
# ============================================================

class DSU:
    def __init__(self, size: int):
        self.parent = list(range(size + 1))
        self.rank = [0] * (size + 1)
        self.component_size = [1] * (size + 1)

    def find(self, node: int) -> int:
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])

        return self.parent[node]

    def union(self, a: int, b: int) -> bool:
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_b] = root_a
        self.component_size[root_a] += self.component_size[root_b]

        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1

        return True

    def same_component(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)

    def size_of_component(self, node: int) -> int:
        return self.component_size[self.find(node)]


def example_dsu() -> dict:
    dsu = DSU(DATA_GRAPH_NODES)

    successful_unions = 0

    for u, v, _weight in DATA_GRAPH_EDGES:
        if dsu.union(u, v):
            successful_unions += 1

    components = defaultdict(list)

    for node in range(1, DATA_GRAPH_NODES + 1):
        components[dsu.find(node)].append(node)

    component_sizes = sorted(
        [len(nodes) for nodes in components.values()],
        reverse=True,
    )

    return {
        "nodes_count": DATA_GRAPH_NODES,
        "union_attempts": len(DATA_GRAPH_EDGES),
        "successful_unions": successful_unions,
        "components_count": len(components),
        "largest_component_sizes": component_sizes[:10],
        "are_1_and_50_connected": dsu.same_component(1, 50),
        "component_size_of_node_1": dsu.size_of_component(1),
    }


# ============================================================
# 7. FENWICK TREE
# ============================================================

class FenwickTree:
    def __init__(self, values: list[int]):
        self.size = len(values)
        self.tree = [0] * (self.size + 1)

        for index, value in enumerate(values, start=1):
            self.add(index, value)

    def add(self, index: int, delta: int) -> None:
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index

    def prefix_sum(self, index: int) -> int:
        total = 0

        while index > 0:
            total += self.tree[index]
            index -= index & -index

        return total

    def range_sum(self, left: int, right: int) -> int:
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


def example_fenwick_tree() -> dict:
    values = DATA_NUMBERS[:1000]
    fenwick = FenwickTree(values)

    left = 100
    right = 200

    old_value = values[149]
    new_value = old_value + 500
    delta = new_value - old_value

    fenwick.add(150, delta)
    values[149] = new_value

    return {
        "dataset_size": len(values),
        "prefix_sum_100": fenwick.prefix_sum(100),
        "range_sum_100_to_200": fenwick.range_sum(left, right),
        "updated_position": 150,
        "old_value": old_value,
        "new_value": new_value,
        "range_sum_140_to_160_after_update": fenwick.range_sum(140, 160),
    }


# ============================================================
# 8. SEGMENT TREE
# ============================================================

class SegmentTree:
    def __init__(self, values: list[int]):
        self.n = len(values)
        self.tree = [0] * (4 * self.n)
        self.values = values[:]
        self.build(1, 0, self.n - 1)

    def build(self, node: int, left: int, right: int) -> None:
        if left == right:
            self.tree[node] = self.values[left]
            return

        mid = (left + right) // 2
        self.build(node * 2, left, mid)
        self.build(node * 2 + 1, mid + 1, right)

        self.tree[node] = min(self.tree[node * 2], self.tree[node * 2 + 1])

    def range_min(self, query_left: int, query_right: int) -> int:
        return self._range_min(1, 0, self.n - 1, query_left, query_right)

    def _range_min(
        self,
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
    ) -> int:
        if query_right < left or right < query_left:
            return 10**18

        if query_left <= left and right <= query_right:
            return self.tree[node]

        mid = (left + right) // 2

        return min(
            self._range_min(node * 2, left, mid, query_left, query_right),
            self._range_min(node * 2 + 1, mid + 1, right, query_left, query_right),
        )

    def update(self, index: int, value: int) -> None:
        self._update(1, 0, self.n - 1, index, value)

    def _update(self, node: int, left: int, right: int, index: int, value: int) -> None:
        if left == right:
            self.tree[node] = value
            return

        mid = (left + right) // 2

        if index <= mid:
            self._update(node * 2, left, mid, index, value)
        else:
            self._update(node * 2 + 1, mid + 1, right, index, value)

        self.tree[node] = min(self.tree[node * 2], self.tree[node * 2 + 1])


def example_segment_tree() -> dict:
    values = DATA_NUMBERS[:1000]
    segment_tree = SegmentTree(values)

    left = 100
    right = 200

    range_min_before = segment_tree.range_min(left, right)

    segment_tree.update(150, -1)

    range_min_after = segment_tree.range_min(left, right)

    return {
        "dataset_size": len(values),
        "range_checked": [left, right],
        "range_min_before_update": range_min_before,
        "updated_index": 150,
        "updated_value": -1,
        "range_min_after_update": range_min_after,
    }


# ============================================================
# 9. TRIE
# ============================================================

@dataclass
class TrieNode:
    children: dict[str, "TrieNode"] = field(default_factory=dict)
    is_end: bool = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root

        for char in word:
            if char not in node.children:
                return False

            node = node.children[char]

        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root

        for char in prefix:
            if char not in node.children:
                return False

            node = node.children[char]

        return True

    def count_prefix(self, prefix: str) -> int:
        node = self.root

        for char in prefix:
            if char not in node.children:
                return 0

            node = node.children[char]

        return self._count_words_from_node(node)

    def _count_words_from_node(self, node: TrieNode) -> int:
        total = 1 if node.is_end else 0

        for child in node.children.values():
            total += self._count_words_from_node(child)

        return total


def example_trie() -> dict:
    trie = Trie()

    for word in DATA_WORDS:
        trie.insert(word)

    sample_word = DATA_WORDS[0]
    prefix = sample_word[:2]

    fake_word = "zzzzzzzzzz"

    return {
        "words_inserted": len(DATA_WORDS),
        "sample_word": sample_word,
        "search_sample_word": trie.search(sample_word),
        "search_fake_word": trie.search(fake_word),
        "prefix_used": prefix,
        "starts_with_prefix": trie.starts_with(prefix),
        "words_with_prefix_count": trie.count_prefix(prefix),
    }


# ============================================================
# 10. SPARSE TABLE
# ============================================================

class SparseTable:
    def __init__(self, values: list[int]):
        self.values = values
        self.n = len(values)
        self.log = [0] * (self.n + 1)

        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1

        max_log = self.log[self.n] + 1

        self.table = [
            [0] * self.n
            for _ in range(max_log)
        ]

        self.table[0] = values[:]

        j = 1
        while (1 << j) <= self.n:
            interval = 1 << j
            half = interval >> 1

            for i in range(self.n - interval + 1):
                self.table[j][i] = min(
                    self.table[j - 1][i],
                    self.table[j - 1][i + half],
                )

            j += 1

    def range_min(self, left: int, right: int) -> int:
        length = right - left + 1
        j = self.log[length]

        return min(
            self.table[j][left],
            self.table[j][right - (1 << j) + 1],
        )


def example_sparse_table() -> dict:
    values = DATA_NUMBERS[:1000]
    sparse_table = SparseTable(values)

    queries = [
        (0, 99),
        (100, 300),
        (250, 750),
        (700, 999),
    ]

    results = []

    for left, right in queries:
        results.append(
            {
                "range": [left, right],
                "sparse_table_min": sparse_table.range_min(left, right),
                "python_min_validation": min(values[left:right + 1]),
            }
        )

    return {
        "dataset_size": len(values),
        "operation": "Static Range Minimum Query",
        "queries": results,
    }


# ============================================================
# 11. ORDERED SET
# ============================================================

class OrderedSet:
    def __init__(self):
        self.data: list[int] = []

    def add(self, value: int) -> None:
        index = bisect.bisect_left(self.data, value)

        if index == len(self.data) or self.data[index] != value:
            self.data.insert(index, value)

    def remove(self, value: int) -> bool:
        index = bisect.bisect_left(self.data, value)

        if index < len(self.data) and self.data[index] == value:
            self.data.pop(index)
            return True

        return False

    def contains(self, value: int) -> bool:
        index = bisect.bisect_left(self.data, value)

        return index < len(self.data) and self.data[index] == value

    def lower_bound(self, value: int) -> Optional[int]:
        index = bisect.bisect_left(self.data, value)

        if index < len(self.data):
            return self.data[index]

        return None

    def upper_bound(self, value: int) -> Optional[int]:
        index = bisect.bisect_right(self.data, value)

        if index < len(self.data):
            return self.data[index]

        return None

    def kth(self, k: int) -> Optional[int]:
        if 0 <= k < len(self.data):
            return self.data[k]

        return None


def example_ordered_set() -> dict:
    ordered_set = OrderedSet()

    for value in DATA_NUMBERS:
        ordered_set.add(value)

    query_value = 5000

    removed_value = ordered_set.data[10]
    removed = ordered_set.remove(removed_value)

    return {
        "original_numbers_count": len(DATA_NUMBERS),
        "unique_ordered_count": len(ordered_set.data),
        "first_20_ordered_values": ordered_set.data[:20],
        "contains_5000": ordered_set.contains(query_value),
        "lower_bound_5000": ordered_set.lower_bound(query_value),
        "upper_bound_5000": ordered_set.upper_bound(query_value),
        "kth_0": ordered_set.kth(0),
        "kth_10": ordered_set.kth(10),
        "removed_value": removed_value,
        "removed_successfully": removed,
        "contains_removed_value_after_remove": ordered_set.contains(removed_value),
    }


# ============================================================
# STREAMLIT UI
# ============================================================

def main() -> None:
    st.set_page_config(
        page_title="Competitive Programming Structures",
        layout="wide",
    )

    st.title("Competitive Programming Structures")
    st.caption(
        "Interactive examples using Python equivalents of common competitive programming structures."
    )

    st.info(
        f"Global datasets generated at startup: "
        f"{DATASET_SIZE} numbers, {DATASET_SIZE} words, "
        f"{DATASET_SIZE} pairs, and {DATASET_SIZE} graph edges."
    )

    show_dataset_preview()

    tabs = st.tabs(
        [
            "1. vector, string, pair",
            "2. stack, queue, deque",
            "3. map, set, unordered_map",
            "4. priority_queue",
            "5. graph adjacency list",
            "6. DSU",
            "7. Fenwick Tree",
            "8. Segment Tree",
            "9. Trie",
            "10. Sparse Table",
            "11. Ordered Set",
        ]
    )

    with tabs[0]:
        st.header("1. vector, string, pair")
        st.write(
            """
            Python equivalents:
            - `vector` → `list`
            - `string` → `str`
            - `pair` → `tuple`
            """
        )

        st.code(
            """
numbers = [10, 20, 30]
word = "algorithm"
pair = (10, 20)

numbers.append(40)
word_length = len(word)
first_value, second_value = pair
""".strip(),
            language="python",
        )

        if st.button("Run vector, string, pair example"):
            show_result(example_vector_string_pair())

    with tabs[1]:
        st.header("2. stack, queue, deque")
        st.write(
            """
            Python equivalents:
            - `stack` → `list` with `append()` and `pop()`
            - `queue` → `collections.deque` with `append()` and `popleft()`
            - `deque` → `collections.deque`
            """
        )

        st.code(
            """
from collections import deque

stack = []
stack.append(10)
stack.pop()

queue = deque()
queue.append(10)
queue.popleft()

dq = deque()
dq.appendleft(1)
dq.append(2)
""".strip(),
            language="python",
        )

        if st.button("Run stack, queue, deque example"):
            show_result(example_stack_queue_deque())

    with tabs[2]:
        st.header("3. map, set, unordered_map")
        st.write(
            """
            Python equivalents:
            - `map` → `dict`, usually sorted manually when needed
            - `set` → `set`
            - `unordered_map` → `dict` or `collections.Counter`
            """
        )

        st.code(
            """
from collections import Counter

numbers = [1, 2, 2, 3]
frequency = Counter(numbers)

unique_values = set(numbers)
ordered_by_key = dict(sorted(frequency.items()))
""".strip(),
            language="python",
        )

        if st.button("Run map, set, unordered_map example"):
            show_result(example_map_set_unordered_map())

    with tabs[3]:
        st.header("4. priority_queue")
        st.write(
            """
            Python equivalent:
            - `priority_queue` → `heapq`

            Python has a min-heap by default.
            For max-heap behavior, insert negative values.
            """
        )

        st.code(
            """
import heapq

heap = []
heapq.heappush(heap, 50)
heapq.heappush(heap, 10)
heapq.heappush(heap, 30)

smallest = heapq.heappop(heap)
""".strip(),
            language="python",
        )

        if st.button("Run priority_queue example"):
            show_result(example_priority_queue())

    with tabs[4]:
        st.header("5. graph adjacency list")
        st.write(
            """
            A graph adjacency list stores each node with its connected neighbors.

            Common uses:
            - BFS
            - DFS
            - Dijkstra
            - Connected components
            """
        )

        st.code(
            """
graph = {
    1: [(2, 10), (3, 5)],
    2: [(1, 10)],
    3: [(1, 5)],
}
""".strip(),
            language="python",
        )

        if st.button("Run graph adjacency list example"):
            show_result(example_graph_adjacency_list())

    with tabs[5]:
        st.header("6. DSU")
        st.write(
            """
            DSU means Disjoint Set Union.

            Also called:
            - Union Find
            - Connected Components structure

            Common uses:
            - Kruskal MST
            - Dynamic connectivity
            - Grouping nodes
            """
        )

        st.code(
            """
dsu.union(1, 2)
dsu.union(2, 3)

dsu.same_component(1, 3)
""".strip(),
            language="python",
        )

        if st.button("Run DSU example"):
            show_result(example_dsu())

    with tabs[6]:
        st.header("7. Fenwick Tree")
        st.write(
            """
            Fenwick Tree is also called Binary Indexed Tree.

            Common uses:
            - Prefix sum
            - Range sum
            - Point update
            """
        )

        st.code(
            """
fenwick.add(index, delta)
prefix = fenwick.prefix_sum(index)
range_total = fenwick.range_sum(left, right)
""".strip(),
            language="python",
        )

        if st.button("Run Fenwick Tree example"):
            show_result(example_fenwick_tree())

    with tabs[7]:
        st.header("8. Segment Tree")
        st.write(
            """
            Segment Tree supports range queries and updates.

            This example uses:
            - Range minimum query
            - Point update
            """
        )

        st.code(
            """
segment_tree.range_min(left, right)
segment_tree.update(index, new_value)
""".strip(),
            language="python",
        )

        if st.button("Run Segment Tree example"):
            show_result(example_segment_tree())

    with tabs[8]:
        st.header("9. Trie")
        st.write(
            """
            Trie is a prefix tree.

            Common uses:
            - Word search
            - Prefix search
            - Autocomplete
            - Dictionary problems
            """
        )

        st.code(
            """
trie.insert("apple")
trie.search("apple")
trie.starts_with("app")
""".strip(),
            language="python",
        )

        if st.button("Run Trie example"):
            show_result(example_trie())

    with tabs[9]:
        st.header("10. Sparse Table")
        st.write(
            """
            Sparse Table is used for fast static range queries.

            This example uses:
            - Static Range Minimum Query
            - O(1) query after preprocessing
            - No updates
            """
        )

        st.code(
            """
sparse_table = SparseTable(values)
minimum = sparse_table.range_min(left, right)
""".strip(),
            language="python",
        )

        if st.button("Run Sparse Table example"):
            show_result(example_sparse_table())

    with tabs[10]:
        st.header("11. Ordered Set")
        st.write(
            """
            Python does not have a native ordered set like C++ PBDS.

            This simplified version uses:
            - sorted list
            - bisect
            - lower_bound
            - upper_bound
            - kth element

            For large production use, a balanced tree library is better.
            """
        )

        st.code(
            """
ordered_set.add(10)
ordered_set.add(20)

ordered_set.lower_bound(15)
ordered_set.upper_bound(15)
ordered_set.kth(0)
""".strip(),
            language="python",
        )

        if st.button("Run Ordered Set example"):
            show_result(example_ordered_set())

    st.divider()

    st.subheader("Run command")

    st.code(
        """
pip install streamlit
streamlit run app.py
""".strip(),
        language="bash",
    )


if __name__ == "__main__":
    main()