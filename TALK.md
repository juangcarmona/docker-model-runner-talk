Understood. Two artifacts. Same structure. Different cognitive roles.

Below is **exactly** what you asked for.

---

# TALK.md - Live Walkthrough (stage file)

> You **show this** in VS Code.
> You **do not read it**.
> Bullets = keywords only.

---

## INTRO - framing (no demo)

### What is Docker Model Runner

* Local runtime
* Docker-managed
* Models = artifacts
* CLI + HTTP
* Images/volumes mental model

### Why it exists

* Local AI: ad-hoc
* Too many runtimes
* GPU pain
* No standard

### What it is NOT

* Agents
* Orchestration
* Cloud inference
* Prod platform

---

## DEMO 1

## Let's try this:

```bash
docker model run smollm3:Q8_0 \
"Summarize in one sentence the difference between Machine Learning, Deep Learning, and Generative AI."
```

---

##  What just happened

* Local
* Docker
* No containers
* No keys
* Baseline

---

## Let's inspect the CLI

```bash
docker model
docker model ls
docker model status
```

* Artifacts
* Backend
* Visibility

---

## 03 - Inspect DMR on Docker Desktop

* Models tab
* Logs
* Resources
* No app containers

---

## 04 - Model lifecycle

```bash
docker model pull smollm3:Q8_0
```

```bash
docker model package --from ai/smollm3:Q8_0 --context-size 8192 jgc/smollm3:Q8_0_ctx8k
```

```bash
docker model run jgc/smollm3:Q8_0_ctx8k "Why does context size matter?"
```

* Context = artifact
* Predictable memory
* Reproducible

---

## 05 - VS Code client

* AI Kit
* Local endpoint
* Same model
* No keys

---


## DEMO 2 - with 'Real' clients

## Local Python app

> > > # **Demo time!**

### Containerized app (CPU)

* App container
* Host runner
* Env config
* No code change

> NOTE: No history in chat --> **THAT IS WHY CONTEXT MATTERS!!**

## DEMO 3 - CPU vs GPU --> Here we go!

```bash
docker model status
docker model run jgc/smollm3:Q8_0_ctx8k "Same question, faster execution."
```

* Same model
* Same CLI
* GPU backend
* Latency

---

## CLOSE

* Models = infra
* Docker = contract
* One runtime
* Many clients

---

## Questions?



