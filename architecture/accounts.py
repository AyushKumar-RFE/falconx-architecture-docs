"""Account and region layout — both AWS accounts at a glance."""

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EKS
from diagrams.aws.database import Aurora, ElastiCache
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.aws.network import CloudFront, VPC
from diagrams.aws.security import WAF
from diagrams.onprem.client import Users

import aws_style as aws

OUT = Path(__file__).resolve().parents[1] / "docs" / "architecture"
OUT.mkdir(parents=True, exist_ok=True)


def render() -> None:
    path = str(OUT / "accounts")
    with Diagram(
        "BigBash — AWS accounts and regions",
        filename=path,
        show=False,
        direction="LR",
        graph_attr=aws.GRAPH,
        node_attr=aws.NODE,
        edge_attr=aws.EDGE,
        outformat=["svg", "png"],
    ):
        users = Users("Users")

        with Cluster("AWS Cloud", graph_attr=aws.CLOUD):
            with Cluster(
                "us-east-1  ·  each account has its own WAF + CloudFront here",
                graph_attr=aws.REGION,
            ):
                waf = WAF("WAF")
                cf = CloudFront("CloudFront")

            with Cluster(
                "Account 460195068944  ·  develop + perf  ·  eu-west-2",
                graph_attr=aws.ACCOUNT,
            ):
                vpc_dev = VPC("rfe-dev-vpc\n10.10.0.0/16")
                with Cluster("rfe-dev-cluster", graph_attr=aws.GROUP):
                    ns_dev = EKS("ns development")
                    ns_perf = EKS("ns performance")
                shared = Aurora("shared Aurora + MSK")
                valkey_dev = ElastiCache("dev Valkey")
                valkey_perf = ElastiCache("perf Valkey")

            with Cluster(
                "Account 389068786427  ·  production  ·  eu-west-2",
                graph_attr=aws.ACCOUNT,
            ):
                vpc_prod = VPC("rfe-prod-vpc\n10.30.0.0/16")
                ns_prod = EKS("rfe-prod-cluster\nns production")
                data_prod = Aurora("own Aurora + MSK + Valkey")

        users >> waf >> cf
        cf >> Edge(label="*.bigbash.life") >> vpc_dev
        cf >> Edge(label="bigbash.site") >> vpc_prod
        vpc_dev >> ns_dev
        vpc_dev >> ns_perf
        ns_dev >> shared
        ns_perf >> shared
        ns_dev >> valkey_dev
        ns_perf >> valkey_perf
        vpc_prod >> ns_prod >> data_prod


if __name__ == "__main__":
    render()
    print(f"wrote {OUT / 'accounts.svg'}")
