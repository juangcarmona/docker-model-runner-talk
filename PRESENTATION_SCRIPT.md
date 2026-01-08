## PRESENTATION_SCRIPT.md

---

### 01 — Why Docker Model Runner

* Local model execution used to be:
  * fragile
  * ad-hoc
  * non-reproducible
* We already solved this class of problems --> with containers
* DMR applies **Docker discipline to model execution**
* Models become managed local resources

---

### 02 — What DMR is

* Docker-managed local model **runtime**
* Exposed via:
  * CLI
  * local HTTP
* Models ≠ containers
* Execution ≠ `docker run`

#### It is Not:

* agents
* orchestration
* cloud inference

---

### 03 — Enable it (Docker Desktop)

* Docker Desktop → AI → Model Runner
* Toggle on
* GPU toggle if available
* No manual CUDA install
* Docker owns the hardware boundary

---

### 04 — CLI: pull & run

```
docker model ls

docker model help

docker model pull smollm3:Q8_0

docker model pull gpt-oss
```

* Explicit model lifecycle
* Local storage
* Versioned artifacts

---

### 05 — Demo: local CPU run

```
docker model run smollm3:Q8_0 "What is Docker Model Runner? One sentence."

docker model run gpt-oss "What is Docker Model Runner? One sentence."

docker model run smollm3:Q8_0 "List three features of Docker Model Runner."

docker model run smollm3:Q8_0 "DMR: CLI or HTTP?"

docker model run smollm3:Q8_0 "Local AI: one benefit."
```

* Cold start
* Token streaming
* CPU-bound
* No visible containers

---

### 06 — Packaging a model with a larger context

```
 docker model package  --from ai/smollm3:Q8_0  --context-size 8192  jgc/smollm3:Q8_0_ctx8k
```

* Context is runtime state
* Same model, different execution
* No rebuilds
* Reproducibility 

---

### 07 — Demo: GPU execution

```
docker model run smollm3:Q8_0 --gpu \
  "Summarize the TCP state machine"
```

* Same command
* Faster throughput
* GPU visible in Docker Desktop

---

### 08 — Mental model (very short)

* Background runner service
* Models loaded on demand
* Shared execution backend
* CLI and HTTP are equivalent frontends

---

### 09 — HTTP endpoint

```
curl http://localhost:PORT/...
```

* Same model
* Same runtime
* Different interface
* Local only

---

### 10 — Demo: local app

* App calls `localhost`
* No keys
* No network
* Fully inspectable

Run it.

---

### 11 — Demo: Compose

* App in container
* Model runner on host
* No sidecars
* No agents

```
docker compose up
```

---

### 12 — Close

* Local-first AI is now practical
* DMR removes ceremony
* Models behave like infrastructure again
* Everything else is optional

---

### Why this version works

* ~12 sections = ~2–2.5 min each
* No redundancy
* No architecture deep dives
* No defensive explanations
* Every section maps to something *visible* in VS Code, terminal, or Docker Desktop

If you want, next we can:

* tune this to **exact commands you’ll run**
* pre-optimize pacing for live latency
* harden it against demo failure modes
