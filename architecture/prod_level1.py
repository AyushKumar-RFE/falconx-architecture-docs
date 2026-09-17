"""Level 1 — BigBash production (current-state baseline).

AWS grouping: Cloud → Account → Region → VPC → public/private subnets.
AZ CIDRs live on the Level 2 network diagram so this stays one-page.
"""

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.aws.compute import ECR, EKS, Lambda, EC2AutoScaling
from diagrams.aws.database import Aurora, ElastiCache
from diagrams.aws.integration import Eventbridge, SQS
from diagrams.aws.management import SystemsManager
from diagrams.aws.network import CloudFront, NATGateway, NLB, Route53
from diagrams.aws.security import CertificateManager, SecretsManager, WAF
from diagrams.aws.storage import S3
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.client import Users
from diagrams.onprem.gitops import ArgoCD
from diagrams.onprem.monitoring import Sentry
from diagrams.onprem.network import Internet
from diagrams.onprem.vcs import Github

import aws_style as aws

OUT = Path(__file__).resolve().parents[1] / "docs" / "architecture"
OUT.mkdir(parents=True, exist_ok=True)

# Do not participate in ranking — keeps the request path as the spine.
OFF = Edge(style="dashed", constraint="false")


def render() -> None:
    path = str(OUT / "prod-level1")
    with Diagram(
        "BigBash production — current-state baseline",
        filename=path,
        show=False,
        direction="LR",
        graph_attr={**aws.GRAPH, "rankdir": "LR", "ranksep": "0.65", "nodesep": "0.35"},
        node_attr=aws.NODE,
        edge_attr=aws.EDGE,
        outformat=["svg", "png"],
    ):
        users = Users("Customers &\noperators")
        dns = Route53("Route 53\nbigbash.site")

        with Cluster("AWS Cloud", graph_attr=aws.CLOUD):
            with Cluster("Account 389068786427  ·  production", graph_attr=aws.ACCOUNT):
                with Cluster("us-east-1", graph_attr=aws.REGION):
                    waf = WAF("WAF\nCOUNT")
                    certs = CertificateManager("ACM")
                    cf = CloudFront("CloudFront")

                with Cluster("eu-west-2", graph_attr=aws.REGION):
                    with Cluster(
                        "VPC rfe-prod-vpc   10.30.0.0/16   3 AZs (2a/2b/2c)   single NAT",
                        graph_attr=aws.VPC,
                    ):
                        with Cluster("Public subnets", graph_attr=aws.PUBLIC_SUBNET):
                            nat = NATGateway("NAT Gateway")
                            bastion = SystemsManager("SSM bastion")

                        with Cluster("Private subnets", graph_attr=aws.PRIVATE_SUBNET):
                            nlb = NLB("Internal NLB\nTraefik / HTTPRoute")
                            with Cluster(
                                "EKS rfe-prod-cluster  1.35 Auto Mode",
                                graph_attr=aws.GROUP,
                            ):
                                eks = EKS("ns production")
                                karpenter = EC2AutoScaling("Karpenter")
                                argo = ArgoCD("Argo CD")
                            with Cluster("Data", graph_attr=aws.GROUP):
                                aurora = Aurora("Aurora PG 17\n+ RDS Proxy")
                                valkey = ElastiCache("Valkey")
                                msk = ManagedStreamingForKafka("MSK + Debezium")
                                aurora_da = Aurora("Aurora DA\n+ RDS Proxy")
                            with Cluster("Settlement · SAM", graph_attr=aws.GROUP):
                                bus = Eventbridge("EventBridge")
                                sqs = SQS("SQS")
                                lam = Lambda("Lambdas")

                    s3 = S3("S3 images")
                    ecr = ECR("ECR {service}-prod")
                    secrets = SecretsManager("config_prod_eu-west-2")

        github = Github("GitHub")
        gha = GithubActions("GitHub Actions")
        feeds = Internet("Betfair +\nfeeds")
        groundcover = Internet("Groundcover")
        sentry = Sentry("Sentry")

        # Spine: request path
        users >> dns >> waf >> cf
        certs >> OFF >> cf
        cf >> Edge(label="images") >> s3
        cf >> Edge(label="VPC origin") >> nlb >> eks

        # Inside cluster
        karpenter >> OFF >> eks
        argo >> OFF >> eks
        eks >> aurora
        eks >> valkey
        eks >> msk
        aurora >> Edge(label="outbox CDC") >> msk
        msk >> Edge(label="consume") >> aurora_da
        eks >> OFF >> bus >> sqs >> lam
        lam >> OFF >> aurora
        eks >> Edge(style="dashed", label="egress", constraint="false") >> nat
        bastion >> Edge(style="dashed", label="break-glass", constraint="false") >> aurora
        eks >> OFF >> secrets

        # Delivery
        github >> gha >> ecr
        gha >> Edge(label="image.tag") >> argo

        # External
        feeds >> OFF >> eks
        eks >> OFF >> groundcover
        eks >> OFF >> sentry


if __name__ == "__main__":
    render()
    print(f"wrote {OUT / 'prod-level1.svg'}")
