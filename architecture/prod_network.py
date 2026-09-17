"""Level 2 — production network: 3 AZs, CIDRs, edge, bastion.

CIDRs are computed the same way as tf-modules/modules/VPC:
  azs             = first 3 of eu-west-2 (a, b, c)
  private_subnets = cidrsubnet(10.30.0.0/16, 4, k)
  public_subnets  = cidrsubnet(10.30.0.0/16, 8, k + 48)
  single_nat_gateway = true
"""

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.aws.compute import EKS
from diagrams.aws.database import Aurora, ElastiCache
from diagrams.aws.management import SystemsManager
from diagrams.aws.network import CloudFront, NATGateway, NLB, PrivateSubnet, PublicSubnet, Route53
from diagrams.aws.security import CertificateManager, WAF
from diagrams.aws.storage import S3
from diagrams.onprem.client import Users

import aws_style as aws

OUT = Path(__file__).resolve().parents[1] / "docs" / "architecture"
OUT.mkdir(parents=True, exist_ok=True)
OFF = Edge(style="dashed", constraint="false")


def render() -> None:
    path = str(OUT / "prod-network")
    with Diagram(
        "Production network — AZs and subnets",
        filename=path,
        show=False,
        direction="TB",
        graph_attr={**aws.GRAPH, "ranksep": "0.45"},
        node_attr=aws.NODE,
        edge_attr=aws.EDGE,
        outformat=["svg", "png"],
    ):
        users = Users("Users")
        dns = Route53("Route 53")

        with Cluster("AWS Cloud", graph_attr=aws.CLOUD):
            with Cluster("Account 389068786427", graph_attr=aws.ACCOUNT):
                with Cluster("us-east-1", graph_attr=aws.REGION):
                    waf = WAF("WAF")
                    acm = CertificateManager("ACM")
                    cf = CloudFront("CloudFront")

                with Cluster("eu-west-2", graph_attr=aws.REGION):
                    s3 = S3("S3 images")
                    with Cluster("VPC rfe-prod-vpc  10.30.0.0/16", graph_attr=aws.VPC):
                        with Cluster("AZ eu-west-2a", graph_attr=aws.AZ):
                            with Cluster("Public 10.30.48.0/24", graph_attr=aws.PUBLIC_SUBNET):
                                pub_a = PublicSubnet("public")
                                nat = NATGateway("NAT\n(only NAT in VPC)")
                                bastion = SystemsManager("SSM bastion")
                            with Cluster("Private 10.30.0.0/20", graph_attr=aws.PRIVATE_SUBNET):
                                priv_a = PrivateSubnet("private")

                        with Cluster("AZ eu-west-2b", graph_attr=aws.AZ):
                            with Cluster("Public 10.30.49.0/24", graph_attr=aws.PUBLIC_SUBNET):
                                pub_b = PublicSubnet("public")
                            with Cluster("Private 10.30.16.0/20", graph_attr=aws.PRIVATE_SUBNET):
                                priv_b = PrivateSubnet("private")

                        with Cluster("AZ eu-west-2c", graph_attr=aws.AZ):
                            with Cluster("Public 10.30.50.0/24", graph_attr=aws.PUBLIC_SUBNET):
                                pub_c = PublicSubnet("public")
                            with Cluster("Private 10.30.32.0/20", graph_attr=aws.PRIVATE_SUBNET):
                                priv_c = PrivateSubnet("private")

                        with Cluster("Spans all private subnets", graph_attr=aws.PRIVATE_SUBNET):
                            nlb = NLB("Internal NLB\nCloudFront VPC origin")
                            eks = EKS("EKS + Karpenter")
                            aurora = Aurora("Aurora + RDS Proxy")
                            valkey = ElastiCache("Valkey")
                            msk = ManagedStreamingForKafka("MSK + Debezium")

        users >> dns >> waf >> cf
        acm >> OFF >> cf
        cf >> Edge(label="images") >> s3
        cf >> Edge(label="VPC origin") >> nlb >> eks
        pub_a >> nat
        pub_a >> bastion
        eks >> Edge(style="dashed", label="egress", constraint="false") >> nat
        bastion >> Edge(style="dashed", label="break-glass", constraint="false") >> aurora
        priv_a >> OFF >> eks
        priv_b >> OFF >> eks
        priv_c >> OFF >> eks
        eks >> aurora
        eks >> valkey
        eks >> msk
        _ = (pub_b, pub_c)  # subnets exist; no extra edges


if __name__ == "__main__":
    render()
    print(f"wrote {OUT / 'prod-network.svg'}")
