data strodtures:

As **data structures mais comuns em Competitive Programming** são:

## 1. Arrays / Vetores

Estrutura mais básica e mais usada.

Usos comuns:

```cpp
vector<int> a;
int arr[100005];
```

Serve para:

```txt
armazenar listas
fazer prefix sum
ordenar dados
acesso rápido por índice
```

Complexidades:

```txt
Acesso por índice: O(1)
Inserção no fim: O(1) amortizado
Busca linear: O(n)
```

---

## 2. String

Muito usada em problemas de texto.

Usos comuns:

```cpp
string s;
```

Serve para:

```txt
palíndromos
substrings
comparação lexicográfica
matching de padrões
```

Algoritmos relacionados:

```txt
KMP
Z-Algorithm
Hash de String
Trie
Suffix Array
```

---

## 3. Stack

Pilha: último que entra é o primeiro que sai.

```cpp
stack<int> st;
```

Serve para:

```txt
parênteses balanceados
monotonic stack
DFS iterativo
histograma máximo
next greater element
```

Complexidades:

```txt
push: O(1)
pop: O(1)
top: O(1)
```

---

## 4. Queue

Fila: primeiro que entra é o primeiro que sai.

```cpp
queue<int> q;
```

Serve para:

```txt
BFS
simulações
processamento em ordem
```

Complexidades:

```txt
push: O(1)
pop: O(1)
front: O(1)
```

---

## 5. Deque

Fila de duas pontas.

```cpp
deque<int> dq;
```

Serve para:

```txt
sliding window maximum/minimum
0-1 BFS
monotonic queue
```

Complexidades:

```txt
push_front: O(1)
push_back: O(1)
pop_front: O(1)
pop_back: O(1)
```

---

## 6. Priority Queue / Heap

Estrutura para sempre pegar o maior ou menor elemento rapidamente.

```cpp
priority_queue<int> pq; // max heap
priority_queue<int, vector<int>, greater<int>> pq; // min heap
```

Serve para:

```txt
Dijkstra
K maiores/menores elementos
simulações com prioridades
Huffman
greedy
```

Complexidades:

```txt
push: O(log n)
pop: O(log n)
top: O(1)
```

---

## 7. Set

Conjunto ordenado sem elementos repetidos.

```cpp
set<int> s;
```

Serve para:

```txt
buscar elementos únicos
manter dados ordenados
lower_bound / upper_bound
problemas com intervalos
```

Complexidades:

```txt
insert: O(log n)
erase: O(log n)
find: O(log n)
lower_bound: O(log n)
```

---

## 8. Multiset

Igual ao `set`, mas permite repetição.

```cpp
multiset<int> ms;
```

Serve para:

```txt
manter valores ordenados com repetição
mediana dinâmica
sliding window median
```

Complexidades:

```txt
insert: O(log n)
erase: O(log n)
find: O(log n)
```

---

## 9. Map

Dicionário ordenado por chave.

```cpp
map<string, int> mp;
```

Serve para:

```txt
contagem de frequência
compressão de valores
associar chave → valor
manter chaves ordenadas
```

Complexidades:

```txt
insert: O(log n)
access: O(log n)
find: O(log n)
```

---

## 10. Unordered Map

Hash map. Mais rápido na média, mas não ordenado.

```cpp
unordered_map<string, int> mp;
```

Serve para:

```txt
contagem rápida
busca por chave
memoization
```

Complexidades médias:

```txt
insert: O(1)
access: O(1)
find: O(1)
```

Pior caso:

```txt
O(n)
```

---

## 11. Unordered Set

Conjunto usando hash.

```cpp
unordered_set<int> s;
```

Serve para:

```txt
verificar existência rapidamente
remover duplicatas
busca média O(1)
```

Complexidades médias:

```txt
insert: O(1)
erase: O(1)
find: O(1)
```

---

## 12. Pair / Tuple

Estruturas para guardar múltiplos valores juntos.

```cpp
pair<int, int> p;
tuple<int, int, string> t;
```

Serve para:

```txt
coordenadas
arestas de grafo
ordenar por múltiplos critérios
retornar múltiplos valores
```

Exemplo:

```cpp
vector<pair<int, int>> edges;
```

---

## 13. Graph com Lista de Adjacência

Estrutura padrão para grafos.

```cpp
vector<int> adj[N];
```

Ou com peso:

```cpp
vector<pair<int, int>> adj[N]; // vizinho, peso
```

Serve para:

```txt
DFS
BFS
Dijkstra
Topological Sort
MST
componentes conectados
```

Complexidade de travessia:

```txt
O(V + E)
```

---

## 14. Union-Find / DSU

Estrutura para componentes disjuntos.

```txt
Disjoint Set Union
```

Serve para:

```txt
Kruskal
componentes conectados
detectar ciclos
queries de união
```

Operações:

```txt
find(x)
union(a, b)
```

Complexidade:

```txt
quase O(1), usando path compression + union by size/rank
```

---

## 15. Fenwick Tree / Binary Indexed Tree

Estrutura para soma em prefixos com atualização eficiente.

Serve para:

```txt
range sum query
point update
inversion count
frequency dinâmica
```

Operações:

```txt
update(index, value): O(log n)
query(prefix): O(log n)
range_query(l, r): O(log n)
```

---

## 16. Segment Tree

Estrutura mais flexível que Fenwick Tree.

Serve para:

```txt
range sum
range minimum
range maximum
range gcd
lazy propagation
range update
```

Complexidades:

```txt
build: O(n)
query: O(log n)
update: O(log n)
```

Com lazy propagation:

```txt
range update: O(log n)
range query: O(log n)
```

---

## 17. Sparse Table

Estrutura para queries estáticas em intervalo.

Serve para:

```txt
range minimum query
range maximum query
range gcd
```

Boa quando o array não muda.

Complexidades:

```txt
build: O(n log n)
query RMQ: O(1)
```

---

## 18. Trie

Árvore de prefixos.

Serve para:

```txt
dicionários
autocomplete
prefix matching
problemas com bits
maximum xor pair
```

Complexidade:

```txt
insert: O(tamanho da string)
search: O(tamanho da string)
```

---

## 19. Bitset

Estrutura compacta para bits.

```cpp
bitset<1000> b;
```

Serve para:

```txt
otimização com bits
subset problems
DP com bitset
operações booleanas rápidas
```

Operações comuns:

```cpp
b.set(i);
b.reset(i);
b.test(i);
b.count();
```

---

## 20. Ordered Set / Policy Based Data Structure

Estrutura avançada do GNU C++.

```cpp
tree<int, null_type, less<int>, rb_tree_tag, tree_order_statistics_node_update>
```

Serve para:

```txt
achar k-ésimo menor
contar quantos elementos são menores que x
queries de ordem
```

Operações:

```txt
find_by_order(k): O(log n)
order_of_key(x): O(log n)
```

Muito útil em problemas avançados.

---

# Resumo prático

As que você mais deve dominar primeiro:

```txt
vector
string
stack
queue
deque
priority_queue
set
map
unordered_map
graph adjacency list
DSU
Fenwick Tree
Segment Tree
```

Ordem boa de estudo:

```txt
1. vector, string, pair
2. stack, queue, deque
3. map, set, unordered_map
4. priority_queue
5. graph adjacency list
6. DSU
7. Fenwick Tree
8. Segment Tree
9. Trie
10. Sparse Table
11. Ordered Set
```

Para competir bem, o núcleo principal é:

```txt
Array + Hash Map + Set + Heap + Graph + DSU + Segment Tree
```
