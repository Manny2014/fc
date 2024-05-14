

# Create GKE Cluster
# ==> https://github.com/terraform-google-modules/terraform-google-kubernetes-engine/tree/v17.3.0/examples/shared_vpc

module "gke" {
  source = "terraform-google-modules/kubernetes-engine/google"
  # PRIVATE CLUSTER (re-run init)
  #source  = "terraform-google-modules/kubernetes-engine/google//modules/private-cluster"
  version = "v19.0.0"

  project_id              = data.terraform_remote_state.dev_project.outputs.project.project_id
  name                    = "${var.cluster_name}"
  region                  = data.terraform_remote_state.bootstrap.outputs.org_default_location
  regional                = true
  zones                   = ["us-central1-a"]
  network                 = data.terraform_remote_state.host_project.outputs.vpc.network.id
  network_project_id      = data.terraform_remote_state.host_project.outputs.project.id
  subnetwork              = "us-central1-0"
  ip_range_pods           = "us-central1-0-scidr-0"
  ip_range_services       = "us-central1-0-scidr-32"
  grant_registry_access   = true
  create_service_account  = true
  initial_node_count      = 0
  cluster_resource_labels = { "test" : "label" }
  release_channel         = "STABLE"
  kubernetes_version      = "latest"
  # service_account            = "gke-service-account@${data.terraform_remote_state.dev_project.outputs.project.project_id}.iam.gserviceaccount.com"
  remove_default_node_pool = true
  registry_project_ids     = ["${data.terraform_remote_state.host_project.outputs.project.id}"]
  authenticator_security_group = "gke-security-groups@${data.terraform_remote_state.bootstrap.outputs.org.domain}"
  enable_binary_authorization  = true
  # PRIVATE CLUSTER
  # enable_private_endpoint    = true
  # enable_private_nodes       = true
  # master_ipv4_cidr_block    = "192.168.1.0/28"

  # ADDITIONAL FW RULES
  # add_cluster_firewall_rules = false
  # firewall_inbound_ports     = ["9443", "15017"] # Additional FW rules
  
  node_pools_oauth_scopes = {
    all = [
        "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
  
  node_pools_labels = {
    all = {}

    default-node-pool = {
      default-node-pool = true
    }
  }

  node_pools = [
    {
      name               = "node-pool-01"
      min_count          = 3
      max_count          = 6
      local_ssd_count    = 0
      disk_size_gb       = 100
      disk_type          = "pd-standard"
      image_type         = "COS"
      auto_repair        = true
      auto_upgrade       = true
      preemptible        = true
      max_pods_per_node  = 110
      initial_node_count = 3
    },
  ]
}
