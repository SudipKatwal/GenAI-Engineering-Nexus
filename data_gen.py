import os


def generate_dummy_docs():
    if not os.path.exists("./data"):
        os.makedirs("./data")

    # 1. Engineering Doc: Payment API Spec
    api_doc = """
    # Payment Gateway API (v2.0)
    ## Authentication
    All requests must include the 'X-API-Key' header.
    ## Endpoints
    - POST /api/v2/charge: Initiates a transaction. Required fields: 'amount', 'currency', 'source_id'.
    - GET /api/v2/refund/{id}: Refunds a transaction. Only works for transactions < 30 days old.
    ## Rate Limits
    - Standard Tier: 100 req/min
    - Enterprise Tier: 1000 req/min
    """
    with open("./data/api_spec.txt", "w") as f:
        f.write(api_doc)

    # 2. Ops Doc: Server Runbook
    runbook = """
    # Runbook: High CPU Usage on Database Clusters
    ## Symptoms
    - Alert: 'DB_CPU_HIGH' triggers via PagerDuty.
    - Latency on /api/v2/charge exceeds 500ms.
    ## Mitigation Steps
    1. Check active queries: Run `SELECT * FROM pg_stat_activity WHERE state = 'active';`
    2. If a query is running > 60s, kill it using `SELECT pg_terminate_backend(pid);`
    3. If load persists, scale up the Read Replica fleet via Terraform: `terraform apply -target=aws_rds_cluster.read_replica`
    """
    with open("./data/runbook.txt", "w") as f:
        f.write(runbook)

    print("✅ Dummy technical documents generated in /data folder.")


if __name__ == "__main__":
    generate_dummy_docs()
